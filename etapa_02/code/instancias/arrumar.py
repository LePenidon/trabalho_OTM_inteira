import sys


def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())


instancia = int(sys.argv[1])


file1 = open(str(instancia)+'.txt', 'r')
Lines = file1.readlines()

file2 = open(str(instancia)+'_bom'+'.txt', 'w')
count = 0
for line in Lines:
    count += 1
    file2.writelines(remove_first_end_spaces(line))
    file2.writelines('\n')
