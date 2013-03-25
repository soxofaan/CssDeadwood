
import os
import sys
import tempfile
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import cssdeadwood


class CssExtractTest(unittest.TestCase):

    def setUp(self):
        self.cssfile = tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False)

    def tearDown(self):
        os.unlink(self.cssfile.name)

    def assertSelectorExtraction(self, css_data, selectors):
        self.cssfile.write(css_data)
        self.cssfile.close()
        extracted = cssdeadwood.extract_css_selectors(self.cssfile.name)
        self.assertEqual(extracted, selectors)


    def test_simple001(self):
        self.assertSelectorExtraction('''
            p { color: red; }
            div#content h1 { font-size: 10pt;}
            ''',
            set(['p', 'div#content h1'])
        )

    def test_simple002(self):
        self.assertSelectorExtraction('''
            p.red { color: red; }
            div#content h1 { font-size: 10pt;}
            ''',
            set(['p.red', 'div#content h1'])
        )

    def test_simple003(self):
        self.assertSelectorExtraction('''
            p { color: red; }
            div.content h1 { font-size: 10pt;}
            ''',
            set(['p', 'div.content h1'])
        )

    def test_asterisk001(self):
        self.assertSelectorExtraction('''
            * { color: red; }
            h1 { font-size: 10pt;}
            ''',
            set(['*', 'h1'])
        )

    def test_asterisk002(self):
        self.assertSelectorExtraction('''
            *  p{ color: red; }
            h1 { font-size: 10pt;}
            ''',
            set(['* p', 'h1'])
        )

    def test_comma001(self):
        self.assertSelectorExtraction('''
            p, div.red { color: red; }
            div#content h1 { font-size: 10pt;}
            ''',
            set(['p', 'div.red', 'div#content h1'])
        )

    def test_whitespace001(self):
        self.assertSelectorExtraction('''
            p   \n      a, 
                div   \t span.red { color: red; }
            div#content
              h1 { font-size: 10pt;}
            ''',
            set(['p a', 'div span.red', 'div#content h1'])
        )

    def test_whitespace001(self):
        self.assertSelectorExtraction('''
            p>a,div span.red{color:red;}div#content h1{font-size:10pt;}.yellow{color:yellow}
            ''',
            set(['p>a', 'div span.red', 'div#content h1', '.yellow'])
        )

    def test_newlines001(self):
        self.assertSelectorExtraction('''
            p, 
            div.red
            { color: red; }
            div#content 
            h1
            { font-size: 10pt;}
            ''',
            set(['p', 'div.red', 'div#content h1'])
        )

    def test_comments001(self):
        self.assertSelectorExtraction('''
            p   /* span */     a,  div    span.red { color: red; }
            ''',
            set(['p a', 'div span.red'])
        )
    def test_comments002(self):
        self.assertSelectorExtraction('''
            span.red { color: red; }
            /* 
            span.blue { color: blue }
            */
            span.green { color: green }
            ''',
            set(['span.red', 'span.green'])
        )


    def test_media001(self):
        self.assertSelectorExtraction('''
            p, div.red { color: red; }
            @media screen {
                div#content h1 { font-size: 10pt;}
            }
            ''',
            set(['p', 'div.red', 'div#content h1'])
        )

    def test_media002(self):
        self.assertSelectorExtraction('''
            p, div.red { color: red; }
            @media screen {
                div#content h1 { font-size: 10pt;}
                span.blue { color: blue; }
            }
            ''',
            set(['p', 'div.red', 'div#content h1', 'span.blue'])
        )

    def test_media003(self):
        self.assertSelectorExtraction('''
            p, div.red { color: red; }
            @media screen and (device-width:768px) {
                div#content h1 { font-size: 10pt;}
                span.blue { color: blue; }
            }
            ''',
            set(['p', 'div.red', 'div#content h1', 'span.blue'])
        )

    def test_media004(self):
        self.assertSelectorExtraction('''
            p, div.red { color: red; }
            @media screen {
                div#content h1 { font-size: 10pt;}
                span.blue { color: blue; }
            }
            ''',
            set(['p', 'div.red', 'div#content h1', 'span.blue'])
        )


