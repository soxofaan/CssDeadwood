#!/usr/bin/env python

'''
Script to search for ids and classes from CSS selectors
in source files (templates, JavaScript files, PHP files, ...)
and report classes or ids that could not be found as a word.

Usage:
    run with file names or directories to scan recursively.

CSS files will be used as source of classes and ids.
The other files will be used to scann through for these classes and ids as words.

'''



import sys
import os
import re
import collections
import operator
import logging
import optparse
import json

import cssutils

_log = logging.getLogger()



def collect_files(seeds, extensions=None):
    '''
    Collect files under given root folders or files
    @param seeds list of root folders or files
    @param extensions optional list of file extensions (lowercase) to filter files
    '''
    files = set()

    # Local function to check extensions (or except everything)
    if extensions != None:
        check_extension = lambda path: os.path.splitext(path)[1].lower() in extensions
    else:
        check_extension = lambda path: True

    for seed in seeds:
        if os.path.isfile(seed) and check_extension(seed):
            files.add(seed)
        elif os.path.isdir(seed):
            for (dirpath, dirnames, filenames) in os.walk(seed):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    if check_extension(path):
                        files.add(path)
    return files


def extract_css_selectors(css_file):
    '''
    Extract CSS selectors from a given CSS file.

    @return set of CSS selectors
    '''
    selectors = set()
    stylesheet = cssutils.parseFile(css_file)
    for rule in stylesheet.cssRules:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            selectors.update([s.selectorText for s in rule.selectorList])
    return selectors


def file_get_contents(file_name):
    with open(file_name) as f:
        contents = f.read()
    return contents


def get_occuring_words(words, content):
    '''
    Return the words occuring in content.
    '''
    found = set()
    for word in words:
        if re.search(r'\b%s\b' % word, content):
            found.add(word)
    return found


def main():

    # Parse command line
    option_parser = optparse.OptionParser(usage='%prog [options]')

    option_parser.add_option("--htmlexport", metavar='FILE',
                  action="store", dest="html_export", default=None,
                  help="Export result to a HTML report (requires jinja2 library).")
    option_parser.add_option("--jsonexport", metavar='FILE',
                  action="store", dest="json_export", default=None,
                  help="Export analysis results in JSON format.")

    option_parser.add_option("-v", "--verbose",
                  action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO,
                  help="Be more verbose")

    options, args = option_parser.parse_args()


    # Set up logging
    logging.basicConfig(level=options.loglevel)

    # Get CSS files and other source files
    css_files = collect_files(args, extensions=['.css'])
    src_files = collect_files(args, extensions=['.tpl', '.php', '.js'])
    _log.info('Using CSS from %d CSS files.' % len(css_files))
    _log.debug('CSS files: %r.' % css_files)
    _log.info('Scanning in %d source files.' % len(src_files))
    _log.debug('Source files: %r.' % src_files)

    # Some precompiled regexes.
    class_regex = re.compile(r'\.([a-zA-Z0-9]+)')
    id_regex = re.compile(r'\#([a-zA-Z0-9]+)')

    # Cache findable ids and classes accross analysis of several CSS files.
    findable_ids = set()
    findable_classes = set()

    # Result object (to be used in reporting/exporting)
    results = {}

    for css_file in css_files:
        _log.info('Analysing ids and classes from %r' % css_file)
        results[css_file] = {}

        selectors = extract_css_selectors(css_file)
        results[css_file]['selectors'] = selectors
        _log.info('Extracted %d CSS selectors from %r.' % (len(selectors), css_file))
        _log.debug('Extracted selectors: %r' % selectors)

        # Extract classes and ids
        classes = set()
        ids = set()
        for selector in selectors:
            classes.update(class_regex.findall(selector))
            ids.update(id_regex.findall(selector))
        results[css_file]['ids'] = ids
        results[css_file]['classes'] = classes
        _log.info('Extracted %d classes.' % len(classes))
        _log.debug('Extracted classes: %r' % classes)
        _log.info('Extracted %d ids.' % len(ids))
        _log.debug('Extracted ids: %r' % ids)

        # Determine unfindable ids and classes.
        # Start with eliminating ids ans classes we already found previously.
        unfindable_ids = ids.difference(findable_ids)
        unfindable_classes = classes.difference(findable_classes)

        # Scan through the source files for the remaining ids and classes.
        for src_file in src_files:
            content = file_get_contents(src_file)

            _log.debug('Searching for %d remaining unfindable ids in %s' % (len(unfindable_ids), src_file))
            findable_ids.update(get_occuring_words(unfindable_ids, content))
            unfindable_ids.difference_update(findable_ids)

            _log.debug('Searching for %d remaining unfindable classes in %s' % (len(unfindable_ids), src_file))
            findable_classes.update(get_occuring_words(unfindable_classes, content))
            unfindable_classes.difference_update(findable_classes)

        results[css_file]['unfindable_ids'] = unfindable_ids
        results[css_file]['unfindable_classes'] = unfindable_classes


        # Report unfindable classes and ids
        if ids:
            print 'Unfindable ids as words: %d from %d (%.2f%%)' % (len(unfindable_ids), len(ids), 100.0 * len(unfindable_ids) / len(ids))
            for id in unfindable_ids:
                print '#' + id,
            print
        if classes:
            print 'Unfindable classes as words: %d from %d (%.2f%%)' % (len(unfindable_classes), len(classes), 100.0 * len(unfindable_classes) / len(classes))
            for classs in unfindable_classes:
                print '.' + classs,
            print

    # JSON report
    if options.json_export:
        logging.info('Writing JSON report: %s' % options.json_export)
        with open(options.json_export, 'w') as f:
            json.dump(results, f, indent=1, default=list)


if __name__ == '__main__':
    main()
