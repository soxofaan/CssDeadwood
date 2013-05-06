
import os
import sys
import tempfile
import unittest


from cssdeadwood.dom_match import match_selectors_against_html_string


class CssMatchTest(unittest.TestCase):


    def testSimple(self):
        html = '<html><head></head><body><p>hello world</p></body></html>'

        selectors = set(['p'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p']))

        selectors = set(['div'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set([]))

        selectors = set(['p', 'div'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p']))


    def testPseudoClasses(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['a', 'p:hover', 'h4:hover'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['a', 'p:hover']))

        selectors = set(['a:focus', 'a:visited'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['a:visited', 'a:focus']))


    def testPseudoChildSelectors(self):
        html = '<html><head></head><body><ol><li>one</li></ol><ul></ul></body></html>'

        selectors = set(['ol li:first-child'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['ol li:first-child']))

        selectors = set(['ul li:first-child'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set())


    def testDirectChilds(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['p > a', 'p a'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p > a', 'p a']))

        selectors = set(['p>a', 'p a'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p>a', 'p a']))


    def testPseudoElements(self):
        html = '<html><head></head><body><p>hello <a href="/world">world</a></p></body></html>'

        selectors = set(['p:before'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p:before']))

        selectors = set(['p:after'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p:after']))

        selectors = set(['p:first-line'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p:first-line']))

        selectors = set(['p:first-letter'])
        result = match_selectors_against_html_string(selectors, html)
        self.assertEqual(result, set(['p:first-letter']))



