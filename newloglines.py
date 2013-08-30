#!/usr/bin/python


import sys
import optparse
import sqlite3
import os.path


def main(argv):
    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options] stampdb logfile""")
    p.add_option("-v", "--verbose", action="store_true",
                 help="Verbose output.")
    options, argv = p.parse_args(argv)
    if len(argv) != 3:
        print >>sys.stderr, p.get_usage()
        return 1
    
    stampdb_name = argv[1]
    logfile_name = argv[2]
    
    try:
        stampdb = sqlite3.connect(stampdb_name)
    except sqlite3.OperationalError as e:
        print >>sys.stderr, "%s: %s" % (stampdb_name, e)
        return 2
    stampdb.text_factory = str
    c = stampdb.cursor()
    columns = (
        "logpath BLOB UNIQUE NOT NULL",
        "lastpos INTEGER NOT NULL",
        "lastlinenum INTEGER NOT NULL",
        "lastline TEXT NOT NULL",
    )
    c.execute("CREATE TABLE IF NOT EXISTS logstamps(%s)" % (", ".join(columns)))
    
    logfile_path = os.path.realpath(logfile_name)
    c.execute("SELECT * FROM logstamps WHERE logpath=?", (logfile_path,))
    match = c.fetchone()
    #print repr(match)
    try:
        with open(logfile_path, "rb") as f:
            if match:
                pos = match[1]
                f.seek(pos, os.SEEK_SET)
                newline = f.readline()
                #print repr(newline)
                #print repr(match[3])
                if newline == match[3]:
                    # If seeking to the saved position yields the saved line
                    # we continue from here.
                    linenum = match[2]
                    #print "line %d matched" % (linenum)
                else:
                    # Otherwise we start over from the beginning of the log.
                    #print "no match, reading from beginning"
                    linenum = -1
                    f.seek(0, os.SEEK_SET)
            else:
                # Read all lines from beginning of log.
                linenum = -1
            output = False
            for line in f:
                pos = f.tell()
                linenum += 1
                sys.stdout.write(line)
                output = True
            if output:
                c.execute("INSERT OR REPLACE INTO logstamps VALUES (?, ?, ?, ?)", (
                    logfile_path,
                    pos - len(line),
                    linenum,
                    line,
                ))
                stampdb.commit()
    except IOError as e:
        print >>sys.stderr, "%s: %s" % (logfile_path, e)
        return 3
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
