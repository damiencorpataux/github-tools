"""Compiles multiple markdown pages into a single page"""

import sys, glob, toc

def compile(files):
    return "\n\n---\n\n".join([open(file).read() for file in files])

def cli():
    if len(sys.argv) < 2: raise Exception("Please specify a filename to process")
    file_pattern = sys.argv[1]
    print compile(file_pattern)
def cli():
    """Manages CLI usage"""
    # CLI args management
    # Note: file_pattern should be between quotes, eg "*.md"
    if len(sys.argv) < 2: raise Exception("Please specify a filename to process")
    cli_pattern = sys.argv[1]
    # Parses the given file pattern: splits comma-separated patterns
    files = []
    for pattern in [f.strip() for f in cli_pattern.split(',')]:
        for file in glob.glob(pattern):
            files.append(file)
    print compile(files)

    # Globs individual file patterns

def help():
    return "\n".join([
        'Concatenates the given files in <file-pattern> and prints it to stdout.',
        '',
        'Usage: one.py <file-pattern>',
        '',
        '<file-pattern> must be quoted',
        '\tif it contains multiple comma-separated files or contain wildcards',
        '\t(eg. "*.md", "Home.md,Manual.md,Conceptual*.md,Cookbook*.md")',
    ])

# CLI mode handler
if __name__ == "__main__":
    try: cli()
    except Exception, e:
        print "\nEXCEPTION:\n%s\n" % e
        print "%s\n" % help()
        #raise e