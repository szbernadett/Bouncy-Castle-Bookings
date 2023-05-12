from db_constants import *
from column import Primary, Foreign, BasicColumn
from table import Table
from colour import Colour
from dimension import Dimension
from price import Price
from bouncycastle import BouncyCastle
from postcode import Postcode
from city import City
from address import Address
from customer import Customer
from booking import Booking
import pandas as pd
from random import randrange, sample, randint


col_prim= Primary("id", DataType.INT)

colour_cols=[BasicColumn("name", DataType.TXT, [Constraint.NN, Constraint.U])]

colour_tbl=Table("Colour", col_prim, colour_cols)

colours=[("red",), ("blue",), ("purple",), ("pink",), 
         ("green",), ("black",), ("orange",), ("yellow",)]

dimension_prim=Primary("id", DataType.INT)

dimension_cols=[BasicColumn("dimensionValues", DataType.TXT)]

dimension_tbl=Table("Dimension", dimension_prim, dimension_cols)

dimensions=[("8 x 10 x 9 ft",), ("13 x 13 x 10 ft",), ("7 x 12 x 10 ft",), 
            ("15 x 15 x 10 ft",), ("15 x 20 x 15 ft",)]

price_prim=Primary("id", DataType.INT)

price_cols=[BasicColumn("priceValue", DataType.TXT, [Constraint.NN, Constraint.U])]

price_tbl=Table("Price", price_prim, price_cols)

prices=[("60",), ("70",),("90",),("100",),("110",)]

castle_prim=Primary("id", DataType.INT)

castle_cols=[BasicColumn("name", DataType.TXT, [Constraint.NN, Constraint.U])]

castle_fkeys=[
    Foreign("dimensionId", DataType.INT, dimension_tbl),
    Foreign("colourId", DataType.INT, colour_tbl),
    Foreign("priceId", DataType.INT, price_tbl)
    ]

castle_tbl=Table("BouncyCastle", castle_prim, castle_cols, castle_fkeys)

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

city_prim=Primary("id", DataType.INT)

city_cols=[BasicColumn("name", DataType.TXT, [Constraint.NN, Constraint.U])]

city_tbl=Table("City", city_prim, city_cols)

cities=[("Manchester",), ("Oldham",), ("Middleton",), ("Salford",)]

pcode_prim=Primary("id", DataType.INT)

postcode_cols=[
    BasicColumn("postcode", DataType.TXT, [Constraint.NN, Constraint.U])
]

pcode_fkeys=[Foreign("cityId", DataType.INT, city_tbl, fkey_constraints=[Constraint.DEL_CASC])]

postcode_tbl=Table("Postcode", pcode_prim, postcode_cols, pcode_fkeys)


postcodes=[("M40 9WJ", 1), ("M9 4ED", 1), ("OL11 7BY", 2), 
           ("OL9 1GD", 2), ("M24 1SB", 3), ("M17 1SB", 1), 
           ("M9 5HY", 1)]

addr_prim=Primary("id", DataType.INT)

address_cols=[
    BasicColumn("addressLine1", DataType.TXT, [Constraint.NN]),
    BasicColumn("addressLine2", DataType.TXT)
]

addr_fkeys=[Foreign("postcodeId", DataType.INT, postcode_tbl, fkey_constraints=[Constraint.DEL_CASC])]

address_tbl=Table("Address", addr_prim, address_cols, addr_fkeys)

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

cust_prim=Primary("id", DataType.INT)

customer_cols=[
    BasicColumn("firstName", DataType.TXT, [Constraint.NN]),
    BasicColumn("lastName", DataType.TXT, [Constraint.NN] ),
    BasicColumn("phoneNumber", DataType.TXT, [Constraint.NN] ),
    BasicColumn("email", DataType.TXT, [Constraint.NN])
]

cust_fkeys=[Foreign("addressId", DataType.INT, address_tbl)]


customer_tbl=Table("Customer", cust_prim, customer_cols, cust_fkeys)

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

booking_prim=Primary("id", DataType.INT)

booking_cols=[
    BasicColumn("date", DataType.TXT)
]

booking_fkeys=[
    Foreign("customerId", DataType.INT, customer_tbl, fkey_constraints=[Constraint.DEL_CASC]),
    Foreign("bouncyCastleId", DataType.INT, castle_tbl, fkey_constraints=[Constraint.DEL_CASC]),
    Foreign("deliveryAddressId", DataType.INT, address_tbl, constraints=[Constraint.DEF0], fkey_constraints=[Constraint.DEL_DEF])
    ]

booking_tbl=Table("Booking", booking_prim, booking_cols, booking_fkeys)

tables=(
    colour_tbl, 
    dimension_tbl, 
    price_tbl, 
    castle_tbl, 
    city_tbl,
    postcode_tbl, 
    address_tbl, 
    customer_tbl, 
    booking_tbl
    )

colour_objs=[]
for c in colours:
    colour_objs.append(Colour(None, c[0]))

dimension_objs=[]
for d in dimensions:
    dimension_objs.append(Dimension(None, d[0]))

price_objs=[]
for p in prices:
    price_objs.append(Price(None, p[0]))

castle_objs=[]
for bc in bouncy_castles:
    castle_objs.append(BouncyCastle(None, bc[0], None, None, None))

city_objs=[]
for c in cities:
    city_objs.append(City(None, c[0]))

postcode_objs=[]
for p in postcodes:
    postcode_objs.append(Postcode(None, p[0], None))

addr_objs=[]
for a in addresses:
    addr_objs.append(Address(None, a[0], a[1], None))

cust_objs=[]
for c in customers:
    cust_objs.append(Customer(None, c[0], c[1], c[2], c[3], None))


booking_date_range=pd.date_range(start="2023-03-01", end="2023-06-30", freq="2D")
booking_date_range=booking_date_range.date
print("booking date range", booking_date_range)

all_booking_dates=[]
for booking_date in booking_date_range:
    bookings_per_day=[]
    for i in range(randint(1,10)):
        bookings_per_day.append(booking_date)
    
    all_booking_dates.append(bookings_per_day)


bookings_to_save=[]
for bookings_per_day in all_booking_dates:
    castle_selection=sample(castle_objs, len(bookings_per_day)) #randomly select bouncy castles for each date without repetition
    customer_selection=sample(cust_objs, len(bookings_per_day)) #randomly select customers for each date without repetition
    del_addresses=[c.address for c in customer_selection] #set delivery address to customers (bililng) address for each date 
    for (booking_date, customer, castle, del_addr) in zip(bookings_per_day, customer_selection, castle_selection, del_addresses):
        bookings_to_save.append(Booking(None, booking_date, customer, castle, del_addr))





