# Statistics
# Function to create statistics
def statistics():

    # list of all seats
    rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    columns = ['A', 'B', 'C', 'D', 'E', 'F']
    all_seats = []

    for i in range(len(rows)):
        for j in range(len(columns)):
            seat = rows[i] + columns[j]
            all_seats.append(seat)


    # list of reserved seats
    reserved_seats = []
    for row in cursor.execute('select row_number from seats where A = "X"'):
        seat = str(row[0]) + 'A'
        reserved_seats.append(seat)
    for row in cursor.execute('select row_number from seats where B = "X"'):
        seat = str(row[0]) + 'B'
        reserved_seats.append(seat)
    for row in cursor.execute('select row_number from seats where C = "X"'):
        seat = str(row[0]) + 'C'
        reserved_seats.append(seat)
    for row in cursor.execute('select row_number from seats where D = "X"'):
        seat = str(row[0]) + 'D'
        reserved_seats.append(seat)
    for row in cursor.execute('select row_number from seats where E = "X"'):
        seat = str(row[0]) + 'E'
        reserved_seats.append(seat)
    for row in cursor.execute('select row_number from seats where F = "X"'):
        seat = str(row[0]) + 'F'
        reserved_seats.append(seat)

    # list of available seats
    available_seats = []

    for i in all_seats:
        if i not in reserved_seats:
            available_seats.append(i)

    # number and percentage of seats
    av_seats_num = len(available_seats)
    av_seats_per = len(available_seats)/len(all_seats)

    re_seats_num = len(reserved_seats)
    re_seats_per = len(reserved_seats)/len(all_seats)

    #Print information
    print(str(av_seats_num) + " Sitze sind verfuegbar. (" + str(av_seats_per) + "% der Gesamtsitze)")
    print(str(re_seats_num) + " Sitze sind reserviert. (" + str(re_seats_per) + "% der Gesamtsitze)")

    print("Verfuegbare Sitze:")
    for seat in available_seats:
        print(seat + " ")

    print("Reservierte Sitze:")
    for seat in reserved_seats:
        print(seat + " ")

    for user in cursor.execute('select * from users'):
            print("UserID: " + str(user[0]) + ", Name: " + user[1] + ", User_name: " + user[2] + ", Seat: " + user[4])

    textdoc = input("If you want to download the statistics press Y.")
    if textdoc == "Y":

        # Write information in textfile statistics.txt
        with open('statistics.txt', 'w') as stats:
            stats.write(str(av_seats_num) + " Sitze sind verfuegbar. (" + str(av_seats_per) + "% der Gesamtsitze)\n")
            stats.write(str(re_seats_num) + " Sitze sind reserviert. (" + str(re_seats_per) + "% der Gesamtsitze)\n")

            stats.write("Verfuegbare Sitze:\n")
            for seat in available_seats:
                stats.write(seat + " ")
            stats.write("\n")

            stats.write("Reservierte Sitze:\n")
            for seat in reserved_seats:
                stats.write(seat + " ")
            stats.write("\n")

            # show User accounts
            for user in cursor.execute('select * from users'):
                stats.write("UserID: " + str(user[0]) + ", Name: " + user[1] + ", User_name: " + user[2] + ", Seat: " + user[4] + "\n")


#statistics()

