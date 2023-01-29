#with open('chartIn.txt') as f:
#    file_contents = f.read()
#    lines = file_contents.split('\n')[1:]
#print(lines)


with open('chartIn.txt') as f:
    file = f.read()
    values = []
    for line in file:
        parts = line.strip().split('\t')
        values.append(column1=parts[0], column2=parts[1], column3=parts[2], column4=parts[3], column5=parts[4],
                      column6=parts[5])
