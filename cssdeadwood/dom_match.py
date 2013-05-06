
import logging

import lxml
import lxml.etree
import lxml.cssselect
import cssselect


# Global logging object
_log = logging.getLogger('cssdeadwood.dom_match')




class CssDeadwoodHtmlTranslator(cssselect.HTMLTranslator):
    '''
    Simple extension of cssselect.HTMLTranslator to make sure that
    pseudo classes like :hover, :focus, :visited, etc always match,
    which is what we want in a dead code detection app.
    '''

    def pseudo_always_matches(self, xpath):
        """Common implementation for pseudo-classes that alwyas match."""
        return xpath

    xpath_link_pseudo = pseudo_always_matches
    xpath_visited_pseudo = pseudo_always_matches
    xpath_hover_pseudo = pseudo_always_matches
    xpath_active_pseudo = pseudo_always_matches
    xpath_focus_pseudo = pseudo_always_matches
    xpath_target_pseudo = pseudo_always_matches
    xpath_enabled_pseudo = pseudo_always_matches
    xpath_disabled_pseudo = pseudo_always_matches
    xpath_checked_pseudo = pseudo_always_matches


def match_selectors_against_html_root_element(selectors, html_element):
    '''
    Find the selectors that match with the DOM from the given HTML.

    @param selectors set of CSS selectors (strings)
    @param html_element lxml.etree.Element object

    @return set of found selectors
    '''
    found_selectors = set()
    css_to_xpath_translator = CssDeadwoodHtmlTranslator()
    for selector_str in selectors:
        try:
            # Instead of just calling css_to_xpath(selector_str),
            # we first convert the css selector string to a cssselect.Selector instance
            # to pass to selector_to_xpath(), so we can properly ignore pseudo elements.
            # Note that cssselect.parse() always returns a list, so we do a for loop.
            for selector in cssselect.parse(selector_str):
                selector.pseudo_element = None
                xpath_expr = css_to_xpath_translator.selector_to_xpath(selector)
                if len(html_element.xpath(xpath_expr)) > 0:
                    found_selectors.add(selector_str)
        except Exception:
            global _log
            _log.exception('lxml css select failed on selector %r' % selector_str)
    return found_selectors


def match_selectors_against_html_string(selectors, html_string):
    '''
    Find the selectors that match with the DOM from the given HTML.

    @param selectors set of CSS selectors (strings)
    @param html_string html string

    @return set of found selectors
    '''
    parser = lxml.etree.HTMLParser()
    html_element = lxml.etree.fromstring(html_string, parser=parser)
    return match_selectors_against_html_root_element(selectors, html_element)


def match_selectors_against_html_resource(selectors, html_resource):
    '''
    Find the selectors that match with the DOM from the given HTML.

    @param selectors set of CSS selectors (strings)
    @param html_resource HTML file path/url or file(-like) object.

    @return set of found selectors
    '''
    parser = lxml.etree.HTMLParser()
    html_element = lxml.etree.parse(html_resource, parser=parser).getroot()
    return match_selectors_against_html_root_element(selectors, html_element)

