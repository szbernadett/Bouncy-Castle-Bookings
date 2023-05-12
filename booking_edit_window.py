from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_helper import DBHelper
from booking import Booking
from postcode import Postcode
from city import City
from address import Address
from customer import Customer
import main_window

class BookingEditWindow(Toplevel):

    def __init__(self, booking: Booking, dbh: DBHelper, main_win: main_window):
        super().__init__()

        self.booking=booking
        self.dbh=dbh
        self.main_win=main_win

        self.castle=self.booking.bouncy_castle if booking is not None else None
        self.customer=self.booking.customer if booking is not None else None
        
        self.castles=self.dbh.get_castles_for_editing_booking(self.booking)
        self.castle_names=[bc.name for bc in self.castles] if booking is not None else []
        self.customer_names=[str(c) for c in self.dbh.customers] if booking is not None else []

        self.title("Edit Booking")
        self.geometry("950x430")
        self.resizable(False, False)

        self.edit_frame=Frame(self, padx=20, pady=20, borderwidth=0, highlightthickness=0)
        self.edit_frame.pack(padx=20, pady=20, anchor=W)
        
        self.customer_info_label=Label(self.edit_frame, text="Customer Info")
        self.customer_info_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.customer_label=Label(self.edit_frame, text="Customer")
        self.customer_label.grid(row=1, column=0, sticky=E)
        self.customer_combobox=ttk.Combobox(self.edit_frame, width=48, values=self.customer_names)
        self.customer_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.customer_combobox.bind("<<ComboboxSelected>>", self.customer_cbox_select)

        self.phone_label=Label(self.edit_frame, text="Phone Number")
        self.phone_label.grid(row=2, column=0, sticky=NE)
        self.phone_entry=Entry(self.edit_frame, width=50)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=N)

        self.email_label=Label(self.edit_frame, text="Email")
        self.email_label.grid(row=3, column=0, sticky=E)
        self.email_entry=Entry(self.edit_frame, width=50)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        self.billing_label=Label(self.edit_frame, text="Billing Address")
        self.billing_label.grid(row=4, column=1, padx=5, pady=(20,5), sticky=W)
        self.addr1_label=Label(self.edit_frame, text="Address Line 1")
        self.addr1_label.grid(row=5, column=0, padx=(20,0),sticky=E)
        self.addr1_entry=Entry(self.edit_frame, width=50)
        self.addr1_entry.grid(row=5, column=1, padx=5, pady=5)

        self.addr2_label=Label(self.edit_frame, text="Address Line 2")
        self.addr2_label.grid(row=6, column=0, padx=(20,0), sticky=E)
        self.addr2_entry=Entry(self.edit_frame, width=50)
        self.addr2_entry.grid(row=6, column=1, padx=5, pady=5)

        self.city_label=Label(self.edit_frame, text="City")
        self.city_label.grid(row=7, column=0, padx=(20,0), sticky=E)
        self.city_entry=Entry(self.edit_frame, width=50)
        self.city_entry.grid(row=7, column=1, padx=5, pady=5)

        self.postcode_label=Label(self.edit_frame, text="Postcode")
        self.postcode_label.grid(row=8, column=0, padx=(20,0), sticky=E)
        self.postcode_entry=Entry(self.edit_frame, width=25)
        self.postcode_entry.grid(row=8, column=1, padx=5, pady=5, sticky=W)

        self.booking_info_label=Label(self.edit_frame, text="Booking Details")
        self.booking_info_label.grid(row=0, column=3, padx=5, pady=5, sticky=W)
        self.castle_label=Label(self.edit_frame, text="Bouncy Castle")
        self.castle_label.grid(row=1, column=2, sticky=E)
        self.castle_combobox=ttk.Combobox(self.edit_frame, width=48, values=self.castle_names)
        self.castle_combobox.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=EW)

        self.date_label=Label(self.edit_frame, text="Date")
        self.date_label.grid(row=2, column=2, sticky=E)
        self.date_entry=Entry(self.edit_frame, width=25)
        self.date_entry.grid(row=2, column=3, padx=5, pady=5, sticky=W)
        self.date_entry.bind("<Key>", self.date_change)

        self.update_castles_btn=Button(self.edit_frame, text="Update Bouncy Castles", command=self.update_castles)
        self.update_castles_btn.grid(row=2, column=4)

        self.price_label=Label(self.edit_frame, text="Price")
        self.price_label.grid(row=3, column=2, sticky=E)
        self.price_value_label=Label(self.edit_frame)
        self.price_value_label.grid(row=3, column=3, padx=5, pady=5, sticky=W)

        self.delivery_label=Label(self.edit_frame, text="Delivery Address")
        self.delivery_label.grid(row=4, column=3, padx=5, pady=(20,5), sticky=W)

        self.check_var=IntVar()
        self.addr_checkbutton=ttk.Checkbutton(self.edit_frame, 
                                              text="Same As Billing Address", 
                                              variable=self.check_var, 
                                              onvalue=1, 
                                              offvalue=0, 
                                              command=self.checkbutton_checked)
        
        self.addr_checkbutton.grid(row=4, column=4, pady=(20,5), sticky=E)
        self.del_addr1_label=Label(self.edit_frame, text="Address Line 1")
        self.del_addr1_label.grid(row=5, column=2, padx=(20,0),sticky=E)
        self.del_addr1_entry=Entry(self.edit_frame, width=50)
        self.del_addr1_entry.grid(row=5, column=3, columnspan=2, padx=5, pady=5, sticky=EW)
        self.del_addr1_entry.bind("<Key>", self.uncheck_checkbutton)

        self.del_addr2_label=Label(self.edit_frame, text="Address Line 2")
        self.del_addr2_label.grid(row=6, column=2, padx=(20,0), sticky=E)
        self.del_addr2_entry=Entry(self.edit_frame, width=50)
        self.del_addr2_entry.grid(row=6, column=3, columnspan=2, padx=5, pady=5, sticky=EW)
        self.del_addr2_entry.bind("<Key>", self.uncheck_checkbutton)


        self.del_city_label=Label(self.edit_frame, text="City")
        self.del_city_label.grid(row=7, column=2, padx=(20,0), sticky=E)
        self.del_city_entry=Entry(self.edit_frame, width=50)
        self.del_city_entry.grid(row=7, column=3, columnspan=2, padx=5, pady=5, sticky=EW)
        self.del_city_entry.bind("<Key>", self.uncheck_checkbutton)


        self.del_postcode_label=Label(self.edit_frame, text="Postcode")
        self.del_postcode_label.grid(row=8, column=2, padx=(20,0), sticky=E)
        self.del_postcode_entry=Entry(self.edit_frame, width=25)
        self.del_postcode_entry.grid(row=8, column=3, padx=5, pady=5, sticky=W)
        self.del_postcode_entry.bind("<Key>", self.uncheck_checkbutton)

        self.btn_frame=Frame(self, padx=40, pady=5)
        self.btn_frame.pack(side=RIGHT, anchor=NE)
        self.save_btn=Button(self.btn_frame, text="Save Changes", width=12, command=self.save)
        self.save_btn.grid(row=0, column=1, padx=(2,20))
        self.close_btn=Button(self.btn_frame, text="Close", width=12, command=self.destroy)
        self.close_btn.grid(row=0, column=0, padx=20)

        self.init_fields()

    def uncheck_checkbutton(self, e:Event) -> None:
        self.check_var.set(0)

    def date_change(self, e: Event) -> None:
         self.castle_combobox.config(state="disabled")

    def update_castles(self) -> None:     
        self.castles=self.dbh.get_castles_for_adding_new_booking(self.date_entry.get())
        self.castle_names=[bc.name for bc in self.castles] if self.booking is not None else []
        self.castle_combobox.config(values=self.castle_names, state="normal")
        self.castle_combobox.current(0)
        self.castle=self.castles[0]
        self.price_value_label.config(text=self.castle.price.value)
        

    def castle_cbox_select(self, e: Event) -> None:           
            self.castle=next(filter(lambda x: x.name==self.castle_combobox.get(), 
                                self.castles), None)
            
            if self.booking is not None:
                self.price_value_label.config(text=self.castle.price.value )    

    def save(self) -> None:
            if self.booking is not None:
                address=self.save_address()
                self.booking.delivery_address=address if self.check_var.get() else self.save_delivery_address()
                customer=self.save_customer(address)
                self.save_booking(customer)
                self.dbh.update()
                self.main_win.change_tree_data(main_window.ViewCommand.REFRESH)
                self.destroy()

    def save_address(self) -> Address:
                city=next(filter(lambda x: x.name==self.city_entry.get(), self.dbh.cities), None)
                if city == None:
                    city=City(None, self.city_entry.get())
                    city.id=self.dbh.insert_or_update_city(city)
                
                postcode=next(filter(lambda x: x.postcode==self.postcode_entry.get(), 
                                     self.dbh.postcodes), None)
                if postcode == None:
                    postcode=Postcode(None, self.postcode_entry.get(), city)
                    postcode.id=self.dbh.insert_or_update_postcode(postcode)

                address=next(filter(lambda x: x.address_line_1==self.addr1_entry.get()
                                    and x.address_line_2==self.addr2_entry.get() 
                                    and x.postcode.postcode==self.postcode_entry.get(), 
                                    self.dbh.addresses), None)

                if address == None:
                    address=Address(None, self.addr1_entry.get(), self.addr2_entry.get(), postcode)
                    address.id=self.dbh.insert_or_update_address(address)
       
                return address
    
    def save_delivery_address(self) -> Address:             
        del_city=next(filter(lambda x: x.name==self.del_city_entry.get(), self.dbh.cities), None)
        if del_city == None:
            del_city=City(None, self.del_city_entry.get())
            del_city.id=self.dbh.insert_or_update_city(del_city)
        
        del_postcode=next(filter(lambda x: x.postcode==self.del_postcode_entry.get(), 
                                self.dbh.postcodes), None)
        if del_postcode == None:
            del_postcode=Postcode(None, self.del_postcode_entry.get(), del_city)
            del_postcode.id=self.dbh.insert_or_update_postcode(del_postcode)

        del_address=next(filter(lambda x: x.address_line_1==self.del_addr1_entry.get() 
                                and x.address_line_2==self.del_addr2_entry.get()
                                and x.postcode.postcode==del_postcode.postcode, 
                                self.dbh.addresses), None)
        if del_address == None:
            del_address=Address(None, 
                                self.del_addr1_entry.get(), 
                                self.del_addr2_entry.get(), 
                                del_postcode)
            del_address.id=self.dbh.insert_or_update_address(del_address)


        return del_address
    
    def save_customer(self, address: Address) -> Customer:
        customer=next(filter(lambda x: 
                             str(x)==self.customer_combobox.get(), 
                             self.dbh.customers), 
                             None)
        if customer == None:
            messagebox.showerror("No customer selected", "Please select a customer to save tis booking", parent=self)

        customer.phone_num=self.phone_entry.get()
        customer.email=self.email_entry.get()
        customer.address=address
        self.dbh.insert_or_update_customer(customer)

        return customer
    
    def save_booking(self, customer: Customer) -> None:

                castle=next(filter(lambda x: str(x)==self.castle_combobox.get(), 
                                self.dbh.bouncy_castles), None)

                date=self.date_entry.get()
                self.booking.date=date
                self.booking.customer=customer
                self.booking.bouncy_castle=castle
                self.dbh.insert_or_update_booking(self.booking)
    
    def customer_cbox_select(self, e: Event) -> None:
        self.customer=next(filter(lambda x: str(x)==self.customer_combobox.get(), 
                                  self.dbh.customers), None)

        if self.booking is not None:
            self.phone_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.addr1_entry.delete(0, END)
            self.addr2_entry.delete(0, END)
            self.city_entry.delete(0, END)
            self.postcode_entry.delete(0, END)
            self.del_addr1_entry.delete(0, END)
            self.del_addr1_entry.delete(0, END)
            self.del_city_entry.delete(0, END)
            self.del_postcode_entry.delete(0, END)
            

            self.phone_entry.insert(0, self.customer.phone_num)
            self.email_entry.insert(0, self.customer.email)
            self.addr1_entry.insert(0, self.customer.address.address_line_1)
            self.addr2_entry.insert(0, self.customer.address.address_line_2)
            self.city_entry.insert(0, self.customer.address.postcode.city.name)
            self.postcode_entry.insert(0, self.customer.address.postcode.postcode)

            self.addr_checkbutton.state(["!selected"])

    def checkbutton_checked(self) -> None:
         self.del_addr1_entry.delete(0, END)
         self.del_addr2_entry.delete(0, END)
         self.del_city_entry.delete(0, END)
         self.del_postcode_entry.delete(0, END)

         if self.check_var.get(): #if checked, enter billing address details of customer
              
              customer=next(filter(lambda x: 
                       str(x)==self.customer_combobox.get(), 
                       self.dbh.customers), None)

              if customer is not None:
                address=customer.address
                self.del_addr1_entry.insert(0, address.address_line_1)
                self.del_addr2_entry.insert(0, address.address_line_2)
                self.del_city_entry.insert(0, address.postcode.city.name)
                self.del_postcode_entry.insert(0, address.postcode.postcode)
         else: # if not checked and delivery address different from billing address, enter details of delivery address, otherwise leave blank
            del_address=self.booking.delivery_address
            if del_address.id != self.booking.customer.address.id:
                self.del_addr1_entry.insert(0, del_address.address_line_1)
                self.del_addr2_entry.insert(0, del_address.address_line_2)
                self.del_city_entry.insert(0, del_address.postcode.city.name)
                self.del_postcode_entry.insert(0, del_address.postcode.postcode)


    def init_fields(self) -> None:
         if self.booking is not None:
              address=self.booking.customer.address

              self.customer_combobox.current(self.customer_names.index(str(self.booking.customer)))
              self.addr1_entry.insert(0, address.address_line_1)
              self.addr2_entry.insert(0, address.address_line_2)
              self.city_entry.insert(0, address.postcode.city.name)
              self.postcode_entry.insert(0, address.postcode.postcode)
              self.phone_entry.insert(0, self.booking.customer.phone_num)
              self.email_entry.insert(0, self.booking.customer.email)

              delivery_address=self.booking.delivery_address
              self.del_addr1_entry.insert(0, delivery_address.address_line_1)
              self.del_addr2_entry.insert(0, delivery_address.address_line_2)
              self.del_city_entry.insert(0, delivery_address.postcode.city.name)
              self.del_postcode_entry.insert(0, delivery_address.postcode.postcode)

              if address.id == delivery_address.id:
                self.addr_checkbutton.state(["selected"])

              self.castle_combobox.current(self.castle_names.index(str(self.booking.bouncy_castle)))
              self.date_entry.insert(0, self.booking.date)
              self.price_value_label.config(text=self.booking.bouncy_castle.price.value)
               

              

        

    
 