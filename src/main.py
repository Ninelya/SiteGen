from website.generator import *
from filemanager import *

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    clean_folder(dir_path_public)
    copy_files(dir_path_static, dir_path_public)
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )
    
main()
