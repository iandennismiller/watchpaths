#!/usr/bin/env python

"""
usage: watchfiles cmd path1 path2 ...
"""

# The current version of watchpaths (c) 2010 Ian Dennis Miller
# Released under an MIT license.

# This is heavily influenced by the pattern available here: 
# http://www.amk.ca/python/simple/dirwatch.html

import os, time, sys

def watch_directories (paths, func, delay=1.0):
    """(paths:[str], func:callable, delay:float)
    Continuously monitors the paths and their subdirectories
    for changes.  If any files or directories are modified,
    the callable 'func' is called with a list of the modified paths of both
    files and directories.  'func' can return a Boolean value
    for rescanning; if it returns True, the directory tree will be
    rescanned without calling func() for any found changes.
    (This is so func() can write changes into the tree and prevent itself
    from being immediately called again.)
    """

    # Basic principle: all_files is a dictionary mapping paths to
    # modification times.  We repeatedly crawl through the directory
    # tree rooted at 'path', doing a stat() on each file and comparing
    # the modification time.

    all_files = {}
    def f (unused, dirname, files):
        # Traversal function for directories
        
        for filename in files:
            path = os.path.join(dirname, filename)

            if '.svn' in dirname.split('/') or filename == '.svn':
                continue
                
            if '.pyc' in os.path.splitext(filename):
                continue

            try:
                t = os.stat(path)
            except os.error:
                # If a file has been deleted between os.path.walk()
                # scanning the directory and now, we'll get an
                # os.error here.  Just ignore it -- we'll report
                # the deletion on the next pass through the main loop.
                continue

            mtime = remaining_files.get(path)
            if mtime is not None:
                # Record this file as having been seen
                del remaining_files[path]
                # File's mtime has been changed since we last looked at it.
                if t.st_mtime > mtime:
                    if not os.path.isdir(path):
                        print "changed: ", path
                        changed_list.append(path)
            else:
                # No recorded modification time, so it must be
                # a brand new file.
                changed_list.append(path)

            # Record current mtime of file.
            all_files[path] = t.st_mtime

    # Main loop
    rescan = False
    while True:
        changed_list = []
        remaining_files = all_files.copy()
        all_files = {}
        for path in paths:
            os.path.walk(path, f, None)
        removed_list = remaining_files.keys()
        if rescan:
            rescan = False
        elif changed_list or removed_list:
            rescan = func(changed_list, removed_list)

        time.sleep(delay)
        
def watch_paths(cmd, paths):
    def f (changed_files, removed_files):
        #os.system("clear")
        for i in range(1, 20):
            print
        print "running " + cmd
        os.system(cmd)
            
    watch_directories(paths, f, 1)

def main():
    self = sys.argv.pop(0)
    cmd = sys.argv.pop(0)
    
    paths = []

    for arg in sys.argv:
        paths.append(arg)

    watch_paths(cmd, paths)

main()
