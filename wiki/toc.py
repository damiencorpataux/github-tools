"""This module is useful for managing markdown pages table of contents.
It enable TOC generation, injection and wiping"""

import sys, re, glob

# FIXME:
# - Ignore lines begining with # that lie inside a blockquote (```)
# - Manage TOC list item indent: what to do when the 1st title is a ##header and the next one is a #header ?
#                                --> it's not toc.py problem
# - The toc should be injected
#   - at the top of the file (easiest, instad of trying inject it after the optional 1st main title,
#     that is, to know if there is a 1st level title followed immediately by another title)
#   - Titling using something else than a markdown header (#) to make it recognizable (per-page _Sidebar.md possible on github?)

toc_title = "**Table of contents**"

def make_toc(filename):
    """Creates markdown toc from file contents"""
    # Collects title lines, FIXME: use "for line in open(file)" syntax http://stackoverflow.com/questions/1706198/
    lines = open(filename, 'r').read().splitlines()
    # FIXME: only match ^#*.*$ with odd count of ``` above (ie not within a quote block)
    titles = [line for index, line in enumerate(lines) if line.startswith("#") and not "".join(lines[0:index]).count('```') % 2]
    # TOC generation
    page = re.sub("\..+$", "", filename) # pagename as in URL
    page = 'wiki' if page == 'Home' else page # for github wiki homepage
    toc = []
    for title in titles:
        # Title level depends on the number of #
        level = len(title) - len(title.lstrip("#"))
        # Cleans title markdown
        title = title.lstrip("# ")
        # Creates anchor name
        anchor = title.lower().replace(" ", "-")
        # Print toc line
        toc.append("%s [%s](%s#%s)" % (
            " " * (level-1)*3 + "*",
            title, page, anchor))
    # Adds toc title if toc is not empty
    toc.insert(0, toc_title);
    return "\n".join(toc)

def wipe_toc(filename):
    """Wipes existing toc"""
    body = re.sub("^%s.*?\n\n" % re.escape(toc_title), '', open(filename, 'r').read(), flags=re.M+re.S)
    with open(filename, "w") as contents: contents.write(body)
    return "TOC wiped in %s" % filename

def apply_toc(filename):
    """Wipes existing toc and inserts created toc"""
    wipe_toc(filename)
    body = open(filename, 'r').read()
    toc = make_toc(filename)
    if toc:
        with open(filename, "w") as contents: contents.write("\n\n".join([toc, body]))
    return "TOC inserted in %s" % filename

def cli():
    """Manages CLI usage"""
    # CLI args management
    # Note: file_pattern should be between quotes, eg "*.md"
    if len(sys.argv) < 2: raise Exception("Please specify a filename to process")
    cli_pattern = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'print'
    # Parses the given file pattern: splits comma-separated patterns
    for pattern in [f.strip() for f in cli_pattern.split(',')]:
        # Globs individual file patterns
        for file in glob.glob(pattern):
            # Excutes the command
            try: print {
                    'wipe': wipe_toc,
                    'apply': apply_toc,
                    'print': make_toc
                }[command](file)
            except KeyError:
                raise Exception("Unknown command '%s'" % command)

def help():
    return "\n".join([
        'Usage: toc.py <file-pattern> <command>',
        '',
        '<file-pattern> must be quoted',
        '\tif it contains multiple comma-separated files or contain wildcards',
        '\t(eg. "*.md", "Home.md,Manual.md,Conceptual*.md,Cookbook*.md")',
        '',
        '<command> must be one of:',
        '\twipe:  wipe toc in the given file-patterns',
        '\tapply: creates/updates toc in file-patterns',
        '\tprint: print toc to stdout',
    ])


# CLI mode handler
if __name__ == "__main__":
    try: cli()
    except Exception, e:
        print "\nEXCEPTION:\n%s\n" % e
        print "%s\n" % help()
        #raise e
