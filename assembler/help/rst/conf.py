project = u'The Book Assembler'
copyright = u'2021, Kiryha Krysko'
author = u'Kiryha Krysko'

version = u'2.0'
release = u'2.0'


extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']
pygments_style = None


import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

chtml_static_path = ['_static']
htmlhelp_basename = 'Assemblerdoc'

latex_elements = {}

latex_documents = [(master_doc, 'Assembler.tex', u'Assembler Documentation', u'Kiryha Krysko', 'manual'), ]
man_pages = [(master_doc, 'assembler', u'Assembler Documentation', [author], 1)]
texinfo_documents = [(master_doc, 'Assembler', u'Assembler Documentation', author,
                      'Assembler', 'One line description of project.', 'Miscellaneous'), ]
epub_title = project
epub_exclude_files = ['search.html']
