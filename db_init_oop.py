from db_helper import DBHelper
from context_manager import ContextManager
import data
from random import randint
from table import Table
import sqlite3 as db
import statement_builder as sb
import traceback
from random import sample
from booking import Booking

cm=ContextManager("BouncyCastleBookings.db")


def create_table(cm: ContextManager, table: Table):
    with cm:
            try:
                cm.cursor.execute(sb.create_table_stmt(table))
            except db.Error:
                print(traceback.format_exc())

for t in data.tables:
    print(t)
    create_table(cm, t)

dbh=DBHelper(cm)

saved_colours=[]
for c in data.colour_objs:
    c.id=dbh.insert_or_update_colour(c)
    saved_colours.append(c)
print(saved_colours)

saved_dimensions=[]
for d in data.dimension_objs:
    d.id=dbh.insert_or_update_dimension(d)
    saved_dimensions.append(d)
print(saved_dimensions)

saved_prices=[]
for p in data.price_objs:
    p.id=dbh.insert_or_update_price(p)
    saved_prices.append(p)
print(saved_prices)

saved_castles=[]
for c in data.castle_objs:
    c.colour=saved_colours[randint(0, len(saved_colours)-1)]
    c.dimension=saved_dimensions[randint(0, len(saved_dimensions)-1)]
    c.price=saved_prices[randint(0, len(saved_prices)-1)]
    c.id=dbh.insert_or_update_bouncy_castle(c)
    saved_castles.append(c)
print(saved_castles)

saved_cities=[]
for c in data.city_objs:
    c.id=(dbh.insert_or_update_city(c))
    saved_cities.append(c)

print(saved_cities)

saved_postcodes=[]
for p in data.postcode_objs:
    p.city=saved_cities[randint(0, len(saved_cities)-1)]
    p.id=dbh.insert_or_update_postcode(p)
    saved_postcodes.append(p)
print(saved_postcodes)

saved_addresses=[]
for a in data.addr_objs:
    a.postcode=saved_postcodes[randint(0, len(data.postcode_objs)-1)]
    a.id=dbh.insert_or_update_address(a)
    saved_addresses.append(a)
print(saved_addresses)

saved_customers=[]
for c in data.cust_objs:
    c.address=saved_addresses[randint(0, len(saved_addresses)-1)]
    c.id=dbh.insert_or_update_customer(c)
    saved_customers.append(c)
print(saved_customers)

bookings_to_save=[]
for bookings_per_day in data.all_booking_dates:
    castle_selection=sample(saved_castles, len(bookings_per_day)) #randomly select bouncy castles for each date without repetition
    customer_selection=sample(saved_customers, len(bookings_per_day)) #randomly select customers for each date without repetition
    del_addresses=[c.address for c in customer_selection] #set delivery address to customers (bililng) address for each date 
    for (booking_date, customer, castle, del_addr) in zip(bookings_per_day, customer_selection, castle_selection, del_addresses):
        bookings_to_save.append(Booking(None, booking_date, customer, castle, del_addr))

for b in bookings_to_save:
    b.id=dbh.insert_or_update_booking(b)
    
print(bookings_to_save)

