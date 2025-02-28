/******************************************************************************
*                              SofaPython3 plugin                             *
*                  (c) 2021 CNRS, University of Lille, INRIA                  *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this program. If not, see <http://www.gnu.org/licenses/>.        *
*******************************************************************************
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/

#include <fstream>

#if defined(__linux__)
#include <dlfcn.h>
#endif

#include <sofa/helper/system/PluginManager.h>
using sofa::helper::system::PluginManager;
using sofa::helper::system::Plugin;

#include <sofa/helper/system/FileRepository.h>
#include <sofa/helper/system/SetDirectory.h>
#include <sofa/helper/system/FileSystem.h>
using sofa::helper::system::FileSystem;

#include <sofa/helper/Utils.h>
using sofa::helper::Utils;

#include <sofa/helper/StringUtils.h>
using sofa::helper::getAStringCopy ;

#include <SofaPython3/PythonEnvironment.h>

#include <sofa/helper/logging/Messaging.h>

#include <sofa/simulation/SceneLoaderFactory.h>
using sofa::simulation::SceneLoaderFactory;

#include <pybind11/embed.h>
#include <pybind11/eval.h>

/// Makes an alias for the pybind11 namespace to increase readability.
namespace py { using namespace pybind11; }

#include "SceneLoaderPY3.h"
using sofapython3::SceneLoaderPY3;

MSG_REGISTER_CLASS(sofapython3::PythonEnvironment, "SofaPython3::PythonEnvironment")

namespace sofapython3
{

class PythonEnvironmentModule
{
public:
    py::module m_sofaModule ;
    py::module m_sofaRuntimeModule ;
};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// \brief The PythonEnvironmentData class which hold "static" data as long as python is running
///
/// The class currently hold the argv that are exposed in the python 'sys.argv'.
/// The elements added are copied and the object hold the pointer to the memory allocated.
/// The memory is release when the object is destructed or the reset function called.
///
/// Other elements than sys.argv may be added depending on future needs.
///
////////////////////////////////////////////////////////////////////////////////////////////////////
class PythonEnvironmentData
{
public:
    ~PythonEnvironmentData() { reset(); }

    int size() { return m_argv.size(); }

    void add(const std::string& data)
    {
        m_argv.push_back( Py_DecodeLocale(data.c_str(), nullptr) );
    }

    void reset()
    {
        for(auto s : m_argv){
            PyMem_Free(s);
        }
        m_argv.clear();
        addedPath.clear();
    }

    wchar_t* getDataAt(unsigned int index)
    {
        return m_argv[index];
    }

    wchar_t** getDataBuffer()
    {
        return &m_argv[0];
    }

    std::set<std::string> addedPath;
private:
    std::vector<wchar_t*> m_argv;
};

PythonEnvironmentData* PythonEnvironment::getStaticData()
{
    static PythonEnvironmentData* m_staticdata { nullptr } ;

    if( !m_staticdata )
    {
        // TODO: replace new with reference counted pointer (make_unique or make_shared)
        m_staticdata = new PythonEnvironmentData();
    }
    return m_staticdata;
}

PythonEnvironmentModule* PythonEnvironment::getStaticModule()
{
    PythonEnvironment::gil lock;

    static PythonEnvironmentModule* m_staticmodule { nullptr } ;
    if( !m_staticmodule )
    {
        // TODO: replace new with reference counted pointer (make_unique or make_shared)
        m_staticmodule = new PythonEnvironmentModule();
        executePython([]{
            getStaticModule()->m_sofaModule = py::module::import("Sofa");
            getStaticModule()->m_sofaRuntimeModule = py::module::import("SofaRuntime");
        });
    }
    return m_staticmodule;
}

std::string PythonEnvironment::pluginLibraryPath = "";

SOFAPYTHON3_API py::module PythonEnvironment::importFromFile(const std::string& module, const std::string& path, py::object* globals)
{
    PythonEnvironment::gil lock;
    py::dict locals;
    locals["module_name"] = py::cast(module); // have to cast the std::string first
    locals["path"]        = py::cast(path);

    py::object globs = py::globals();
    if (globals == nullptr)
        globals = &globs;

    py::eval<py::eval_statements>(            // tell eval we're passing multiple statements
                                              "import importlib.util \n"
                                              "importlib.machinery.SOURCE_SUFFIXES.append('pyscn') \n"
                                              "spec = importlib.util.spec_from_file_location(module_name, path) \n"
                                              "new_module = importlib.util.module_from_spec(spec) \n"
                                              "spec.loader.exec_module(new_module)",
                                              *globals,
                                              locals);
    py::module m =  py::cast<py::module>(locals["new_module"]);
    return m;
}


void PythonEnvironment::Init()
{
    std::string pythonVersion = Py_GetVersion();
    msg_info("SofaPython3") << "Initializing with python version " << pythonVersion;

    if( !SceneLoaderFactory::getInstance()->getEntryFileExtension("py3") )
    {
        msg_info("SofaPython3") << "Registering a scene loader for [.py, .py3, .pyscn, .py3scn] files." ;
        // TODO: replace new with reference counted pointer (make_unique or make_shared)
        SceneLoaderFactory::getInstance()->addEntry(new SceneLoaderPY3());
    }

    /// Prevent the python terminal from being buffered, not to miss or mix up traces.
    if( putenv( (char*)"PYTHONUNBUFFERED=1" ) )
        msg_warning("SofaPython3") << "failed to set environment variable PYTHONUNBUFFERED";

    if ( !Py_IsInitialized() )
    {
        msg_info("SofaPython3") << "Initializing python";
        py::initialize_interpreter();
        // the first gil aquisition should happen right after the python interpreter
        // is initialized.
        static const PyThreadState* init = PyEval_SaveThread(); (void) init;
    }

    PyEval_InitThreads();

    // Required for sys.path, used in addPythonModulePath().
    executePython([]{ PyRun_SimpleString("import sys");});

    // Force C locale.
    executePython([]{ PyRun_SimpleString("import locale");});
    executePython([]{ PyRun_SimpleString("locale.setlocale(locale.LC_ALL, 'C')");});

    // Workaround: try to import numpy and to launch numpy.finfo to cache data;
    // this prevents a deadlock when calling numpy.finfo from a worker thread.
    executePython([]{ PyRun_SimpleString("try:\n\timport numpy;numpy.finfo(float)\nexcept:\n\tpass");});

    // Workaround: try to import scipy from the main thread this prevents a deadlock when importing
    // scipy from a worker thread when we use the SofaScene asynchronous loading
    executePython([]{ PyRun_SimpleString("try:\n\tfrom scipy import misc, optimize\nexcept:\n\tpass\n");});

    // If the script directory is not available (e.g. if the interpreter is invoked interactively
    // or if the script is read from standard input), path[0] is the empty string,
    // which directs Python to search modules in the current directory first.
    executePython([]{ PyRun_SimpleString(std::string("sys.path.insert(0,\"\")").c_str());});

    // Add the paths to the plugins' python modules to sys.path.  Those paths
    // are read from all the files in 'etc/sofa/python.d'
    std::string confDir = Utils::getSofaPathPrefix() + "/etc/sofa/python.d";
    if (FileSystem::exists(confDir))
    {
        std::vector<std::string> files;
        FileSystem::listDirectory(confDir, files);
        for (size_t i=0; i<files.size(); i++)
        {
            addPythonModulePathsFromConfigFile(confDir + "/" + files[i]);
        }
    }

    /// Add the directories listed in the SOFAPYTHON3_PLUGINS_PATH environnement
    /// variable to sys.path
    const std::string envVarName = "SOFAPYTHON3_PLUGINS_PATH";
    const std::string deprecatedEnvVarName = "SOFAPYTHON_PLUGINS_PATH";
    std::string usedEnvVarName = envVarName;

    char* deprecatedPathVar = getenv(deprecatedEnvVarName.c_str());
    char* pathVar = getenv(envVarName.c_str());
    
    // case where only the deprecated env var is set
    if (pathVar != nullptr && deprecatedPathVar == nullptr)
    {
        msg_deprecated("SofaPython3") << deprecatedEnvVarName << " environment variable is deprecated, use " << envVarName << " instead.";
        usedEnvVarName = "SOFAPYTHON_PLUGINS_PATH";
    }
    // case where both env vars are set
    else if (pathVar != nullptr && deprecatedPathVar != nullptr)
    {
        msg_deprecated("SofaPython3") << deprecatedEnvVarName << " and " << envVarName << " environment variables are both set.";
        msg_deprecated("SofaPython3") << deprecatedEnvVarName << " is deprecated, and only " << envVarName << " will be used.";
    }
    
    sofa::helper::system::FileRepository pluginPathsRepository(envVarName.c_str());
    const auto& pluginPaths = pluginPathsRepository.getPaths();
    for (auto pluginPath : pluginPaths)
    {
        std::string cleanPath = FileSystem::cleanPath(pluginPath);
        addPythonModulePath(cleanPath);
    }

    // Add sites-packages wrt the plugin
    addPythonModulePathsFromPlugin("SofaPython3");

    // Lastly, we (try to) add modules from the root of SOFA
    addPythonModulePathsFromDirectory( Utils::getSofaPathPrefix() );

    executePython([]{ PyRun_SimpleString("import SofaRuntime");});

    // python livecoding related
    executePython([]{ PyRun_SimpleString("from Sofa.livecoding import onReimpAFile");});

    // general sofa-python stuff

    // python modules are automatically reloaded at each scene loading
    setAutomaticModuleReload( true );

    // Initialize pluginLibraryPath by reading PluginManager's map
    std::map<std::string, Plugin>& map = PluginManager::getInstance().getPluginMap();
    for( const auto& elem : map)
    {
        Plugin p = elem.second;
        if ( strcmp(p.getModuleName(), sofa_tostring(SOFA_TARGET)) == 0 )
        {
            pluginLibraryPath = elem.first;
        }
    }

    s_isInitialized = true;
}

// Single implementation for the three different versions
template<class T>
void executePython_(const T& emitter, std::function<void()> cb)
{
    sofapython3::PythonEnvironment::gil acquire;

    try{
        cb();
    }catch(py::error_already_set& e)
    {
        std::stringstream tmp;
        tmp << "Unable to execute code." << msgendl
                     << "Python exception:" << msgendl
                     << "  " << e.what()
                     << PythonEnvironment::getPythonCallingPointString();
        msg_error(emitter) << tmp.str();
    }
}

void PythonEnvironment::executePython(const std::string& emitter, std::function<void()> cb)
{
    return executePython_(emitter, cb);
}

void PythonEnvironment::executePython(std::function<void()> cb)
{
    return executePython_("SofaPython3::executePython", cb);
}

void PythonEnvironment::executePython(const sofa::core::objectmodel::Base* b, std::function<void()> cb)
{
    return executePython_(b, cb);
}

void PythonEnvironment::Release()
{
    /// Finish the Python Interpreter
    /// obviously can't use raii here
    if(  Py_IsInitialized() ) {
        PyGILState_Ensure();
        py::finalize_interpreter();
        getStaticData()->reset();
    }

}

void PythonEnvironment::addPythonModulePath(const std::string& path)
{
    if (!(FileSystem::exists(path) && FileSystem::isDirectory(path)))
    {
        msg_warning("SofaPython3") << "Could not add '" + path + "'" << " to sys.path (it does not exist or is not a directory)";
        return;
    }

    PythonEnvironmentData* data = getStaticData() ;
    if (  data->addedPath.find(path)==data->addedPath.end())
    {
        // note not to insert at first 0 place
        // an empty string must be at first so modules can be found in the current directory first.

        executePython([&]{ PyRun_SimpleString(std::string("sys.path.insert(1,\""+path+"\")").c_str());});

        msg_info("SofaPython3")<< "Added '" + path + "' to sys.path";
        data->addedPath.insert(path);
    }
}

void PythonEnvironment::addPythonModulePathsFromConfigFile(const std::string& path)
{
    std::ifstream configFile(path.c_str());
    std::string line;
    while(std::getline(configFile, line))
    {
        if (!FileSystem::isAbsolute(line))
        {
            line = Utils::getSofaPathPrefix() + "/" + line;
        }
        addPythonModulePath(line);
    }
}

void PythonEnvironment::addPythonModulePathsFromDirectory(const std::string& directory)
{
    if ( ! (FileSystem::exists(directory) && FileSystem::isDirectory(directory)) )
    {
        return;
    }

    // Using python<MAJOR>.<MINOR> directory suffix for modules paths is now the recommanded
    // standard location: https://docs.python.org/3.11/install/#how-installation-works and
    // https://docs.python.org/3.11/library/site.html#module-site 
    const auto pythonVersionFull = std::string{Py_GetVersion()};
    const auto pythonVersion = pythonVersionFull.substr(0, pythonVersionFull.find(" ")); // contains major.minor.patch
    const auto pythonVersionMajorMinor = pythonVersion.substr(0, pythonVersion.rfind(".")); // contains only manjor.minor
    const auto pythonMajorMinorSuffix = "/python" + pythonVersionMajorMinor;

    std::vector<std::string> searchDirs = {
        directory,
        directory + "/lib",
        directory + pythonMajorMinorSuffix,
        directory + "/python3" // deprecated
    };

    // Iterate in the pluginsDirectory and add each sub directory with a 'python' name
    // this is mostly for in-tree builds.
    std::vector<std::string> files;
    FileSystem::listDirectory(directory, files);
    for (std::vector<std::string>::iterator i = files.begin(); i != files.end(); ++i)
    {
        const std::string subdir = directory + "/" + *i;
        if (FileSystem::exists(subdir) && FileSystem::isDirectory(subdir))
        {
            const std::vector<std::string> suffixes = {
              pythonMajorMinorSuffix,
              "/python3" // deprecated
            };
            for (const auto& suffix : suffixes)
            {
              const auto pythonSubdir = subdir + suffix;
              if (FileSystem::exists(pythonSubdir) && FileSystem::isDirectory(pythonSubdir))
              {
                searchDirs.push_back(pythonSubdir);
              }
            }
        }
    }

    // For each of the directories in pythonDirs, search for a site-packages entry
    for(std::string& searchDir : searchDirs)
    {
        // Search for a subdir "site-packages"
        if (FileSystem::exists(searchDir + "/site-packages") && FileSystem::isDirectory(searchDir + "/site-packages"))
        {
            addPythonModulePath(searchDir + "/site-packages");
        }
    }
}

void PythonEnvironment::addPythonModulePathsFromPlugin(const std::string& pluginName)
{
    std::map<std::string, Plugin>& map = PluginManager::getInstance().getPluginMap();
    for( const auto& elem : map)
    {
        Plugin p = elem.second;
        if ( p.getModuleName() == pluginName )
        {
            // 1. Try to find the plugin directory starting from SOFA root
            for ( auto path : sofa::helper::system::PluginRepository.getPaths() )
            {
                std::string pluginRoot = FileSystem::cleanPath( path + "/" + pluginName );
                if ( FileSystem::exists(pluginRoot) && FileSystem::isDirectory(pluginRoot) )
                {
                    addPythonModulePathsFromDirectory(pluginRoot);
                    return;
                }
            }

            // 2. Try to find the plugin directory starting from the plugin library
            std::string pluginLibraryPath = elem.first;
            // moduleRoot can be 1 or 2 levels above the library directory
            // like "plugin_name/lib/plugin_name.so"
            // or "sofa_root/bin/Release/plugin_name.dll"
            std::string moduleRoot = FileSystem::getParentDirectory(pluginLibraryPath);
            int maxDepth = 0;
            while(!FileSystem::exists(moduleRoot + "/lib") && maxDepth < 2)
            {
                moduleRoot = FileSystem::getParentDirectory(moduleRoot);
                maxDepth++;
            }
            addPythonModulePathsFromDirectory(moduleRoot);
            return;
        }
    }
    msg_info("SofaPython3") << pluginName << " not found in PluginManager's map.";
}

void PythonEnvironment::addPluginManagerCallback()
{
    PluginManager::getInstance().addOnPluginLoadedCallback(pluginLibraryPath,
        [](const std::string& pluginLibraryPath, const Plugin& plugin)
        {
            SOFA_UNUSED(pluginLibraryPath);
            // search for plugin with PluginRepository
            for ( auto path : sofa::helper::system::PluginRepository.getPaths() )
            {
                std::string pluginRoot = FileSystem::cleanPath( path + "/" + plugin.getModuleName() );
                if ( FileSystem::exists(pluginRoot) && FileSystem::isDirectory(pluginRoot) )
                {
                    addPythonModulePathsFromDirectory(pluginRoot);
                    return;
                }
            }
        }
    );
}

void PythonEnvironment::removePluginManagerCallback()
{
    PluginManager::getInstance().removeOnPluginLoadedCallback(pluginLibraryPath);
}


// some basic RAII stuff to handle init/termination cleanly
namespace
{

struct raii {
    raii() {
        /// initialization is done when loading the plugin
        /// otherwise it can be executed too soon
        /// when an application is directly linking with the SofaPython library
    }

    ~raii() {
        //PythonEnvironment::Release();
    }
};

static raii singleton;

} // namespace


/// basic script functions
std::string PythonEnvironment::getError()
{
    gil lock;
    std::string error;

    PyObject *ptype, *pvalue /* error msg */, *ptraceback /*stack snapshot and many other informations (see python traceback structure)*/;
    PyErr_Fetch(&ptype, &pvalue, &ptraceback);
    if(pvalue)
        error = PyBytes_AsString(pvalue);

    return error;
}

