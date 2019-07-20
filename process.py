"""
Generates code sample HTML from a given directory.
"""

import argparse
import os
import shutil
import json

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

from bs4 import BeautifulSoup


class UnknownExtension(Exception):
    """
    Raised when a file that is to be processed is of a type that the tool
    cannot understand.
    """

def generate_css(destination_dir=".", dry_run=False):
    """
    Generate CSS files for all known styles
    """
    styles = sorted(list(get_all_styles()))
    style_index = []
    location = os.path.join(os.path.abspath(destination_dir), "css", "syntax")
    if not os.path.isdir(location):
        print(f"Making destination directory {location}")
        if not dry_run:
            os.makedirs(location)
    else:
        print(f"Destination directory {location} exists")
        
    for style in styles:
        dest = os.path.join(location, f"syntax.{style}.css")
        info = {
            'name': style,
            'path': os.path.relpath(dest, destination_dir)
        }
        style_index.append(info)
        print(f"Generating CSS for {style} at {dest}, rel: {info['path']}")
        if not dry_run:
            formatter = HtmlFormatter(style=style, linenos=True)
            css = formatter.get_style_defs("#example")
            with open(dest, "w") as dest_fp:
                dest_fp.write(css)
    
    index_location = os.path.join(os.path.abspath(destination_dir), "css")
    index = os.path.join(index_location, "syntax-index.json")
    print(f"Generating JSON CSS file index at {index}")
    if not dry_run:
        with open(index, "w") as index_fp:
            json.dump(style_index, index_fp, indent="\t")

def process_file(source_path, destination_dir, dry_run=False):
    
    filename = os.path.basename(source_path)
    base, ext = os.path.splitext(filename)
    
    source_dest = os.path.join(destination_dir, filename)
    highlight_dest = os.path.join(destination_dir, f"{filename}.html")
    
    if ext == ".py":
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(linenos=True)
    elif ext == ".pycon":
        lexer = get_lexer_by_name("pycon")
        formatter = HtmlFormatter(linenos=False)
    else:
        raise UnknownExtension(f"Unknown extension: {ext}")
    
    print(f"Copying source file from {source_path} to {source_dest}")
    if not dry_run:
        shutil.copy(source_path, source_dest)
        
    relative_source = os.path.relpath(source_dest, destination_dir)
    relative_highlight = os.path.relpath(highlight_dest, destination_dir)
    title = base
    with open(source_path, "r", encoding='utf-8') as fp:
        # strip the BOM if present
        first_line = fp.readline().strip("\ufeff")
        code = fp.read()
        
        if first_line.startswith("#"):
            title = first_line[1:]
        else:
            code = first_line+code
        
        print(f"Writing highlighted source in {highlight_dest}")
        if not dry_run:
            with open(highlight_dest, "w") as highlight_fp:
                highlight(code, lexer, formatter, outfile=highlight_fp)
    
    return relative_source, relative_highlight, title

def directory(value):
    """
    Simple "type" function for argparse that expands a path and makes sure it's
    a directory.
    """
    value = os.path.expanduser(os.path.abspath(value))
    if not os.path.isdir(value):
        parser.error(f"{value} is not a directory")
    
    return value

parser = argparse.ArgumentParser(description='Process code samples into HTML for viewing')

parser.add_argument('source', 
    type=directory, 
    help='Path to look for source files.')

parser.add_argument('--outdir',
    "-o",
    type=directory,
    default="./code",
    help='Destination directory.')

parser.add_argument("--dry-run",
    "-n",
    action="store_true",
    help="Enable 'dry run' mode - only print what we'd be doing instead of manipulating any files")
    
if __name__ == "__main__":
    args = parser.parse_args()
    
    print(f"Removing all contents from directory {args.outdir}")
    if not args.dry_run:
        shutil.rmtree(args.outdir)
    else:
        print(f"DRY RUN: not removing {args.outdir}")
        
    try:
        os.makedirs(args.outdir)
    except OSError:
        print(f"WARNING: source directory {args.outdir} already exists")
    
    index = []
    
    for filename in os.listdir(args.source):
        filepath = os.path.join(args.source, filename)
        try:
            source_link, highlight_link, title = process_file(filepath, args.outdir, args.dry_run)
            
            index.append({
               'source': source_link,
               'highlight': highlight_link,
               'title': title
            })
            
        except UnknownExtension as e:
            print(f"WARNING: {e}")
            
    with open("./code_index_template.html") as fp:
        soup = BeautifulSoup(fp)
        
        dl = soup.find("dl")
        dl.clear()
        
        for entry in index:
            dt = soup.new_tag("dt")
            dt.append(entry["title"])
            dd = soup.new_tag("dd")
            a = soup.new_tag("a", href="code/"+entry["highlight"])
            a.append("code/"+entry["source"])
            
            dd.append(a)
            
            dl.append(dt)
            dl.append(dd)
        
        index_path = os.path.join(args.outdir, "index.html")
        
        print(f"Writing index file {index_path}")
        if not args.dry_run:
            with open(index_path, "w") as index_fp:
                index_fp.write(soup.prettify())