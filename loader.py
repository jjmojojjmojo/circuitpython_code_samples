"""
Code Loader Script.

Given the index number, gets the code from the source directory 
and copies it to /Volumes/CIRCUITPY/code.py
"""
import argparse
import os
import glob
import shutil

def directory(value):
    """
    Simple "type" function for argparse that expands a path and makes sure it's
    a directory.
    """
    value = os.path.expanduser(os.path.abspath(value))
    if not os.path.isdir(value):
        parser.error(f"{value} is not a directory")
    
    return value

parser = argparse.ArgumentParser(description='Load code samples onto a CircuitPython board.')

parser.add_argument('--source',
    default="./code",
    type=directory, 
    help='Path to look for source files.')

parser.add_argument('index',
    type=int,
    help="File index number to load")
    
parser.add_argument('--outdir',
    "-o",
    type=directory,
    default="/Volumes/CIRCUITPY",
    help='Destination directory.')

parser.add_argument("--dry-run",
    "-n",
    action="store_true",
    help="Enable 'dry run' mode - only print what we'd be doing instead of manipulating any files")
    
args = parser.parse_args()

sourcefile = glob.glob(f"{args.source}/{args.index:03}*.py")[0]
destfile = os.path.join(args.outdir, "code.py")

if not args.dry_run:
    with open(destfile, "w") as dest_fp:
        with open(sourcefile, "r") as source_fp:
            for line in source_fp:
                dest_fp.write(line.strip("\ufeff"))
else:
    print(f"DRY RUN: would have copied {sourcefile} to {destfile}")