bool PythonEnvironment::runString(const std::string& script)
{
    gil lock;
    PyObject* pDict = PyModule_GetDict(PyImport_AddModule("__main__"));
    PyObject* result = PyRun_String(script.data(), Py_file_input, pDict, pDict);

    if(0 == result)
    {
        msg_error("SofaPython3") << "Script (string) import error";
        PyErr_Print();
        return false;
    }

    Py_DECREF(result);

    return true;
}

bool PythonEnvironment::runFile(const std::string& filename,
                                const std::vector<std::string>& arguments)
{
    py::object main = py::module::import(filename.c_str()).attr("__main__");

    main(arguments);
    return true;
}


std::string PythonEnvironment::getStackAsString()
{
    gil lock;
    PyObject* pDict = PyModule_GetDict(PyImport_AddModule("SofaRuntime"));
    PyObject* pFunc = PyDict_GetItemString(pDict, "getStackForSofa");
    if (PyCallable_Check(pFunc))
    {
        PyObject* res = PyObject_CallFunction(pFunc, nullptr);
        std::string tmp=PyBytes_AsString(PyObject_Str(res));
        Py_DECREF(res) ;
        return tmp;
    }
    return "Python Stack is empty.";
}

std::string PythonEnvironment::getPythonCallingPointString()
{
    gil lock;
    return py::cast<std::string>(getStaticModule()->m_sofaModule.attr("getPythonCallingPointAsString")());
}

