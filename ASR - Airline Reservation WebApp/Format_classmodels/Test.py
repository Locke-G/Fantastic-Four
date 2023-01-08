with open('chartIn.txt') as f:
    file_contents = f.read()
    lines = file_contents.split('\n')[1:]
print(lines)

