==================
Code Sample Viewer
==================

This is a site for displaying code samples associated with a presentation, "State And Events In CircuitPython" originally presented to the `Triangle Python User Group <http://trizpug.org/>`__ on 11/29/2018.

The idea was to provide a way to show code samples without resorting to screen grabs or trying to get Powerpoint/LibreOffice Impress to display code properly in a slide.

By hosting the code samples in a viewer like this, the presenter can provide a link that any person in attendance can visit to follow along on their laptop (it might also work on a tablet but this hasn't been tested yet). By separating the samples from the presentation content, the user is free to set the font size and color scheme to their comfort. They can also copy/paste the code easily to try it out.

Extra Files
===========
This directory contains the HTML, CSS and Javascript that runs the code viewer, as well as the code used to generate the code examples.

There are two other odd files here that should be explained:

:code:`Tripython Presentation 11-15-2018.pdf`
    This file is the presentation that prompted this project, as a PDF. Note that the links to the live code samples viewer don't work in most PDF viewers.
    
:code:`loader.py`
    This file copies one of the code examples, identified by number, to a CircuitPython development board. It was used by the author to demonstrate the code during the presentation.

Setup
=====
This directory is intended to be used as a python virtual environment::
    
    $ python -m venv .
    
It can be initialized with the :code:`activate` script::
    
    $ source bin/activate
    
Once the environment is activated, to install necessary packages, use :code:`pip` and the provided :code:`requirements.txt`::
    
    $ pip install -r requirements.txt
    

Build
=====
The :code:`process.py` script will scan a given directory for :code:`*.py` files (or :code:`*.pycon` files, that represent a python interactive shell session), and create a series of tokenized HTML files using pygments in the :code:`code` directory.

An :code:`index.html` file is created for use by the browser interface to load the list of files.

:code:`process.py` takes the first line of the each file and uses it as the title for the code example (unless the first line is not a *hash-style* comment), and strips it from the output.

Usage::
    
    $ python process.py --help
    usage: process.py [-h] [--outdir OUTDIR] [--dry-run] source
    
    Process code samples into HTML for viewing
    
    positional arguments:
      source                Path to look for source files.
    
    optional arguments:
      -h, --help            show this help message and exit
      --outdir OUTDIR, -o OUTDIR
                            Destination directory.
      --dry-run, -n         Enable 'dry run' mode - only print what we'd be doing
                            instead of manipulating any files
                            

Please consult :code:`process.py --help` for the latest usage!

Generating CSS
--------------
:code:`process.py` has a function, :code:`generate_css()` that will generate CSS files for all known pygments themes, and an :code:`index.json` file for use by the browser UI.

To use, run the function from a python prompt::
    
    >>> from process import generate_css
    >>> generate_css()
    
You may want to pass :code:`dry_run=True` to the function the first time its run.

Preview
=======
Any web server can be used to serve this directory, but the author has provided a simple WSGI app that will serve the files, and the gunicorn web server in :code:`requirements.txt`.

To use, activate the environment, and run::
    
    $ gunicorn -w 4 wsgi:app
    
You can then view the site at http://127.0.0.1:8000

TODO
====
* Let users select a pygments theme. **DONE**.
* Generiscize for future presentations.
* Add CSS generation as a CLI option to :code:`process.py`.
* Provide more detail and descriptive text for each sample, beyond just the title.