sofa::helper::logging::FileInfo::SPtr PythonEnvironment::getPythonCallingPointAsFileInfo()
{
    gil lock;
    py::tuple cp = getStaticModule()->m_sofaRuntimeModule.attr("getPythonCallingPoint")();
    return SOFA_FILE_INFO_COPIED_FROM(py::cast<std::string>(cp[0]), py::cast<int>(cp[1]));
}

void PythonEnvironment::setArguments(const std::string& filename, const std::vector<std::string>& arguments)
{
    gil lock;
    const std::string basename = sofa::helper::system::SetDirectory::GetFileNameWithoutExtension(filename.c_str());

    PythonEnvironmentData* data = getStaticData() ;
    data->reset() ;
    data->add( basename );

    if(!arguments.empty()) {
        for(const std::string& arg : arguments) {
            data->add(arg);
        }
    }

    PySys_SetArgvEx( data->size(), data->getDataBuffer(), 0);
}

void PythonEnvironment::SceneLoaderListerner::rightBeforeLoadingScene()
{
    // unload python modules to force importing their eventual modifications
    executePython([]{ PyRun_SimpleString("SofaRuntime.unloadModules()");});
}

void PythonEnvironment::setAutomaticModuleReload( bool b )
{
    if( b )
        SceneLoader::addListener( SceneLoaderListerner::getInstance() );
    else
        SceneLoader::removeListener( SceneLoaderListerner::getInstance() );
}

