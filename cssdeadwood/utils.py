
import os
import re


def collect_files(seeds, extensions=None):
    '''
    Collect files from given seeds: files or folders to scan through recursively.

    @param seeds list of root folders or files
    @param extensions optional list of file extensions (lowercase) to filter files
    '''
    files = set()

    # Local function to check extensions (or accept everything)
    if extensions is not None:
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



def file_get_contents(file_name):
    with open(file_name) as f:
        contents = f.read()
    return contents





def get_occuring_words(words, content):
    '''
    Return the subset of given words that occur in content.
    '''
    found = set()
    for word in words:
        if re.search(r'\b%s\b' % word, content):
            found.add(word)
    return found

