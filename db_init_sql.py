import sqlite3 as db
import traceback

connection=db.connect("BouncyCastleBookings.db")

if connection is not None:
    print("Successfully connected to database")
else:
    print("Connection to database failed")

cursor=connection.cursor()
cursor.execute("PRAGMA foreign_keys=1")

statements=("""CREATE TABLE IF NOT EXISTS "Postcode" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"postcode" TEXT UNIQUE,
"cityId" INTEGER NOT NULL,
FOREIGN KEY(cityId) REFERENCES City(id) 
);""",

"""CREATE TABLE IF NOT EXISTS "City" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"name" TEXT UNIQUE
);""",

"""CREATE TABLE IF NOT EXISTS "Address" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"addressLine1" TEXT,
"addressLine2" TEXT,
"postcodeId" INTEGER NOT NULL,
FOREIGN KEY(postcodeId) REFERENCES Postcode(id)
);""",


"""CREATE TABLE IF NOT EXISTS "Customer" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"firstName" TEXT,
"lastName" TEXT,
"phoneNumber" TEXT,
"email" TEXT,
"addressId" INTEGER NOT NULL,
FOREIGN KEY(addressId) REFERENCES Address(id)
);""",

"""CREATE TABLE IF NOT EXISTS "Colour" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"name" TEXT UNIQUE
);""",

"""CREATE TABLE IF NOT EXISTS "Dimension" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"values" TEXT UNIQUE
);""",

"""CREATE TABLE IF NOT EXISTS "Price" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"value" TEXT UNIQUE
);""",

"""CREATE TABLE IF NOT EXISTS "BouncyCastle" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"name" TEXT UNIQUE,
"dimensionId" INTEGER NOT NULL,
"colourId" INTEGER NOT NULL,
"priceId" INTEGER NOT NULL,
FOREIGN KEY(dimensionId) REFERENCES Dimension(id), 
FOREIGN KEY(colourId) REFERENCES Colour(id),
FOREIGN KEY(priceId) REFERENCES Price(id)
);""",

"""CREATE TABLE IF NOT EXISTS "Booking" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"date" TEXT,
"customerId" INTEGER NOT NULL,
"bouncyCastleId" INTEGER NOT NULL,
"deliveryAddressID" INTEGER NOT NULL,
FOREIGN KEY(customerId) REFERENCES Customer(id) ON DELETE CASCADE,
FOREIGN KEY(bouncyCastleId) REFERENCES BouncyCastle(id) ON DELETE CASCADE,
FOREIGN KEY(deliveryAddressId) REFERENCES Address(id)
);""")

for statement in statements:
    try:
        cursor.execute(statement)
        connection.commit()
    except db.Error as e:
        print("Error while creating tables: ", traceback.format_exc() )

colours=[("red",), ("blue",), ("purple",), ("pink",), 
         ("green",), ("black",), ("orange",), ("yellow",)]

dimensions=[("8 x 10 x 9 ft",), ("13 x 13 x 10 ft",), ("7 x 12 x 10 ft",), 
            ("15 x 15 x 10 ft",), ("15 x 20 x 15 ft",)]

prices=[("60",), ("70",),("90",),("100",),("110",)]
bouncy_castles=[("Princess castle with slide", 2, 4, 3), 
                ("Fortnite", 4, 6, 4), 
                ("Paw Patrol with ball pit", 3, 1, 2), 
                ("Frozen", 1, 2, 1),
                ("Cocomelon with ball pit", 3, 8, 3),
                ("Giant slide", 5, 3, 5),
                ("Disco Dome", 4, 2, 4),
                ("Dinousaur with slide", 3, 5, 5),
                ("Superhero", 2, 1, 2), 
                ("Minions", 1, 8, 1)]

cities=[("Manchester",), ("Oldham",), ("Middleton",), ("Salford",)]

postcodes=[("M40 9WJ", 1), ("M9 4ED", 1), ("OL11 7BY", 2), 
           ("OL9 1GD", 2), ("M24 1SB", 3), ("M17 1SB", 1), 
           ("M9 5HY", 1)]