void PythonEnvironment::excludeModuleFromReload( const std::string& moduleName )
{
    executePython([&]{ PyRun_SimpleString( std::string( "try: SofaRuntime.__SofaPythonEnvironment_modulesExcludedFromReload.append('" + moduleName + "')\nexcept:pass" ).c_str() );});
}

static const bool debug_gil = false;
static PyGILState_STATE lock(const char* trace) {
    if(debug_gil) {
        auto tid = PyGILState_GetThisThreadState()->thread_id % 10000;
        auto id = PyGILState_GetThisThreadState()->id;

        if(trace)
            std::clog << ">> ["<<id << "(" << tid  <<")]:: " << trace<< " wants the gil" << std::endl;
        else
            std::clog << ">> ["<<id << "(" << tid  <<")]:: wants the gil" << std::endl;
    }
    return PyGILState_Ensure();
}

PythonEnvironment::gil::gil(const char* trace)
    : state(lock(trace)),
      trace(trace) { }


PythonEnvironment::gil::~gil() {

    auto tid = PyGILState_GetThisThreadState()->thread_id % 10000;
    auto id = PyGILState_GetThisThreadState()->id;
    if(debug_gil) {
        if(trace)
            std::clog << "<< ["<<id << "(" << tid  <<")]: " << trace << " prepare to released the gil" << std::endl;
        else
            std::clog << "<< ["<<id << "(" << tid  <<")]:: prepare to released the gil" << std::endl;
    }

    PyGILState_Release(state);
    if(debug_gil) {
        if(trace)
            std::clog << "<< ["<<id << "(" << tid  <<")]: " << trace << " released the gil" << std::endl;
        else
            std::clog << "<< ["<<id << "(" << tid  <<")]: released the gil" << std::endl;
    }

}


//PythonEnvironment::no_gil::no_gil(const char* trace)
//    : state(PyEval_SaveThread()),
//      trace(trace) {
//    if(debug_gil && trace) {
//        std::clog << ">> " << trace << " temporarily released the gil" << std::endl;
//    }
//}

//PythonEnvironment::no_gil::~no_gil() {

//    if(debug_gil && trace) {
//        std::clog << "<< " << trace << " wants to reacquire the gil" << std::endl;
//    }

//    PyEval_RestoreThread(state);
//}

} // namespace sofapython



