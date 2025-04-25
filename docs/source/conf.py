# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
project = "EvoSim"
copyright = "2025, Jason Zhao"
author = "Jason Zhao"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Extention configs -------------------------------------------------------

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- HTML output options -----------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]


html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#cc99ff",
        "color-brand-content": "#ffcccc",
        "color-admonition-background": "#333366",
    },
    "dark_css_variables": {
        "color-brand-primary": "#cc99ff",
        "color-brand-content": "#666666",
        "color-admonition-background": "#FFFFFF",
    },
}

pygments_style = "catppuccin-mocha"
pygments_dark_style = "catppuccin-mocha"
