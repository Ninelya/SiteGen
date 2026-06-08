import os
from parsers.parser import *

def generate_pages_recursive(
        base_path: str,
        sourse: str,
        template_path: str,
        destination: str) -> None:
    for item in os.listdir(sourse):
        sourse_path = os.path.join(sourse, item)
        dest_path = os.path.join(destination, item)
        try:
            if (os.path.isfile(sourse_path)
                and sourse_path.endswith(".md")):
                dest_path = dest_path.rstrip(".md") + ".html"
                print(f"{sourse_path} -> {dest_path}")
                generate_page(base_path, sourse_path, template_path, dest_path)
            elif os.path.isdir(sourse_path):
                print(f"{sourse_path} -> {dest_path}")
                os.mkdir(dest_path)
                generate_pages_recursive(base_path, sourse_path, template_path, dest_path)
        except Exception as e:
            print(f"Failed to generate {sourse_path} to {dest_path}. Reason: {e}")

def generate_page(
        base_path: str,
        from_path: str,
        template_path: str,
        dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    markdown = open(from_path).read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    
    template = open(template_path).read()
    full_page = template\
    .replace("{{ Title }}", title)\
    .replace("{{ Content }}", content)\
    .replace("href=\"/", f"href=\"{base_path}/")\
    .replace("src=\"/", f"src=\"{base_path}/")
    
    with open(dest_path, "w") as page:
        page.write(full_page)

