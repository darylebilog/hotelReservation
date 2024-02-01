import db_base as db
import csv


class Reservation:

    def __init__(self, row):
        self.room_type = row[0]
        self.bed_type = row[1]
        self.bed_count = row[2]
        self.price = row[3]
        self.room_number = row[4]


class CsvReservation(db.DBbase):

    def __init__(self, db_name):
        super().__init__(db_name)
        self._reservation_score = None

    def reset_database(self):

        try:
            sql = """
                DROP TABLE IF EXISTS Reservation;

                CREATE TABLE Reservation (
                room_type TEXT NOT NULL,
                bed_type TEXT NOT NULL,
                bed_count INTEGER,
                price FLOAT,
                room_number TEXT NOT NULL PRIMARY KEY UNIQUE);
            """
            super().execute_script(sql)

        except Exception as e:
            print(e)

    def read_reservation_data(self, file_name):
        self._reservation_score = []

        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                next(record)
                for row in csv_reader:
                    res = Reservation(row)
                    self._reservation_score.append(res)

        except Exception as e:
            print(e)

    def save_to_database(self):
        print("Number of records to save: ", len(self._reservation_score))
        save = input("Continue? ").lower()

        if save == "yes":
            for item in self._reservation_score:

                try:
                    super().get_cursor.execute("""INSERT INTO Reservation
                        (room_type, bed_type, bed_count, price, room_number)
                        VALUES(?,?,?,?,?)""",
                                               (item.room_type, item.bed_type, item.bed_count, item.price,
                                                item.room_number))
                    super().get_connection.commit()
                    print("Saved item", item.room_type, item.bed_type, item.room_number)
                except Exception as e:
                    print(e)
        else:
            print("Export to DB aborted")

    def room_reservation_update(self):
        self._reservation_score = []

        room_number = input("Enter room number: ")
        room_type = input("Enter updated room type: ")
        bed_type = input("Enter updated bed type: ")
        bed_count = input("Enter updated bed count: ")
        price = input("Enter updated price: ")

        try:
            super().get_connection.execute("""UPDATE Reservation
            SET room_type = ?,
            bed_type = ?,
            bed_count = ?,
            price = ?
            WHERE room_number = ?""",
                                           (room_type, bed_type, bed_count, price, room_number))
            super().get_connection.commit()
            print("Details updated for Room", room_number)
        except Exception as e:
            print(e)

    def delete_room(self, room_number):
        try:
            super().get_cursor.execute("""DELETE FROM Reservation
            WHERE room_number = ?;""", (room_number,))
            super().get_connection.commit()
            print("Room details deleted Successfully for ", room_number)

        except Exception as e:
            print("An error as occurred", e)

    def add_room(self):
        self._reservation_score = []

        room_number = input("Enter room number: ")
        room_type = input("Enter updated room type: ")
        bed_type = input("Enter updated bed type: ")
        bed_count = input("Enter updated bed count: ")
        price = input("Enter updated price: ")

        try:
            super().get_connection.execute("""INSERT OR IGNORE INTO Reservation
            (room_type, bed_type, bed_count, price, room_number)
            VALUES (?,?,?,?,?)""",
                                            (room_type, bed_type, bed_count, price, room_number))
            super().get_connection.commit()
            print("Added details for Room", room_number)
        except Exception as e:
            print(e)

    def fetch(self):
        self._reservation_score = []

        room_number = input("Enter Room Number: ")
        try:
            if room_number is not None:
                return print(super().get_cursor.execute("""SELECT * FROM Reservation WHERE room_number = ? ;""",
                                                  (room_number,)).fetchone())
            else:
                return print(super().get_cursor.execute("""SELECT * FROM Reservation;""").fetchall())
        except Exception as e:
            print("An error occurred : {}".format(e))


csv_lab = CsvReservation("ReservationDB.sqlite")
# csv_lab.reset_database()
# csv_lab.read_reservation_data("hotel_room_list.csv")
# csv_lab.save_to_database()
# csv_lab.room_reservation_update()
# csv_lab.delete_room("1606")
# csv_lab.add_room()
csv_lab.fetch()
