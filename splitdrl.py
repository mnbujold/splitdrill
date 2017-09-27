#!/usr/bin/env python

import sys

def _readheader(fileName):
    # Reads tool list from start of file - pre/appended with %
    header = []
    f = open(fileName)
    line = f.readline()
    if line == '%\n':
        header.append(line)
        line = f.readline()
        while line != '%\n':
            header.append(line)
            line = f.readline()
    f.close()
    header.append(line)
    return header

def _readtools(header):
    tools = []
    for i in range(3,len(header)-1):
        tools.append(header[i][:3])
    tools.append('M30')
    return tools

def _usage():
    print "splitdrl.py - Splits Excellon-format drill files into separate files for each tool size."
    print "Type: ./splitdrl.py <filename> to execute"
    
def main():

    #_fileName = "Ctl_Board_Ver_20.TXT"

    if len(sys.argv) != 2:
        _usage()
        sys.exit(1)
    else:
        _fileName = sys.argv[1]

    _header = _readheader(_fileName)
    _tools = _readtools(_header)

    sections = []
    lastline = 0
    f = open(_fileName)
    line = f.readline()
    while line:
        for tool in _tools:
            if tool == line.rstrip():
                sections.append(lastline)
        lastline = f.tell()
        line = f.readline()

    for index in range(len(sections)):
        f2 = open(_tools[index] + '.txt','w')
        for l in _header:
            f2.write(l)
        f.seek(sections[index])
        if index < len(sections)-1:
            while f.tell() < sections[index+1]:
                line = f.readline()
                f2.write(line)
        f2.write('M30')
        f2.close()
    f.close()


if __name__ == '__main__':
    main()

