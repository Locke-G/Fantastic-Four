import sqlite3

# read textfile into list
data_list = []
with open('chartIn.txt') as f:
    file_data = f.readlines()
    for i in range(1, len(file_data)):
        data_lists = file_data[i].replace('F\n', 'F').split("\t")
        data_tuple = tuple(data_lists)
        data_list.append(data_tuple)
print(data_list)

# create empty database
connection = sqlite3.connect('df.db')

# create cursor object
cursor = connection.cursor()

# create tablenames
cursor.execute("create table df (row_number integer, window_A text,"
               " middle_B text, aisle_C text, aisle_D text, middle_E text, middle_F text)")

# read data to df
cursor.executemany('insert into df values (?,?,?,?,?,?,?)', data_list)
connection.commit()

# change value
cursor.execute('update df set window_A = "X" where row_number = 1')
connection.commit()

# show seatchart
for row in cursor.execute('select * from df'):
    print(row[1], row[2], row[3], "| |", row[4], row[5], row[6])

# close database
connection.close()
