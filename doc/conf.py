# -*- coding: utf-8 -*-
#
# islpy documentation build configuration file, created by
# sphinx-quickstart on Sun Jul 10 16:41:50 2011.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

#import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = "1.0"

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named "sphinx.ext.*") or your custom ones.
extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.intersphinx",
        "sphinx.ext.imgmath",
        "sphinx_copybutton",
        ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
#source_encoding = "utf-8-sig"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"islpy"
copyright = u"2011-16, Andreas Kloeckner"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
ver_dic = {}
with open("../islpy/version.py") as vfile:
    exec(compile(vfile.read(), "../islpy/version.py", "exec"), ver_dic)

version = ".".join(str(x) for x in ver_dic["VERSION"])
# The full version, including alpha/beta/rc tags.
release = ver_dic["VERSION_TEXT"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

html_theme = "furo"

html_theme_options = {
        }


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
        "https://docs.python.org/3/": None,
        }


# mostly a no-op on the pybind parts for now:
# https://github.com/pybind/pybind11/issues/945
autodoc_typehints = "description"


def autodoc_process_signature(app, what, name, obj, options, signature,
        return_annotation):
    from inspect import ismethod
    if ismethod(obj) and obj.__doc__:
        import re
        pattern = r"^[ \n]*%s(\([a-z_0-9, ]+\))" % re.escape(obj.__name__)
        func_match = re.match(pattern, obj.__doc__)

        if func_match is not None:
            signature = func_match.group(1)
        elif obj.__name__ == "is_valid":
            signature = "()"

    return (signature, return_annotation)


def autodoc_process_docstring(app, what, name, obj, options, lines):
    # clear out redundant pybind-generated member list
    if any("Members" in ln for ln in lines):
        del lines[:]

    from inspect import isclass, isroutine
    UNDERSCORE_WHITELIST = ["__len__", "__hash__", "__eq__", "__ne__"]  # noqa: N806
    if isclass(obj) and obj.__name__[0].isupper():
        methods = [nm for nm in dir(obj)
                if isroutine(getattr(obj, nm))
                and (not nm.startswith("_") or nm in UNDERSCORE_WHITELIST)]

        def gen_method_string(meth):
            result = ":meth:`%s`" % meth
            if getattr(obj, "_" + meth + "_is_static", False):
                result += " (static)"

            return result

        if methods:
            lines[:] = [".. hlist::", "  :columns: 3", ""] + [
                    "  * "+gen_method_string(meth)
                    for meth in methods] + lines

            for nm in methods:
                underscore_autodoc = []
                if nm in UNDERSCORE_WHITELIST:
                    underscore_autodoc.append(".. automethod:: %s" % nm)

                if underscore_autodoc:
                    lines.append("")
                    lines.extend(underscore_autodoc)


def setup(app):
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-process-signature", autodoc_process_signature)
