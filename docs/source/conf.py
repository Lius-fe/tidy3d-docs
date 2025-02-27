# -- Path setup --------------------------------------------------------------

import os
import re
import codecs
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath("../notebooks"))
sys.path.insert(0, os.path.abspath("../../../tidy3d"))
sys.path.insert(0, os.path.abspath("../../tidy3d"))
sys.path.insert(0, os.path.abspath("../../tidy3d/tidy3d"))
sys.path.insert(0, os.path.abspath("../../tidy3d/tidy3d/components"))
sys.path.insert(0, os.path.abspath("../../tidy3d/tidy3d/web"))
sys.path.insert(0, os.path.abspath("../../tidy3d/tidy3d/plugins"))
# sys.path.insert(0, "../notebooks")
# sys.path.insert(0, "../tidy3d/tidy3d/components")
# sys.path.insert(0, "../tidy3d/tidy3d")
# sys.path.insert(0, "../tidy3d")
sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("./_ext"))

print(sys.path)


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# -- Generate Material Library documentation ---------------------------------

import generate_doc

generate_doc.main()

# -- Project information -----------------------------------------------------

import datetime

project = "Tidy3D"

author = "Flexcompute"

year = datetime.date.today().strftime("%Y")
copyright = f"Flexcompute 2020-{year}"

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx_copybutton",
    "m2r2",
    "sphinx_sitemap",
    "custom_meta"
]

source_suffix = [".rst", ".md"]

autodoc_default_options = {"inherited-members": True, "show-inheritance":True}

autodoc_inherit_docstrings = True
# autosummary_generate = True

# autodoc_pydantic_model_show_json = True
# autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_signature_prefix = "class"
autodoc_pydantic_field_signature_prefix = "attribute"
autodoc_pydantic_model_show_config_member = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_show_field_summary = False
# autodoc_pydantic_model_members = False
# autodoc_pydantic_field_list_validators = False
# autodoc_pydantic_settings_summary_list_order = 'bysource'
# autodoc_pydantic_model_undoc_members = False
# autoclass_content = "class"
extlinks = {}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

autosummary_generate = True
# autodoc_typehints = "none"

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# python prompts for copy / paste.  Ignore `>>>` and `...` stuff so pasted runs in interpreter.
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
# html_theme_path = ["_themes"]
# html_theme = "sphinx_rtd_theme"
# html_theme = "sphinx_book_theme"
# pygments_style = 'monokai-dark'

# import stanford_theme
# html_theme = "stanford_theme"
# html_theme_path = [stanford_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

# html_theme_options = {"logo_only": True}

html_static_path = ["_static"]

html_theme = "sphinx_book_theme"
html_title = "Tidy3D Electromagnetic Solver"
html_logo = "../../tidy3d/img/Tidy3D-logo.svg"
html_favicon = "_static/logo.svg"
html_show_sourcelink = False
html_theme_options = {
    "logo_only": True,
    "path_to_docs": "docs",
    "repository_url": "https://github.com/flexcompute/tidy3d",
    "repository_branch": "main",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org/v2/gh/flexcompute-readthedocs/tidy3d-docs/readthedocs?labpath=docs%2Fsource%2Fnotebooks",
        "notebook_interface": "jupyterlab",
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
}
html_source_suffix = ''

# html_logo = "_static/logo.svg"
# html_favicon = "_static/logo.svg"

html_css_files = ["css/custom.css"]

# sphinx_github_changelog_token = "..."

# def setup(app):
# app.add_css_file("css/custom.css")


# -- Latex fixes? ------------------------------------------

# latex_elements = {
#     'preamble': r'''\renewcommand{\hyperref}[2][]{#2}'''
# }
latex_engine = "xelatex"

# for sphinx-sitemap
html_baseurl = "https://docs.flexcompute.com/projects/tidy3d/en/latest"


# if pandoc isnt working, uncomment below but make sure to not commit the bin/ library
# from inspect import getsourcefile

# # Get path to directory containing this file, conf.py.
# DOCS_DIRECTORY = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

# def ensure_pandoc_installed(_):
#     import pypandoc

#     # Download pandoc if necessary. If pandoc is already installed and on
#     # the PATH, the installed version will be used. Otherwise, we will
#     # download a copy of pandoc into docs/bin/ and add that to our PATH.
#     pandoc_dir = os.path.join(DOCS_DIRECTORY, "bin")
#     # Add dir containing pandoc binary to the PATH environment variable
#     if pandoc_dir not in os.environ["PATH"].split(os.pathsep):
#         os.environ["PATH"] += os.pathsep + pandoc_dir
#     pypandoc.ensure_pandoc_installed(
#         targetfolder=pandoc_dir,
#         delete_installer=True,
#     )


# def setup(app):
#     app.connect("builder-inited", ensure_pandoc_installed)
