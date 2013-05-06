
import re
import collections

from cssdeadwood.utils import file_get_contents



def extract_css_selectors(css_file):
    '''
    Extract CSS selectors from a given CSS file.

    @param css_file CSS file path

    @return set of CSS selectors
    '''
    selectors = set()
    css = file_get_contents(css_file)
    # Precompiled regex to clean up/normalize whitespace
    whitespace_regex = re.compile(r'\s+', flags=re.DOTALL)
    # Remove comments.
    css = re.compile(r'/\*.*?\*/', flags=re.DOTALL).sub('', css)
    # Collect the selectors/selector groups in front of { ... } declaration blocks
    for match in re.compile(r'\s*([^{}]*)\s*{', flags=re.DOTALL).finditer(css):
        selector_part = match.group(1).strip()
        # Ignore at-rules
        if selector_part.startswith('@'):
            continue
        # Split on comma to get selectors.
        for selector_candidate in selector_part.split(','):
            # Clean up/normalize whitespace
            selector_candidate = whitespace_regex.sub(' ', selector_candidate.strip())
            # Store
            selectors.add(selector_candidate)

    return selectors





# Some precompiled regexes to extract ids and clasess from CSS selectors.
REGEX_ID = re.compile(r'\#([a-zA-Z0-9]+)')
REGEX_CLASS = re.compile(r'\.([a-zA-Z0-9]+)')


def extract_ids_and_classes_from_selectors(selectors):
    '''
    Extract ids and classes used in the given CSS selectors.

    @return (ids, classes, origins) with:
        ids: set of extracted ids
        classes: set of extracted classes
        origins: mapping of ids (format '#x') and classes (format '.x')
            to list of selectors they were found in.
    '''
    ids = set()
    classes = set()
    origins = collections.defaultdict(lambda: [])
    for selector in selectors:
        for id in REGEX_ID.findall(selector):
            ids.add(id)
            origins['#' + id].append(selector)
        for classs in REGEX_CLASS.findall(selector):
            classes.add(classs)
            origins['.' + classs].append(selector)
    return (ids, classes, origins)

