import sys
import argparse
from utils import generate_module_stubs, generate_component_stubs


def main(site_package_dir,modules_name,use_pybind11 = False,dump_file_location = None):

    work_dir = site_package_dir[0]
    modules = modules_name

    #Generate stubs using either pybind11-stubgen or mypy version of stubgen

    print(f"Generating stubgen for modules: {modules}")

    for module_name in modules:
        generate_module_stubs(module_name, work_dir,use_pybind11,dump_file_location)

    #Generate stubs for components using the factory
    target_name="Sofa.Component"
    generate_component_stubs(work_dir,target_name,dump_file_location)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='generate_stubs',
                    description='Generates python stubs for SOFA modules')

    parser.add_argument('--use_pybind11',action='store_true',help='If flag is present, will use pybind11-stubgen instead of mypy stugen')
    parser.add_argument('--dump_file_location',nargs='?', const='GenerateStubsDumpInfos.txt', default=None,help='If flag is present, will generate a files in the current dir which line are a concatenation of the absolute path of generated file and their target path separated by ;')
    parser.add_argument('-d','--site_package_dir',nargs=1,help='Path to the site-package folder containing the SOFA modules')
    parser.add_argument('-m','--modules_name',nargs='+',help='List of modules names to generate stubs for')

    args = parser.parse_args()

    main(args.site_package_dir,args.modules_name,args.use_pybind11,args.dump_file_location)
