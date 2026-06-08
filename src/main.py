from website.generator import *
from filemanager import *
import sys

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    base_path = "/" if sys.argv[0] is None else sys.argv[0]
    print(base_path)
    clean_folder(dir_path_public)
    copy_files(dir_path_static, dir_path_public)
    generate_pages_recursive(
        base_path,
        dir_path_content,
        template_path,
        dir_path_public,
    )
    
main()
