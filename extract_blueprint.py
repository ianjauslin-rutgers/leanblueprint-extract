## Copyright (C) 2024 Ian Jauslin, Alex Kontorovich
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import re

# defaults
infile_str=""
outfile_str=""
start_delimiter=r"/\-%%"
end_delimiter=r"%%\-/"
line_delimiter=r"\-\-%%"
show="blueprint"

def print_help():
    print("Usage: extract_blueprint [-B|-L] [-s start_delimiter] [-e end_delimiter] [-l line_delimiter] [-o output] <input_file.lean>\n\
\n\
  A tool to extract the blueprint from a lean file specified with the argument <input_file.lean>\n\
\n\
  -B, --blueprint: print the blueprint, extracted from the input file (default)\n\
  -L, --lean: print the lean code from which the blueprint has been stripped\n\
  -s, --start_delimiter <start_delimiter>: a regular expression specifying the tag that opens a blueprint exntry (default: '/\\-%%')\n\
  -e, --end_delimiter <end_delimiter>: a regular expression specifying the tag that closes a blueprint exntry (default: '%%\\-/')\n\
  -l, --line_delimiter <line_delimiter>: a regular expression specifying a single line blueprint entry (default: '\\-\\-%%')\n\
  -o, --output <output>: write output to file <output> (default: stdout)\n\
\n\
")


def main():
    read_cli()

    # open input file
    if infile_str=="":
        print_help()
        exit(-1)
    infile=open(infile_str,'r')
    # read text
    text=infile.read()
    infile.close()

    # open outfile
    if outfile_str!="":
        outfile=open(outfile_str,'w')
    else:
        # default outfile: stdout
        outfile=sys.stdout

    # extract blueprint from file
    (blueprint,text_without)=extract_blueprint(text)

    if show=="blueprint":
        outfile.write(blueprint)
    elif show=="lean":
        outfile.write(text_without)


# read cli arguments
def read_cli():
    global infile_str
    global outfile_str
    global start_delimiter
    global end_delimiter
    global line_delimiter
    global show

    flag=""

    for arg in sys.argv[1:]:
        if arg=="--help":
            print_help()
            exit(0)
        elif arg=="--start":
            flag="start_delimiter"
        elif arg=="--end":
            flag="end_delimiter"
        elif arg=="line":
            flag="line_delimiter"
        elif arg=="output":
            flag="outfile"
        elif arg=="--blueprint":
            show="blueprint"
        elif arg=="--lean":
            show="lean"

        elif arg[0]=='-':
            for letter in arg[1:]:
                if letter=='s':
                    flag="start_delimiter"
                elif letter=='e':
                    flag="end_delimiter"
                elif letter=='l':
                    flag="line_delimiter"
                elif letter=='o':
                    flag="outfile"
                elif letter=='B':
                    show="blueprint"
                elif letter=='L':
                    show="lean"

        else:
            if flag=="start_delimiter":
                start_delimiter=arg
                flag=""
            elif flag=="end_delimiter":
                end_delimiter=arg
                flag=""
            elif flag=="line_delimiter":
                line_delimiter=arg
                flag=""
            elif flag=="outfile":
                line_delimiter=arg
                flag=""

            else:
                infile_str=arg


def extract_blueprint(text):
    # dictionary of extracted text
    extracted=dict()

    # extract text between delimiters
    matches=re.finditer(start_delimiter+r'(.*?)'+end_delimiter, text, flags=re.DOTALL)
    for match in matches:
        # add to extracted dict
        extracted[match.start(1)]=match.group(1)

    # extract single lines
    matches=re.finditer(r'^'+line_delimiter+r'(.*)$', text, flags=re.MULTILINE)
    for match in matches:
        # add to extracted dict
        extracted[match.start(1)]=match.group(1)

    # text without blueprint
    text_without=re.sub(start_delimiter+r'.*?'+end_delimiter,'', text, flags=re.DOTALL)
    text_without=re.sub(r'^'+line_delimiter+r'.*$','', text_without, flags=re.MULTILINE)

    # sort extracted lines
    extracted=sorted(extracted.items())
    # combine entries
    out=""
    for item in extracted:
        out=out+item[1]+"\n"

    # return the blueprint and the lean file without the blueprint
    return (out,text_without)

main()
