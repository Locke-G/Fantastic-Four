##############################
# Function to enter a seat and check if it has the right format
def select_seat():
    seat = input("Please select a seat from row 1-9, e.g. 4B (row 4 seat B): ")
    # Check length of input
    if len(seat) == 2:
        row = seat[0]
        seatnumber = seat[1]
        # Check if input is in right format
        if (row not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']) or (seatnumber not in ['A', 'B', 'C', 'D', 'E', 'F']):
            print("Input is not in correct format.")
            return None
        else:
            # row_number minus 1 to start from 1 and not 0
            row = int(seat[0])-1
            return [row, seatnumber]
    elif len(seat) == 3:
        row = seat[0:2]
        seatnumber = seat[2]
        # Check if input is in right format
        if (row not in ['10']) or (seatnumber not in ['A', 'B', 'C', 'D', 'E', 'F']):
            print("Input is not in correct format.")
            return None
        else:
            return [9, seatnumber]
    else:
        print("Input is not in correct format.")
        return None


# Function to enter a seat and check if it has the right format
def select_seat():
    seat = input("Please select a seat from row 1-9, e.g. 4B (row 4 seat B): ")
    # Check length of input
    if len(seat) == 2:
        row = seat[0]
        seatnumber = seat[1]
        # Check if input is in right format
        if (row not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']) or (seatnumber not in ['A', 'B', 'C', 'D', 'E', 'F']):
            print("Input is not in correct format.")
            return None
        else:
            # row_number minus 1 to start from 1 and not 0
            row = int(seat[0])-1
            return [row, seatnumber]
    elif len(seat) == 3:
        row = seat[0:2]
        seatnumber = seat[2]
        # Check if input is in right format
        if (row not in ['10']) or (seatnumber not in ['A', 'B', 'C', 'D', 'E', 'F']):
            print("Input is not in correct format.")
            return None
        else:
            return [9, seatnumber]
    else:
        print("Input is not in correct format.")
        return None

#reserve a seat
# as long as Confirmation is false, user has to choose a seat, when free seat is chosen and confirmed, confirmation = True
confirmation = False

# loop to select a seat
while not confirmation:
    # Seat selection
    seat = select_seat()
    if seat != None:
        row = seat[0] +1
        sign = seat[1]
        # Check if the seat is available
        cursor.execute("SELECT %s FROM seats where row_number = ?" % sign, (row,))
        seat_sql = cursor.fetchall()
        if seat_sql == [('X',)]:
            print("This seat is already occupied.")
            continue
        print("Do you want seat ", sign, "in row ", row, "? If yes enter Y, if not enter N.")
        conf = input()
        if conf == 'Y':
            confirmation = True
            # Change selected seat to 'X' as occupied seat in dataframe
            cursor.execute('update seats set %s = "X" where row_number = %s' % (sign, row))
            connection.commit()
        else:
            continue
    else:
        print("Please select another seat.")
        continue

# show seat chart
for row in cursor.execute('select * from seats'):
    print(row[1], row[2], row[3], "| |", row[4], row[5], row[6])
