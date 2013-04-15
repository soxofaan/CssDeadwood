
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
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p']))

        selectors = set(['div'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set([]))

        selectors = set(['p', 'div'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p']))


    def testPseudoClasses(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['a', 'p:hover', 'h4:hover'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['a', 'p:hover']))

        selectors = set(['a:focus', 'a:visited'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['a:visited', 'a:focus']))


    def testPseudoChildSelectors(self):
        html = '<html><head></head><body><ol><li>one</li></ol><ul></ul></body></html>'

        selectors = set(['ol li:first-child'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['ol li:first-child']))

        selectors = set(['ul li:first-child'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set())


    def testDirectChilds(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['p > a', 'p a'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p > a', 'p a']))

        selectors = set(['p>a', 'p a'])
        result = cssdeadwood.match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p>a', 'p a']))


