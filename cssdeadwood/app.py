#!/usr/bin/env python


import sys
import logging
import optparse
import json

import lxml
import lxml.etree
import lxml.cssselect
import cssselect

from cssdeadwood.utils import collect_files, file_get_contents, get_occuring_words
from cssdeadwood.css_extract import extract_css_selectors, extract_ids_and_classes_from_selectors
from cssdeadwood.dom_match import match_selectors_against_html_resource


# TODO: instead of used vs not used, provide histogram analysis to have better view on hot vs not hot
# TODO: source id/class based elimination: only do search on strings, not logic
# TODO: operation mode to only provide HTML files
# TODO: operation mode to only provide urls
# TODO: HTML format reporting


_log = logging.getLogger('cssdeadwood')





class CssDeadwoodApp(object):
    '''
    CSS Deadwood main() function,
    written OOP-style and chopped up in small methods, for better testability.
    '''


    def _eliminate_selectors_from_dom_matching(self, selectors, html_files):
        # The results struct for tracking intermediate data
        results = {}

        # Start with flagging all selectors as "unused"
        unused_selectors = selectors.copy()
        for html_file in html_files:
            original_total = len(unused_selectors)
            _log.debug('DOM matching %d CSS selectors with DOM from %r' % (original_total, html_file))
            found_selectors = match_selectors_against_html_resource(unused_selectors, html_file)
            unused_selectors.difference_update(found_selectors)
            _log.info('DOM matching %d CSS selectors: %d matches, %d unmatched with DOM from %r' % (original_total, len(found_selectors), len(unused_selectors), html_file))

        # Return result
        results['unused_selectors'] = sorted(unused_selectors)

        return unused_selectors, results

    def _eliminate_selectors_from_idclass_grepping(self, selectors, src_files):
        '''
        Eliminate selectors by searching for mentioned ids and classes in the given source files.
        '''
        # The results struct for tracking intermediate data
        results = {}

        # Extract ids and classes.
        ids, classes, origins = extract_ids_and_classes_from_selectors(selectors)
        results['ids'] = ids
        results['classes'] = classes
        _log.info('Id/class extraction from %d CSS selectors for source code matching: extracted %d ids, %d classes.' % (len(selectors), len(ids), len(classes)))
        _log.debug('Extracted ids: %r' % ids)
        _log.debug('Extracted classes: %r' % classes)

        # Determine unfindable ids and classes.
        findable_ids = set()
        findable_classes = set()
        unfindable_ids = ids.copy()
        unfindable_classes = classes.copy()
        # Scan through the source files for the remaining ids and classes.
        for src_file in src_files:
            content = file_get_contents(src_file)
            _log.debug('Searching for %d remaining unfindable ids in %s' % (len(unfindable_ids), src_file))
            findable_ids.update(get_occuring_words(unfindable_ids, content))
            unfindable_ids.difference_update(findable_ids)
            _log.debug('Searching for %d remaining unfindable classes in %s' % (len(unfindable_classes), src_file))
            findable_classes.update(get_occuring_words(unfindable_classes, content))
            unfindable_classes.difference_update(findable_classes)
        results['unfindable_ids'] = unfindable_ids
        results['unfindable_classes'] = unfindable_classes

        # Eliminate selectors with findable ids/classes
        used_idclass_selectors = set()
        for id in findable_ids:
            used_idclass_selectors.update(origins['#' + id])
        for classs in findable_classes:
            used_idclass_selectors.update(origins['.' + classs])
        unused_selectors = selectors.difference(used_idclass_selectors)
        _log.info('Id/class based elimination from {total:d} CSS selectors with {src:d} source files: {used:d} possibly used, {unused:d} unused.'.format(
            total=len(selectors),
            src=len(src_files),
            used=len(used_idclass_selectors),
            unused=len(unused_selectors)
        ))

        # return result
        results['unused_selectors'] = sorted(unused_selectors)

        return unused_selectors, results


    def main(self, argv=sys.argv):

        # Parse command line
        option_parser = optparse.OptionParser(usage='%prog [options] [cssfiles] [htmlfiles] [srcsfiles]')

        default_src_extensions = '.php,.py,.rb,.js'
        option_parser.add_option("-e", "--srcext", metavar='EXT',
                      action="store", dest="src_extensions", default=default_src_extensions,
                      help="Define the source file extensions (comma separated) to filter on when recursively scanning source folders. Default: '%s'." % default_src_extensions)

        option_parser.add_option("--htmlexport", metavar='FILE',
                      action="store", dest="html_export", default=None,
                      help="Export result to a HTML report (requires jinja2 library).")
        option_parser.add_option("--jsonexport", metavar='FILE',
                      action="store", dest="json_export", default=None,
                      help="Export analysis results in JSON format.")

        option_parser.add_option("-v", "--verbose",
                      action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO,
                      help="Be more verbose")

        options, args = option_parser.parse_args(args=argv[1:])

        # Set up logging
        logging.basicConfig(level=options.loglevel)
        logging.getLogger('CssDeadwood.bs4').setLevel(logging.ERROR)

        # Get CSS, HTML and other source files form given arguments.
        css_files = collect_files(args, extensions=['.css'])
        html_files = collect_files(args, extensions=['.html'])
        if len(options.src_extensions.strip()) > 0:
            src_extensions = options.src_extensions.split(',')
        else:
            src_extensions = []
        src_files = collect_files(args, extensions=src_extensions)
        _log.info('Working with %d CSS files.' % len(css_files))
        _log.debug('CSS files: %r.' % css_files)
        _log.info('Working with %d HTML files.' % len(html_files))
        _log.debug('HTML files: %r.' % html_files)
        _log.info('Working with %d source files.' % len(src_files))
        _log.debug('Source files: %r.' % src_files)

        # Result object where we will store all analysis data, to be used in reporting/exporting.
        results = {}

        for css_file in css_files:
            _log.info('Analysing CSS selectors from %r' % css_file)
            results[css_file] = {}

            # Extract selectore from CSS source
            selectors = extract_css_selectors(css_file)
            results[css_file]['selectors'] = selectors
            _log.info('Extracted %d CSS selectors from %r.' % (len(selectors), css_file))
            _log.debug('Extracted selectors: %r' % selectors)

            # Start with flagging all selectors as "unused"
            unused_selectors = selectors.copy()

            # Eliminate selectors that match with the DOM trees from the HTML files.
            if html_files:
                unused_selectors, data = self._eliminate_selectors_from_dom_matching(unused_selectors, html_files)
                results[css_file]['dom_matching'] = data

            # Extract ids and classes and scan other source files for these.
            if src_files:
                unused_selectors, data = self._eliminate_selectors_from_idclass_grepping(unused_selectors, src_files)
                results[css_file]['idclass_elimination'] = data

            results[css_file]['unused_selectors'] = sorted(unused_selectors)

        # Report
        for css_file, data in results.items():
            print (css_file + ' ').ljust(80, '-')
            total_count = len(data['selectors'])
            if total_count == 0:
                print 'No selectors'
                continue
            unused_count = len(data['unused_selectors'])
            perc = 100.0 * unused_count / total_count
            print 'Could not determine usage of the following %d CSS selectors (from %d in total: %.2f%%):' % (unused_count, total_count, perc)
            print '\n'.join(data['unused_selectors'])

        # TODO: HTML report

        # JSON report
        if options.json_export:
            logging.info('Writing JSON report: %s' % options.json_export)
            with open(options.json_export, 'w') as f:
                json.dump(results, f, indent=1, default=list)



def main():
    CssDeadwoodApp().main(sys.argv)

