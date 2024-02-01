import datetime

import db_base as db
import csv

class Availability:

    def __init__(self, row):
        self.room_number = row[0]
        self.status = row[1]

class Booking:

    def __init__(self, row):
        self.room_number = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.email = row[4]
        self.price = row[5]
        self.date = row[6]


class CsvAvailability(db.DBbase):
    def __init__(self, db_name):
        super().__init__(db_name)

    def read_csv(self, file_name):
        self._availability = []

        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                next(record)
                for row in csv_reader:
                    availability = Availability(row)
                    self._availability.append(availability)

        except Exception as e:
            print(e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Availability;

                CREATE TABLE Availability (
                    room_number TEXT NOT NULL PRIMARY KEY UNIQUE,
                    status TEXT);

            """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)

    def save_to_database(self):
        print("Number of records to save: ", len(self._availability))
        save = input("Continue?(y/n) ").lower()
        if save == "y":
            for room in self._availability:
                try:
                    super().get_cursor.execute(""" INSERT OR IGNORE INTO Availability (room_number, status)
                    VALUES (?,?)""", (room.room_number, room.status))
                    super().get_connection.commit()
                    print("Saved record", room.room_number, room.status)
                except Exception as e:
                    print(e)
        else:
            print("Record(s) not saved.")

    def room_availability_update(self, room_number):
        try:
            super().get_cursor.execute("UPDATE Availability SET status = \"Not Available\" where room_number = ?", (room_number,))
            super().get_connection.commit()
            print("Updated record", room_number, "Not Available")
        except Exception as e:
            print(e)

    def menu(self):
        try:
            room_details = super().get_cursor.execute("SELECT room_number, room_type, price FROM Reservation where room_number in (SELECT room_number FROM Availability where status = \"Available\");") \
                .fetchall()
            print("Available Rooms :")
            for room in room_details:
                print(room[0], room[1], room[2])
            room_number = input("What room would you like to book? ")
            #print("Room :", room_number)
            print("Please enter you details:")
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone: ")
            price = super().get_cursor.execute("SELECT price FROM Reservation where room_number = ?;", (room_number, )) \
                .fetchone()
            #print("Price:", price)
            #print(f"Room {room_number} booked successfully!")
            self.room_availability_update(room_number)
            return [room_number, first_name, last_name, email, phone, price[0]]
        except Exception as e:
            print(e)


class CsvBooking(db.DBbase):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add(self,room_number=None, first_name=None, last_name=None, email=None, phone=None, price=None, date=None):
        try:
            super().get_cursor.execute(
                """Insert or Ignore into Booking (room_number,first_name,last_name,email,phone,price,date) values (?,?,?,?);""",
                (room_number, first_name, last_name, email, phone, price, date))
            super().get_connection.commit()
            print(f" {room_number} reservation completed successfully.")

        except Exception as e:
            print("An error as occured", e)

    def update(self, booking_id=None,room_number=None, first_name=None, last_name=None, email=None, phone=None, price=None,date=None):

        try:
            super().get_cursor.execute(
                """update Booking set room_number = ? ,first_name = ?, last_name=?,email=?,phone = ? , price = ?,date=? WHERE booking_id = ?;""",
                (room_number,first_name, last_name, email, phone, price,date, booking_id,))

            super().get_connection.commit()
            print(f"{room_number} details updated successfully")

        except Exception as e:
            print("An error as occured", e)

    def delete(self, booking_id):

        try:
            super().get_cursor.execute("""DELETE FROM Booking WHERE booking_id = ?;""", (booking_id,))
            super().get_connection.commit()
            print("room details deleted Successfully !")

        except Exception as e:
            print("An error as occurred", e)

    def fetch(self, booking_id=None):
        try:
            if booking_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Booking WHERE booking_id = ? ;""",
                                                  (booking_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Booking;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))

    def read_csv(self, file_name):
        self._booking = []

        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                next(record)
                for row in csv_reader:
                    print("row", row)
                    booking = Booking(row)
                    self._booking.append(booking)

        except Exception as e:
            print(e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Booking;

                CREATE TABLE Booking (
                    booking_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    room_number TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    email TEXT,
                    price TEXT,
                    date TEXT);

            """
            super().execute_script(sql)
            print("Created Booking Table!")
        except Exception as e:
            print("An error occurred.", e)

    def save_to_database(self):
        print("Number of records to save: ", len(self._booking))
        save = input("Continue?(y/n) ").lower()
        if save == "y":
            for record in self._booking:
                try:
                    now = datetime.datetime.now()
                    super().get_cursor.execute(""" INSERT OR IGNORE INTO Booking (room_number, first_name, last_name, phone, email, price, date)
                    VALUES (?,?,?,?,?,?,?)""", (record.room_number, record.first_name, record.last_name, record.phone, record.email, record.price, now))
                    super().get_connection.commit()
                    print("Saved record", record.room_number, record.first_name, record.last_name, record.phone, record.email, now)
                except Exception as e:
                    print(e)
        else:
            print("Record(s) not saved.")

    def room_book(self, room_number, first_name, last_name, phone, price, email):
        try:
            now = datetime.datetime.now()
            super().get_cursor.execute(""" INSERT OR IGNORE INTO Booking (room_number, first_name, last_name, phone, email, price, date)
            VALUES (?,?,?,?,?,?,?)""", (
                                    room_number, first_name, last_name, phone, email, price, now))
            super().get_connection.commit()
            print("Saved record", room_number, first_name, last_name, phone, email, price, now)
        except Exception as e:
            print(e)


def main():
    availability = CsvAvailability("ReservationDB.sqlite")
    # availability.reset_database()
    # availability.read_csv("Status.csv")
    # availability.save_to_database()
    booking_details = availability.menu()
    print(booking_details)
    booking = CsvBooking("ReservationDB.sqlite")
    #booking.reset_database()
    #print("Reset done!")
    #booking.read_csv("Details.csv")
    #print("Read Csv done!")
    #booking.save_to_database()
    #booking.add('123','akilika','anjan','aa@gmail.com','3456789876','$250','03/25/2023')
    booking.room_book(booking_details[0], booking_details[1], booking_details[2], booking_details[3], booking_details[4], booking_details[5])

