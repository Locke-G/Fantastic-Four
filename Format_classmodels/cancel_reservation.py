################Cancel reservation#####################

# as long as Confirmation is false, user has to choose a seat, when free seat is chosen and confirmed, confirmation = True
confirmation_cancel = False

# check if user is admin?

# loop to select a seat
while not confirmation_cancel:
    # Seat selection
    seat = select_seat()
    if seat != None:
        row = seat[0] + 1
        sign = seat[1]
        # Check if the seat is reserved
        cursor.execute("SELECT %s FROM seats where row_number = ?" % sign, (row,))
        seat_sql = cursor.fetchall()
        if seat_sql == [('X',)]:
            print("Do you want to cancel seat ", sign, "in row ", row, "? If yes enter Y, if not enter N.")
            conf = input()
            if conf == 'Y':
                confirmation_cancel = True
                # Change selected seat from 'X' to seatnumber in dataframe
                cursor.execute('update seats set %s = ? where row_number = %s' % (sign, row), (sign,))
                connection.commit()
        else:
            print("This seat is not reserved.")
            confirmation_cancel = True
    else:
        print("Please select another seat.")
        continue

# show seat chart
for row in cursor.execute('select * from seats'):
    print(row[1], row[2], row[3], "| |", row[4], row[5], row[6])

# close database
connection.close()
