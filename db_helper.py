from context_manager import ContextManager
from postcode import Postcode
from city import City
from address import Address
from customer import Customer
from colour import Colour
from dimension import Dimension
from price import Price
from bouncycastle import BouncyCastle
from booking import Booking
import sqlite3 as db
import traceback
from table import Table
from column import *
import statement_builder as sb
import logconfig

logger=logconfig.config_logger(__name__, "logs/crud.log")


class DBHelper():
     def __init__(self, context_manager: ContextManager):
          self.__context_manager=context_manager

          self.__prices=self.get_all_prices()
          self.__colours=self.get_all_colours()
          self.__dimensions=self.get_all_dimensions()
          
          self.__bouncy_castles=self.get_all_bouncy_castles()

          self.__cities=self.get_all_cities()
          self.__postcodes=self.get_all_postcodes()
          self.__addresses=self.get_all_addresses()

          self.__customers=self.get_all_customers()
          
          self.__bookings=self.get_all_bookings()
          self.__bookings_today=self.get_bookings_today()
          self.__bookings_previous_day=self.get_bookings_previous_day()
          self.__bookings_next_day=self.get_bookings_next_day()


     @property
     def context_manager(self) -> ContextManager:
          return self.__context_manager
     
     @context_manager.setter
     def context_manager(self, context_manager: ContextManager):
          self.__context_manager=context_manager

     @property
     def bookings(self) -> list:
          return self.__bookings
     
     @bookings.setter
     def bookings(self, bookings: list):
          self.__bookings=bookings

     @property
     def customers(self) -> list:
          return self.__customers
     
     @customers.setter
     def customers(self, customers: list):
          self.__customers=customers

     @property
     def bouncy_castles(self) -> list:
          return self.__bouncy_castles
     
     @bouncy_castles.setter
     def bouncy_castles(self, bouncy_castles: list):
          self.bouncy_castles=bouncy_castles

     @property
     def prices(self) -> list:
          return self.__prices
     
     @prices.setter
     def prices(self, prices: list) -> list:
          self.__prices=prices

     @property
     def dimensions(self) -> list:
          return self.__dimensions
     
     @dimensions.setter
     def dimensions(self, dimensions: list):
          self.__dimensions=dimensions

     @property
     def colours(self) -> list:
          return self.__colours
     
     @colours.setter
     def colours(self, colours: list):
          self.__colours=colours

     @property
     def prices(self) -> list:
           return self.__prices
     
     @prices.setter
     def prices(self, prices: list):
           self.__prices=prices

     @property
     def cities(self) -> list:
          return self.__cities
     
     @cities.setter
     def cities(self, cities: list):
          self.__cities=cities

     @property
     def postcodes(self)  -> list:
          return self.__postcodes
     
     @postcodes.setter
     def postcodes(self, postcodes: list):
           self.__postcodes=postcodes

     @property
     def addresses(self)  -> list:
           return self.__addresses
     
     @addresses.setter
     def addresses(self, addresses: list):
           self.__addresses=addresses

     @property
     def bookings_today(self)  -> list:
           return self.__bookings_today
     
     @bookings_today.setter
     def bookings_today(self, bookings: list):
           self.__bookings_today=bookings

     @property
     def bookings_next_day(self)  -> list:
           return self.__bookings_next_day
     
     @bookings_next_day.setter
     def bookings_next_day(self, bookings: list):
           self.__bookings_next_day=bookings

     @property
     def bookings_previous_day(self) -> list:
           return self.__bookings_previous_day
     
     @bookings_previous_day.setter
     def bookings_previous_day(self, bookings: list):
           self.__bookings_previous_day=bookings

     
     def update(self) -> None:
          self.__prices=self.get_all_prices()
          self.__colours=self.get_all_colours()
          self.__dimensions=self.get_all_dimensions()
          
          self.__bouncy_castles=self.get_all_bouncy_castles()

          self.__cities=self.get_all_cities()
          self.__postcodes=self.get_all_postcodes()
          self.__addresses=self.get_all_addresses()

          self.__customers=self.get_all_customers()
          
          self.__bookings=self.get_all_bookings()
          self.__bookings_today=self.get_bookings_today()
          self.__bookings_previous_day=self.get_bookings_previous_day()
          self.__bookings_next_day=self.get_bookings_next_day()

     def create_table(self, table: Table) -> None:
           with self.context_manager:
                 try:
                       self.context_manager.cursor.execute(sb.create_table_stmt(table))
                 except db.Error:
                       print(traceback.format_exc())
                       
