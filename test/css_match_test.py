
import os
import sys
import tempfile
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import cssdeadwood


class CssMatchTest(unittest.TestCase):


    def testSimple(self):
        html = '<html><head></head><body><p>hello world</p></body></html>'

        selectors = set(['p'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set(['p']))

        selectors = set(['div'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set([]))

        selectors = set(['p', 'div'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set(['p']))


    def testHoverPseudoClasses(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['a', 'a:hover'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set(['a', 'a:hover']))

    def testDirectChilds(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['p > a', 'p a'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set(['p > a', 'p a']))

        selectors = set(['p>a', 'p a'])
        result = cssdeadwood.match_selectors_against_html(selectors, html)
        self.assertEqual(result, set(['p>a', 'p a']))