addresses=[("275 Moston lane", "", 1), 
           ("23 Beverley street", "", 2),
           ("111 Cambridge street", "Flat 1", 3),
           ("78 Oscar street", "", 4),
           ("239 Rochdale road", "", 5),
           ("Guinness Road Trading Estate", "Unit 1", 6),
           ("665 Church Lane", "2nd Floor", 7),
           ("664 Church Lane", "", 7),
           ("663 Church Lane", "", 7),
           ("662 Church Lane", "", 7)]

customers=[("Test", "User", "08767655432", "bouncycastles0161@gmail.com", 1), 
           ("John", "Murphy", "03476543218", "mcar75@mail.com", 2),
           ("Amira", "Basa", "08764389765", "pinkprincess@mail.com", 3),
           ("Mike", "Jones", "0453262288", "milliej@mail.com", 4),
           ("Samira", "Basa", "07886554322", "samba@mail.com", 5),
           ("Alan", "Basa", "08765443782", "alanb@mail.com", 6),
           ("Destiny", "Osadiaye", "04582911875", "destiny@mail.com", 7),
           ("Prayer", "Osadiaye", "09843762287", "prayer@mail.com", 8),
           ("Favor", "Osadiaye", "04766588321", "favor@mail.com", 9),
           ("Prince", "Osadiaye", "09875546332", "prince@mail.com", 10)]

bookings=[("2023-03-01", 1, 10, 1),
          ("2023-03-02", 2, 9, 2),
          ("2023-03-02", 3, 8, 3),
          ("2023-03-04", 4, 7, 4),
          ("2023-03-04", 5, 6, 5),
          ("2023-03-08", 6, 5, 6),
          ("2023-03-08", 1, 4, 1),
          ("2023-03-10", 2, 3, 2),
          ("2023-03-10", 3, 2, 3),
          ("2023-05-01", 4, 1, 4),
          ("2023-05-01", 5, 2, 5),
          ("2023-05-01", 6, 3, 6),
          ("2023-05-01", 1, 4, 1),
          ("2023-05-02", 2, 5, 2),
          ("2023-05-02", 3, 6, 3),
          ("2023-05-03", 4, 7, 4),
          ("2023-05-03", 5, 8, 5),
          ("2023-05-08", 6, 9, 6),
          ("2023-05-06", 1, 10, 1),
          ("2023-05-06", 2, 9, 2),
          ("2023-05-06", 3, 8, 3),
          ("2023-05-06", 4, 7, 4),
          ("2023-05-08", 5, 6, 5),
          ("2023-05-08", 6, 5, 6),
          ("2023-05-08", 1, 4, 1),
          ("2023-05-08", 2, 3, 2),
          ("2023-05-08", 3, 2, 3),
          ("2023-05-10", 4, 1, 4),
          ("2023-05-10", 5, 2, 5),
          ("2023-05-10", 6, 3, 6),
          ("2023-05-10", 1, 4, 1)
           ]

try:    
    statement="INSERT INTO City VALUES(NULL, ?)"
    cursor.executemany(statement, cities)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Postcode VALUES(NULL, ?, ?)"
    cursor.executemany(statement, postcodes)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Address VALUES(NULL, ?, ?, ?)"
    cursor.executemany(statement, addresses)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Dimension VALUES(NULL, ?)"
    cursor.executemany(statement, dimensions)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Colour VALUES(NULL, ?)"
    cursor.executemany(statement, colours)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Price VALUES(NULL, ?)"
    cursor.executemany(statement, prices)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO BouncyCastle VALUES(NULL, ?, ?, ?, ?)"
    cursor.executemany(statement, bouncy_castles)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

try:    
    statement="INSERT INTO Customer VALUES(NULL, ?, ?, ?, ?, ?)"
    cursor.executemany(statement, customers)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())


try:    
    statement="INSERT INTO Booking VALUES(NULL, ?, ?, ?, ?)"
    cursor.executemany(statement, bookings)
    connection.commit()
except db.Error as e:
    print(traceback.format_exc())

connection.close()
