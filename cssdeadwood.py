
import sys
import re
import collections
import operator
import logging

import bs4
import cssutils



def main():

    logging.basicConfig(level=logging.INFO)

    css_file = sys.argv[1]
    html_files = sys.argv[2:]

    # Read the CSS file and extract the selectors.
    selectors = set()
    cssutils.log.setLevel(logging.ERROR)
    stylesheet = cssutils.parseFile(css_file)
    for rule in stylesheet.cssRules:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            selectors.update([s.selectorText for s in rule.selectorList])

    logging.info('Collected %d selectors' % len(selectors))

    # Parse html files, try selectors and build usage histogram.
    selector_histogram = collections.defaultdict(lambda: 0)
    logging.info('Trying selectors on %d HTML pages' % len(html_files))
    for html_file in html_files:
        logging.info('Trying selectors on %r' % html_file)
        with open(html_file) as f:
            soup = bs4.BeautifulSoup(f)

        for selector in selectors:
            logging.debug('Trying selector %r' % selector)
            try:
                hits = soup.select(selector)
                selector_histogram[selector] += len(hits)
            except Exception, e:
                logging.exception(e)


    # Report selectors with usage count.
    selector_report = [(count, selector) for (selector, count) in selector_histogram.items()]
    selector_report.sort()
    for count, selector in selector_report:
        print '%10d %s' % (count, selector)

    selectors_total = len(selector_histogram)
    selectors_unused = len([selector for selector, count in selector_histogram.items() if count == 0])

    print '%d unused selectors from %d: %.2f%%' % (selectors_unused, selectors_total, 100.0 * selectors_unused / selectors_total)



if __name__ == '__main__':
    main()