#--------POSTCODES---------

     def get_all_postcodes(self)-> list:
          postcodes=[]
          statement="SELECT * FROM Postcode;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         postcodes.append(Postcode(res[0],
                                                   res[1],
                                                   next(filter(lambda x: x.id==res[2], 
                                                            self.cities), None)
                                                  )
                                        )
                         
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return postcodes

     def insert_or_update_postcode(self, postcode: Postcode) -> int:
          id=0
          row_query="SELECT * FROM Postcode WHERE postcode=?"
          statement="""
                    INSERT OR IGNORE INTO Postcode VALUES(?, ?, ?) 
                    ON CONFLICT (id) DO UPDATE
                    SET
                    postcode=?,
                    cityId=?
                    """
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (postcode.id, 
                                                                 postcode.postcode, 
                                                                 postcode.city.id,
                                                                 postcode.postcode,
                                                                 postcode.city.id))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (postcode.postcode,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]
                    
                         
          except db.Error:
               print(traceback.format_exc())
          finally:
                return id


     def delete_postcode(self, postcode: Postcode) -> None:
          statement="DELETE FROM Postcode WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (postcode.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#--------CITIES-----------

     def get_all_cities(self)-> list:
          cities=[]
          statement="SELECT * FROM City;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         cities.append(City(*res))

          except db.Error:
                    print(traceback.format_exc())
          finally:
               return cities

     def insert_or_update_city(self, city: City) -> int:
          id=0
          row_query="SELECT id FROM City WHERE name=?"
          statement="""INSERT OR IGNORE INTO City VALUES(?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         name=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (city.id, 
                                                                 city.name, 
                                                                 city.name))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (city.name,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]
               
          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id

     
     def delete_city(self, city: City) -> None:
          statement="DELETE FROM City WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (city.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#---------ADDRESSES---------

     def get_all_addresses(self)-> list:
          addresses=[]
          statement="SELECT * FROM Address;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         addresses.append(Address(res[0],
                                                  res[1],
                                                  res[2],
                                                  next(filter(lambda x: x.id==res[3], 
                                                            self.postcodes),  None),
                                                  )
                                        )

          except db.Error as e:
                    print(traceback.format_exc())
          finally:
               return addresses

     def insert_or_update_address(self, address: Address) -> int:
          id=0
          row_query="SELECT id FROM Address WHERE addressLine1=? AND addressLine2=? AND postcodeId=?"
          statement="""INSERT OR IGNORE INTO Address VALUES(?, ?, ?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         addressLine1=?,
                         addressLine2=?,
                         postcodeId=?"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (address.id,
                                                                    address.address_line_1,
                                                                    address.address_line_2, 
                                                                    address.postcode.id,
                                                                    address.address_line_1,
                                                                    address.address_line_2,
                                                                    address.postcode.id))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (address.address_line_1,
                                                                    address.address_line_2, 
                                                                    address.postcode.id))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]
                   
          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id


     def delete_address(self, address: Address) -> None:
          statement="DELETE FROM Address WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (address.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#----------CUSTOMERS-----------    

     def get_all_customers(self) -> list:
          customers=[]
          statement="SELECT * FROM Customer;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         customers.append(Customer(res[0],
                                                  res[1],
                                                  res[2],
                                                  res[3],
                                                  res[4],
                                                  next(filter(lambda x: x.id==res[5], 
                                                            self.addresses), None)
                                                  )
                                        )
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return customers

     def insert_or_update_customer(self, customer: Customer) -> int:
          id=0
          row_query="SELECT * FROM Customer WHERE phoneNumber=?;"
          statement="""INSERT OR IGNORE INTO Customer VALUES(?, ?, ?, ?, ?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         firstName=?,
                         lastName=?,
                         phoneNumber=?,
                         email=?,
                         addressId=?
                         ;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (customer.id,
                                                                 customer.first_name,
                                                                 customer.last_name,
                                                                 customer.phone_num,
                                                                 customer.email,
                                                                 customer.address.id,
                                                                 customer.first_name,
                                                                 customer.last_name,
                                                                 customer.phone_num,
                                                                 customer.email,
                                                                 customer.address.id))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (customer.phone_num,))
                    row=self.context_manager.cursor.fetchone()
                    
                    id=row[0]
                    
          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id
     
     def delete_customer(self, customer: Customer) -> None:
          statement="DELETE FROM Customer WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (customer.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())
#
#-----------COLOURS-----------              

     def get_all_colours(self) -> list:
          colours=[]
          statement="SELECT * FROM Colour"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()
                    
                    for res in results:
                         colours.append(Colour(res[0], res[1]))

          except db.Error:
                    print(traceback.format_exc())
          finally:
               return colours
          
     def insert_or_update_colour(self, colour: Colour) -> int:
          id=0
          row_query="SELECT * FROM Colour WHERE  name=?"
          statement="""INSERT OR IGNORE INTO Colour VALUES(?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         name=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (colour.id,
                                                                 colour.name,
                                                                 colour.name))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (colour.name,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]

          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id

     def delete_colour(self, colour: Colour) -> None:
          statement="DELETE FROM Colour WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (colour.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#------------DIMENSIONS------------              

     def get_all_dimensions(self) -> list:
          dimensions=[]
          statement="SELECT * FROM Dimension;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         dimensions.append(Dimension(*res))
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return dimensions

     def insert_or_update_dimension(self, dimension: Dimension) -> int:
          id=0
          row_query=" SELECT * FROM Dimension WHERE dimensionValues=?"
          statement="""INSERT OR IGNORE INTO Dimension VALUES(?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         dimensionValues=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (dimension.id, 
                                                                 dimension.values,
                                                                 dimension.values))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (dimension.values,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]

          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id

     def delete_dimension(self, dimension: Dimension) -> None:
          statement="DELETE FROM Dimension WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (dimension.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#----------PRICES-----------

     def get_all_prices(self) -> list:
          prices=[]
          statement="SELECT * FROM Price;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()
                    
                    for res in results:
                         prices.append(Price(*res))
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return prices
     
     def insert_or_update_price(self, price: Price) -> id:
          id=0
          row_query="SELECT * FROM Price WHERE priceValue=?"
          statement="""INSERT OR IGNORE INTO Price VALUES(?, ?)
                         ON CONFLICT (id) DO UPDATE
                         SET
                         priceValue=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (price.id,
                                                                 price.value,
                                                                 price.value))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (price.value,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]

          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id


     def delete_price(self, price: Price) -> None:
          statement="DELETE FROM Price WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (price.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

