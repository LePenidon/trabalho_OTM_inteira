def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())


file1 = open('5.txt', 'r')
Lines = file1.readlines()

file2 = open('5_bom.txt', 'w')
count = 0
for line in Lines:
    count += 1
    file2.writelines(remove_first_end_spaces(line))
    file2.writelines('\n')
