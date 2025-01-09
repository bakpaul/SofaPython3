import sys
import os
import shutil
from sofaStubgen import load_component_list, create_sofa_stubs
from mypy.stubgen import parse_options, generate_stubs
import argparse
import pathlib
import io




#Method to use pybind11-stubgen
def pybind11_stub(module_name: str):
    import logging
    from pybind11_stubgen import CLIArgs, stub_parser_from_args, Printer, to_output_and_subdir, run, Writer
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s - [%(levelname)7s] %(message)s",
    )
    args = CLIArgs(
        module_name=module_name,
        output_dir='./out',
        stub_extension="pyi",
        # default ags:
        root_suffix=None,
        ignore_all_errors=False,
        ignore_invalid_identifiers=None,
        ignore_invalid_expressions=None,
        ignore_unresolved_names=None,
        exit_code=False,
        numpy_array_wrap_with_annotated=False,
        numpy_array_use_type_var=False,
        numpy_array_remove_parameters=False,
        enum_class_locations=[],
        print_safe_value_reprs=None,
        print_invalid_expressions_as_is=False,
        dry_run=False)

    parser = stub_parser_from_args(args)
    printer = Printer(invalid_expr_as_ellipses=not args.print_invalid_expressions_as_is)

    out_dir, sub_dir = to_output_and_subdir(
        output_dir=args.output_dir,
        module_name=args.module_name,
        root_suffix=args.root_suffix,
    )

    run(
        parser,
        printer,
        args.module_name,
        out_dir,
        sub_dir=sub_dir,
        dry_run=args.dry_run,
        writer=Writer(stub_ext=args.stub_extension),
    )

class shutilFilter:
    def __init__(self,fromFolder,destFolder):
        self.fromFolder = fromFolder
        self.destFolder = destFolder
        self.dumpFilePaths = []

    def dumpFileInfo(self,fromFilePath,destFilePath):
        self.dumpFilePaths.append(f"{os.path.realpath(fromFilePath)};{os.path.realpath(destFilePath)}")


    def findDestPath(self,currentRelativeToFromPath):

        absoluteFromFolder = os.path.abspath(self.fromFolder)

        #here we remove the first folder because it is the output folder
        destPath = ''
        head = os.path.abspath(currentRelativeToFromPath)
        while(head != absoluteFromFolder):
            head,tail = os.path.split(head)
            destPath = os.path.join(destPath,tail)

        return os.path.abspath(os.path.join(self.destFolder,destPath))

    def writeFileInfo(self,filename):
        output = io.open(filename, mode='a')
        for path in self.dumpFilePaths:
            print(path, file=output)

    def __call__(self,path, objectList):
        return []

# This class is used with shutil.copytree to skip already existing files in dest folder.
class noOverrideFilter(shutilFilter):
    def __init__(self,fromFolder,destFolder,dump_file_location=False):
        super().__init__(fromFolder,destFolder)
        self.dumpFileLocation = dump_file_location

    def __call__(self,path, objectList):

        destPath = self.findDestPath(path)
        returnList = []
        for obj in objectList:
            objDestPath = os.path.join(destPath,obj)
            objFromPath = os.path.join(path,obj)
            if(os.path.isfile(objDestPath)):
                returnList.append(obj)
            elif(self.dumpFileLocation and os.path.isfile(objFromPath)):
                self.dumpFileInfo(objFromPath,objDestPath)

        return returnList

class dumpFilesFiler(shutilFilter):
    def __init__(self,fromFolder,destFolder):
        super().__init__(fromFolder,destFolder)

    def __call__(self,path, objectList):

        destPath = self.findDestPath(path)

        for obj in objectList:
            objFromPath = os.path.join(path,obj)
            if(os.path.isfile(objFromPath)):
                objDestPath = os.path.join(destPath,obj)
                self.dumpFileInfo(objFromPath,objDestPath)
        return []

#
# def dumpFileLocation(fromFolder,destFolder):
#     allFiles = list(pathlib.Path(fromFolder).rglob("*"))



#Generate stubs using either pybind11-stubgen or mypy version of stubgen
def generate_module_stubs(module_name, work_dir, usePybind11_stubgen = False, dump_file_location = None):
    print(f"Generating stubgen for {module_name} in {work_dir}")

    if(usePybind11_stubgen):
        #Use pybind11 stubgen
        #Could be replaced by an os call to
        #subprocess.run(["pybind11-stubgen", module_name, "-o", "out"], check=True)
        pybind11_stub(module_name)
    else:
        #Use mypy stubgen
        options = parse_options(["-v","-p",module_name,"--include-docstrings","--no-analysis", "--ignore-errors"])
        generate_stubs(options)

    module_out_dir = os.path.join("out", module_name)
    target_dir = os.path.join(work_dir, module_name)


    if os.path.isdir(module_out_dir):
        if(dump_file_location is not None):
            DFF = dumpFilesFiler(module_out_dir,target_dir)
            shutil.copytree(module_out_dir, target_dir, dirs_exist_ok=True,ignore=DFF)
            DFF.writeFileInfo(dump_file_location)
        else:
            shutil.copytree(module_out_dir, target_dir, dirs_exist_ok=True)

        print(f"Resync terminated for copying '{module_name}' to '{target_dir}'")

    shutil.rmtree("out", ignore_errors=True)

#Generate stubs for components using the factory
def generate_component_stubs(work_dir,target_name, dump_file_location = None):
    print(f"Generating stubgen for all components in Sofa.Components using custom sofaStubgen.py")

    components = load_component_list(target_name)
    create_sofa_stubs(components, "out/")


    sofa_out_dir = os.path.join("out",*target_name.split('.'))
    target_dir = os.path.join(work_dir, *target_name.split('.'))

    if os.path.isdir(sofa_out_dir):
        #For now on we don't want no overriting of file, we thus use the parameter 'ignore=noOverrideFilter(sofa_out_dir,target_dir)' to skip files already existing in dest folder because it might brake the lib.
        # When file merging is supported by create_sofa_stubs this will be removed because then, we will want to override the dest files because we've already did the merge
        if(dump_file_location is not None):
            DFF = noOverrideFilter(sofa_out_dir,target_dir,True)
            shutil.copytree(sofa_out_dir, target_dir, dirs_exist_ok=True,ignore=DFF)
            DFF.writeFileInfo(dump_file_location)
        else:
            shutil.copytree(sofa_out_dir, target_dir, dirs_exist_ok=True, ignore=noOverrideFilter(sofa_out_dir,target_dir))
        print("Resync terminated.")

    shutil.rmtree("out", ignore_errors=True)