#-------BOUNCY CASTLES--------

     def get_all_bouncy_castles(self) -> list:
          castles=[]
          statement="SELECT * FROM BouncyCastle;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         castles.append(BouncyCastle(res[0],
                                                     res[1],
                                                     next(filter(lambda x: x.id==res[2],
                                                                 self.dimensions), None),
                                                     next(filter(lambda x: x.id==res[3], 
                                                            self.colours), None),
                                                     next(filter(lambda x: x.id==res[4], 
                                                            self.prices), None)))
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return castles

     def insert_or_update_bouncy_castle(self, castle: BouncyCastle) -> int:
          id=0
          row_query="SELECT * FROM BouncyCastle WHERE name=?"
          statement="""INSERT OR IGNORE INTO BouncyCastle VALUES(?, ?, ?, ?, ?)
                       ON CONFLICT (id) DO UPDATE
                       SET
                       name=?,
                       dimensionId=?,
                       colourId=?,
                       priceId=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (castle.id,
                                                                 castle.name,
                                                                 castle.dimension.id,
                                                                 castle.colour.id,
                                                                 castle.price.id,
                                                                 castle.name,
                                                                 castle.dimension.id,
                                                                 castle.colour.id,
                                                                 castle.price.id))
                    self.context_manager.connection.commit()
                    self.context_manager.cursor.execute(row_query, (castle.name,))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]

          except db.Error:
                    print(traceback.format_exc())
          finally:
                return id
     

     def delete_bouncy_castle(self, castle: BouncyCastle) -> None:
          statement="DELETE FROM BouncyCastle WHERE id=?;"
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (castle.id,))
                    self.context_manager.connection.commit()

          except db.Error:
               print(traceback.format_exc())

#------------BOOKINGS----------------             

     def get_all_bookings(self) -> list:
          bookings=[]
          statement="SELECT * FROM Booking;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()
                    
                    for res in results:
                         
                         bookings.append(Booking(res[0],
                                             res[1],
                                             next(filter(lambda x: x.id==res[2], 
                                                            self.customers), None),
                                             next(filter(lambda x: x.id==res[3], 
                                                            self.bouncy_castles), None),
                                             next(filter(lambda x: x.id==res[4], 
                                                            self.addresses), None)
                                             )
                                        )    
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return bookings

     def insert_or_update_booking(self, booking: Booking) -> int:
          id=0
          row_query="SELECT * FROM Booking WHERE date=? AND bouncyCastleId=?"

          statement="""INSERT INTO Booking 
                       VALUES(?, ?, ?, ?, ?)
                       ON CONFLICT (id) DO UPDATE
                       SET
                       date=?,
                       customerId=?,
                       bouncyCastleId=?,
                       deliveryAddressId=?;"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (booking.id,
                                                                    booking.date,
                                                                    booking.customer.id,
                                                                    booking.bouncy_castle.id,
                                                                    booking.delivery_address.id,
                                                                    booking.date,
                                                                    booking.customer.id,
                                                                    booking.bouncy_castle.id,
                                                                    booking.delivery_address.id))
                    self.context_manager.connection.commit()

                    self.context_manager.cursor.execute(row_query, (booking.date, booking.bouncy_castle.id))
                    row=self.context_manager.cursor.fetchone()

                    id=row[0]
                    
          except db.Error:
               print(traceback.format_exc())
          finally:
               return id
     
     def delete_booking(self, booking: Booking) -> None:
          statement="DELETE FROM Booking WHERE id=?;"
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement, (booking.id,))
                    self.context_manager.connection.commit()
          except db.Error:
               print(traceback.format_exc())

     def get_bookings_today(self)-> list:
           bookings=[]
           statement="SELECT * FROM Booking WHERE date=DATE('now')"
           logger.info(statement)
           try:
                 with self.context_manager:
                       self.context_manager.cursor.execute(statement)
                       results=self.context_manager.cursor.fetchall()
                       
                       for res in results:
                             bookings.append(Booking(res[0],
                                             res[1],
                                             next(filter(lambda x: x.id==res[2], 
                                                            self.customers), None),
                                             next(filter(lambda x: x.id==res[3], 
                                                            self.bouncy_castles), None),
                                             next(filter(lambda x: x.id==res[4], 
                                                            self.addresses), None)))
           except db.Error:
                 print(traceback.format_exc())
           finally:
                 return bookings
           
     def get_bookings_previous_day(self)-> list:
           bookings=[]
           statement="""SELECT * FROM Booking WHERE date IN(
                    SELECT date FROM Booking WHERE date < DATE('now')
                    GROUP BY date 
                    ORDER BY date DESC
                    LIMIT 1
                    );"""
           logger.info(statement)
           try:
                 with self.context_manager:
                       self.context_manager.cursor.execute(statement)
                       results=self.context_manager.cursor.fetchall()

                 for res in results:
                       
                    bookings.append(Booking(res[0],
                                                  res[1],
                                                  next(filter(lambda x: x.id==res[2], 
                                                                 self.customers), None),
                                                  next(filter(lambda x: x.id==res[3], 
                                                                 self.bouncy_castles), None),
                                                  next(filter(lambda x: x.id==res[4], 
                                                                 self.addresses), None)))
           except db.Error:
                 print(traceback.format_exc())
           finally:
                 return bookings
     
     def get_bookings_next_day(self)-> list:
           bookings=[]
           statement="""SELECT * FROM Booking WHERE date IN(
                    SELECT date FROM Booking WHERE date > DATE('now')
                    GROUP BY date 
                    ORDER BY date ASC
                    LIMIT 1
                    );"""
           logger.info(statement)
           try:
                 with self.context_manager:
                       self.context_manager.cursor.execute(statement)
                       results=self.context_manager.cursor.fetchall()

                 for res in results:
                    bookings.append(Booking(res[0],
                                            res[1],
                                            next(filter(lambda x: x.id==res[2], 
                                                                 self.customers), None),
                                            next(filter(lambda x: x.id==res[3], 
                                                                 self.bouncy_castles), None),
                                            next(filter(lambda x: x.id==res[4], 
                                                                 self.addresses), None)))                 
           except db.Error:
                 print(traceback.format_exc())
           finally:
                 return bookings
           
     def get_castles_for_editing_booking(self, booking: Booking)-> list: # returns all castles avaliable for the booking date, 
           castles=[]                                                    # including the castle that has originally been booked
           query="""SELECT * FROM  BouncyCastle 
                    WHERE id NOT IN 
                    (SELECT bouncyCastleId FROM Booking 
                    WHERE date=?
                    AND NOT id=?);"""
           logger.info(query)
           try:
                 with self.context_manager:
                    self.context_manager.cursor.execute(query, (booking.date, booking.id))
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         castles.append(BouncyCastle(res[0],
                                                     res[1],
                                                     next(filter(lambda x: x.id==res[2], 
                                                                 self.dimensions), None),
                                                     next(filter(lambda x: x.id==res[3], 
                                                                 self.colours), None),
                                                     next(filter(lambda x: x.id==res[4], 
                                                     self.prices), None)))
           except db.Error:
                 print(traceback.format_exc())
           finally:
                 return castles
           
     def get_castles_for_adding_new_booking(self, date: str)-> list: # returns a list of castles that are available for a specific date
           castles=[]
           query="""SELECT * FROM  BouncyCastle 
                    WHERE id NOT IN (
                    SELECT bouncyCastleId FROM Booking
                    WHERE date=?
                    );"""
           logger.info(query)
           try:
               with self.context_manager:
                    self.context_manager.cursor.execute(query, (date,))
                    results=self.context_manager.cursor.fetchall()
                    for res in results:
                         castles.append(BouncyCastle(res[0],
                                                       res[1],
                                                       next(filter(lambda x: x.id==res[2],
                                                                      self.dimensions), None),
                                                       next(filter(lambda x: x.id==res[3], 
                                                                 self.colours), None),
                                                       next(filter(lambda x: x.id==res[4], 
                                                                 self.prices), None)))
           except db.Error:
                 print(traceback.format_exc())
           finally:
                 return castles
           
     def custom_sql(self, query: str) -> list:
           results=None
           with self.context_manager:
               try:
                       self.context_manager.cursor.execute(query)
                       self.context_manager.connection.commit()
                       results=self.context_manager.cursor.fetchall()

                       if results == None:
                              results=["results None"]
                       elif not results:
                         results=["results empty"]

               except db.Error as e:
                    results=[e]
               finally:
                    return results
                 
     def search_bookings_by_customer(self, customer: Customer) -> list :
           query="SELECT * FROM Booking WHERE customerId=?"
           bookings=[]
           logger.info(query)
           with self.context_manager:
                 try:
                       self.context_manager.cursor.execute(query, (customer.id,))
                       results=self.context_manager.cursor.fetchall()

                       for res in results:
                         bookings.append(Booking(res[0],
                                                  res[1],
                                                  next(filter(lambda x: x.id==res[2], 
                                                                           self.customers), None),
                                                  next(filter(lambda x: x.id==res[3], 
                                                                           self.bouncy_castles), None),
                                                  next(filter(lambda x: x.id==res[4], 
                                                                           self.addresses), None)))
                 except db.Error:
                       print(traceback.format_exc())
                 finally:
                       return bookings
                 
     def search_bookings_by_bouncy_castle(self, bouncy_castle: BouncyCastle) -> list :
           query="SELECT * FROM Booking WHERE bouncyCastleId=?"
           bookings=[]
           logger.info(query)
           with self.context_manager:
                 try:
                       self.context_manager.cursor.execute(query, (bouncy_castle.id,))
                       results=self.context_manager.cursor.fetchall()

                       for res in results:
                         bookings.append(Booking(res[0],
                                                  res[1],
                                                  next(filter(lambda x: x.id==res[2], 
                                                                           self.customers), None),
                                                  next(filter(lambda x: x.id==res[3], 
                                                                           self.bouncy_castles), None),
                                                  next(filter(lambda x: x.id==res[4], 
                                                                           self.addresses), None)))
                 except db.Error:
                       print(traceback.format_exc())
                 finally:
                       return bookings
                 
     def search_bookings_by_date(self, date: str) -> list :
           query="SELECT * FROM Booking WHERE date=?"
           bookings=[]
           logger.info(query)
           with self.context_manager:
                 try:
                       self.context_manager.cursor.execute(query, (date,))
                       results=self.context_manager.cursor.fetchall()

                       for res in results:
                         bookings.append(Booking(res[0],
                                                  res[1],
                                                  next(filter(lambda x: x.id==res[2], 
                                                                           self.customers), None),
                                                  next(filter(lambda x: x.id==res[3], 
                                                                           self.bouncy_castles), None),
                                                  next(filter(lambda x: x.id==res[4], 
                                                                           self.addresses), None)))
                 except db.Error:
                       print(traceback.format_exc())
                 finally:
                       return bookings
                 
     def get_all_non_booked_bouncy_castles(self) -> list:
          castles=[]
          statement="""SELECT * FROM BouncyCastle WHERE id NOT IN (
                       SELECT bouncyCastleId FROM Booking WHERE date >= DATE('now')
                         );"""
          logger.info(statement)
          try:
               with self.context_manager:
                    self.context_manager.cursor.execute(statement)
                    results=self.context_manager.cursor.fetchall()

                    for res in results:
                         castles.append(BouncyCastle(res[0],
                                                     res[1],
                                                     next(filter(lambda x: x.id==res[2],
                                                                 self.dimensions), None),
                                                     next(filter(lambda x: x.id==res[3], 
                                                            self.colours), None),
                                                     next(filter(lambda x: x.id==res[4], 
                                                            self.prices), None)))
          except db.Error:
                    print(traceback.format_exc())
          finally:
               return castles