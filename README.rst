
CSS Deadwood
============


CSS Deadwood is a tool to search for unused CSS selectors
by scanning given CSS files for CSS selectors and matching these against
HTML files (and optionally PHP/Python/Ruby/templates source code).


Installation
------------

The easiest way to install CSS Deadwood is with pip::

    pip install cssdeadwood

or easy_install::

    easy_install cssdeadwood

These will install (among others) the ``cssdeadwood`` script in a ``bin``
folder corresponding with the used installation procedure.

Note that CSS Deadwood depends on `lxml <http://lxml.de/>`_, which may take a while to
install/compile if it is not available on your system already.

Development
~~~~~~~~~~~

Or, if you want to go for the development version, clone CSS Deadwood from
https://github.com/soxofaan/CssDeadwood/



Usage
-----

Basic usage of the ``cssdeadwood`` tool is pretty simple:
just provide pass it one or more CSS files and
one or more HTML files and let it do its job::

	cssdeadwood style.css index.html

For example, CSS Deadwood comes with a demo mode::

	cssdeadwood --example

	--------------------------------------------------------------------------------
	Running CSS Deadwood in example mode with following CSS and HTML file as input:
	/path/to/cssdeadwood/test/files/css/css001.css
	/path/to/cssdeadwood/test/files/html/html001.html
	--------------------------------------------------------------------------------

	INFO:cssdeadwood:Working with 1 CSS files.
	INFO:cssdeadwood:Working with 1 HTML files.
	INFO:cssdeadwood:Working with 0 source files.
	INFO:cssdeadwood:Analysing CSS selectors from '/path/to/cssdeadwood/test/files/css/css001.css'
	INFO:cssdeadwood:Extracted 5 CSS selectors from '/path/to/cssdeadwood/test/files/css/css001.css'.
	INFO:cssdeadwood:DOM matching 5 CSS selectors: 3 matches, 2 unmatched with DOM from '/path/to/cssdeadwood/test/files/html/html001.html'
	/path/to/cssdeadwood/test/files/css/css001.css
	Could not determine usage of the following 2 CSS selectors (from 5 in total: 40.0%):
	#content div.ad
	a.premium


