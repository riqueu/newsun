# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../tests'))

project = 'NEWSUN'
copyright = "2024, Artur V. Krause, Bruno L. Z. Rosa, Gustavo de O. da Silva, Gustavo L. dos Santos, Henrique C. Beltrão'"
author = "Artur V. Krause, Bruno L. Z. Rosa, Gustavo de O. da Silva, Gustavo L. dos Santos, Henrique C. Beltrão'"
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.githubpages"]

master_doc = "index"

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    "sidebar_width": "300px"
    }
html_sidebars = {
   '**': ['globaltoc.html', 'sourcelink.html'],
}