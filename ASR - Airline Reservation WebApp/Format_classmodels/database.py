import sqlite3

# read textfile (seatchart) into list
data_list = []
with open('chartIn2.txt') as f:
    file_data = f.readlines()
    for i in range(1, len(file_data)):
        data_lists = file_data[i].replace('F\n', 'F').replace('X\n', 'X').split("\t")
        data_tuple = tuple(data_lists)
        data_list.append(data_tuple)
print(data_list)

#List of user accounts
#userID integer, name text, user_name text, password text, seat text
user_list = [(12, 'Gabriel', 'Gabriel', 'Gabriel', 'X'),
             (34, 'Duy', 'Duy', 'Duy', 'X'),
             (56, 'Marike', 'Marike', 'Marike', 'X'),
             (78, 'admin', 'admin', 'admin', 'X')]

# create empty database
connection = sqlite3.connect('df.db')

# create cursor object
cursor = connection.cursor()

# create table "seats" for seatchart
cursor.execute("create table seats (row_number integer, A text,"
               " B text, C text, D text, E text, F text)")

# read data to table seats
cursor.executemany('insert into seats values (?,?,?,?,?,?,?)', data_list)
connection.commit()

#create table "users" for users
cursor.execute("create table users (userID integer, name text, user_name text, password text, seat text)")

# read data to table users
cursor.executemany('insert into users values (?,?,?,?,?)', user_list)
connection.commit()


# show seatchart
for row in cursor.execute('select * from seats'):
    print(row[1], row[2], row[3], "| |", row[4], row[5], row[6])



