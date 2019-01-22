from __future__ import print_function

import sys


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

args = sys.argv

if len(args) < 2:
    print('usage: CountPairs.py input_file output_file')
    print('optional -r min max (acceptable similarity range)')
    print('optional -i intensity_percent (minimal intensity threshold)')
    exit(1)

input_path = args[1]
output_path = args[2]
intensity = 0.0
min = 1.9
max = 2.0
if args.count('-r') > 0:
    index = args.index('-r') + 1
    min = float(args[index])
    max = float(args[index+1])
if args.count('-i') > 0:
    index = args.index('-i') + 1
    intensity = float(args[index])


def are_same(l_pep, s_pep, l_pep_int, s_pep_int):
    dif = l_pep - s_pep
    return (dif >= min) and (dif < max) and (l_pep_int >= s_pep_int * intensity) and (s_pep_int >= l_pep_int * intensity)

f = open(input_path)
outfile = open(output_path, 'w')

retTime = 0
prev = 0
prev_int = 0

for line in f:
    propLine = line.split()
    if propLine[1] == "RetTime":
        retTime = propLine[2]
        outfile.write('RetTime\t'+retTime+'\n')
        prev = 0
        prev_int = 0
    else:
        if is_number(propLine[0]):
            curr = float(propLine[0])
            if are_same(curr, prev, float(propLine[1]), prev_int):
                outfile.write(str(prev) + '\t' + str(prev_int) + '\t' + str(curr) + '\t' + propLine[1] + '\n')
            prev = curr
            prev_int = float(propLine[1])
            outfile.write