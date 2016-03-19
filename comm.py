#!/usr/bin/python

"""
This program imitates the "comm" command on the linux command line. 
I also implemented the -u flag for unsorted files
and -1 -2 -3 to remove lines that are unique to one file or both.
"""

import random, sys
from optparse import OptionParser

class randline:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()

    def chooseline(self):
        return random.choice(self.lines)

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE

    Compares two files"""

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-u",
                      action="store_true", dest="unsorted", default=False,
                      help="output NUMLINES lines (default 1)")
    parser.add_option("-1",
                      action="store_true", dest="option1", default=False)
    parser.add_option("-2",
                      action="store_true", dest="option2", default=False)
    parser.add_option("-3",
                      action="store_true", dest="option3", default=False)
    options, args = parser.parse_args(sys.argv[1:])
    try:
        unsorted = options.unsorted
        numlines = int(options.numlines)
        option1 = options.option1
        option2 = options.option2
        option3 = options.option3
    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))
    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if len(args) != 2:
        parser.error("wrong number of operands")
    input_file1 = args[0]
    input_file2 = args[1]
    try:
        generator = randline(input_file1)
        generator2 = randline(input_file2)
        file1_length = len(generator.lines)
        file2_length = len(generator2.lines)
        if unsorted == True: #used -u
            i = 0
            j = 0
            while i + j < file1_length + file2_length:
                if i >= file1_length:
                    if not option2:
                        if not option1:
                            sys.stdout.write('        ')
                        sys.stdout.write(str(generator2.lines[j]))
                    j = j + 1
                    continue
                elif j >= file2_length:
                    if not option1:
                        sys.stdout.write(str(generator.lines[i]))
                    i = i + 1
                    continue
                if generator.lines[i] < generator2.lines[j]:
                    temp = j
                    common = False
                    while temp < file2_length:
                        if generator.lines[i] == generator2.lines[temp]:
                            if not option3:
                                if not option1:
                                    sys.stdout.write('        ')
                                if not option2:
                                    sys.stdout.write('        ')
                            sys.stdout.write(str(generator.lines[i]))
                            generator2.lines.remove(generator.lines[i])
                            common = True
                            file2_length = file2_length - 1
                            break
                        temp = temp + 1

                    if common == False:
                        if not option1:
                            sys.stdout.write(str(generator.lines[i]))
                    i = i + 1
                    continue
                elif generator2.lines[j] < generator.lines[i]:
                    temp = i
                    common = False
                    while temp < file1_length:
                        if generator2.lines[j] == generator.lines[temp]:
                            if not option3:
                                if not option1:
                                    sys.stdout.write('        ')
                                if not option2:
                                    sys.stdout.write('        ')
                                sys.stdout.write(str(generator2.lines[j]))
                            generator.lines.remove(generator2.lines[j])
                            common = True
                            file1_length = file1_length - 1
                            break
                        temp = temp + 1
                    if (common == False) & (not option2):
                        if not option1:
                            sys.stdout.write('        ')
                        sys.stdout.write(str(generator2.lines[j]))
                    j = j + 1
                    continue
                else:
                    if not option3:
                        if not option1:
                            sys.stdout.write('        ')
                        if not option2:
                            sys.stdout.write('        ')
                        sys.stdout.write(str(generator.lines[i]))
                    i = i + 1
                    j = j + 1
            
        else: #User did not use -u
            temp_list = []
            temp_list2 = []
            for i in range(file1_length):
                temp_list.append(generator.lines[i])
            for i in range(file2_length):
                temp_list2.append(generator2.lines[i])
            temp_list.sort()
            temp_list2.sort()
            
            list1_sorted = True
            list2_sorted = True
            for i in range(file1_length):
                if temp_list[i] != generator.lines[i]:
                    list1_sorted = False
            for i in range(file2_length):
                if temp_list2[i] != generator2.lines[i]:
                    list2_sorted = False
            i = 0
            j = 0
            if list1_sorted and list2_sorted:
                while i + j < file1_length + file2_length:
                    if i >= file1_length:
                        if not option2:
                            if not option1:
                                sys.stdout.write('        ')
                            sys.stdout.write(str(generator2.lines[j]))
                        j = j + 1
                        continue
                    elif j >= file2_length:
                        if not option1:                            
                            sys.stdout.write(str(generator.lines[i]))
                        i = i + 1
                        continue
                    if generator.lines[i] < generator2.lines[j]:
                        if not option1:
                            sys.stdout.write(str(generator.lines[i]))
                        i = i + 1
                        continue
                    elif generator2.lines[j] < generator.lines[i]:
                        if not option2:
                            if not option1:
                                sys.stdout.write('        ')
                            sys.stdout.write(str(generator2.lines[j]))
                        j = j + 1
                        continue
                    else:
                        if not option3:
                            if not option1:
                                sys.stdout.write('        ')
                            if not option2:
                                sys.stdout.write('        ')
                            sys.stdout.write(str(generator.lines[i]))
                        i = i + 1
                        j = j + 1
            else:
                if(list2_sorted == False):
                    sys.stdout.write("comm: file 2 is not in sorted order\n")
                if(list1_sorted == False):
                    sys.stdout.write("comm: file 1 is not in sorted order\n")
                parser.error("One or more files were not in sorted order")
    except IOError as e:
        parser.error("I/O error({0}): {1}".
                     format(e.errno, e.strerror))

if __name__ == "__main__":
    main()
