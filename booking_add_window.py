from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from tkinter import ttk
from db_helper import DBHelper
from booking import Booking
import main_window
import datetime
from address import Address
from city import City
from postcode import Postcode


class BookingAddWindow(Toplevel):
    def __init__(self, dbh: DBHelper, main_win: main_window):
        super().__init__()

        self.dbh=dbh
        self.main_win=main_win
        self.customers=dbh.customers

        self.title("Add New Booking")
        self.geometry("1000x680")
        self.resizable(False, False)


        self.select_frame=LabelFrame(self, padx=20, pady=20, borderwidth=0, highlightthickness=0)
        self.select_frame.pack(pady=(20,0))
        
        today=datetime.date.today()
        self.cal_label=Label(self.select_frame, text="Select Date")
        self.cal_label.grid(row=0, column=0)
        self.cal=Calendar(self.select_frame, selectmode="day", cursor="hand1",
                           year=today.year, month=today.month, day=today.day)
        self.cal.grid(row=1, column=0)
        self.cal.bind("<<CalendarSelected>>", self.calendar_select)

        self.castle_label=Label(self.select_frame, text="Select Bouncy Castle")
        self.castle_label.grid(row=0, column=1)
        
        self.castles_frame=Frame(self.select_frame, borderwidth=0, highlightthickness=0)
        self.castles_frame.grid(row=1, column=1, padx=(0,20))
        self.castles_scroll=Scrollbar(self.castles_frame, orient=VERTICAL)
        self.castles_scroll.pack(side=RIGHT, fill=Y)
        self.castles_box=Listbox(self.castles_frame, 
                                 yscrollcommand=self.castles_scroll.set,
                                 width=50)
        self.castles_box.pack(padx=(20,0))
        self.castles_scroll.config(command=self.castles_box.yview)
        self.castles_box.bind("<<ListboxSelect>>", self.update_castle_fields)

        self.customer_search=Entry(self.select_frame, width=50)
        self.customer_search.grid(row=0, column=2, sticky=W)
        self.search_hint="Type to search customers"
        self.customer_search.insert(0, self.search_hint)
        self.customer_search.bind("<KeyRelease>", self.filter_customers)
        self.customer_search.bind("<FocusIn>", lambda args: self.customer_search.delete(0, END))
        self.customer_search.bind("<FocusOut>", lambda args: self.search_focus_out(args))

        self.customer_frame=Frame(self.select_frame, borderwidth=0, highlightthickness=0)
        self.customer_frame.grid(row=1, column=2)
        self.customer_scroll=Scrollbar(self.customer_frame, orient=VERTICAL)
        self.customer_scroll.pack(side=RIGHT, fill=Y)
        self.customer_box=Listbox(self.customer_frame,
                                  yscrollcommand=self.customer_scroll.set, 
                                  width=50)
        self.customer_box.pack()
        self.customer_scroll.config(command=self.customer_box.yview)
        self.customer_box.bind("<<ListboxSelect>>", self.update_customer_fields)


        self.booking_frame=LabelFrame(self, padx=50, pady=10, borderwidth=0, highlightthickness=0)
        self.booking_frame.pack(anchor=N)

        self.fn_label=Label(self.booking_frame, text="First Name")
        self.fn_label.grid(row=1, column=0, sticky=E)
        self.fn_entry=Entry(self.booking_frame, width=50)
        self.fn_entry.grid(row=1, column=1, padx=5, pady=5)

        self.ln_label=Label(self.booking_frame, text="Last Name")
        self.ln_label.grid(row=2, column=0, sticky=E)
        self.ln_entry=Entry(self.booking_frame, width=50)
        self.ln_entry.grid(row=2, column=1, padx=5, pady=5)

        self.phone_label=Label(self.booking_frame, text="Phone Number")
        self.phone_label.grid(row=3, column=0, sticky=E)
        self.phone_entry=Entry(self.booking_frame, width=50)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5)

        self.email_label=Label(self.booking_frame, text="Email")
        self.email_label.grid(row=4, column=0, sticky=E)
        self.email_entry=Entry(self.booking_frame, width=50)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5)

        self.billing_label=Label(self.booking_frame, text="Billing Address")
        self.billing_label.grid(row=0, column=3, padx=5, pady=5, sticky=E)
        self.addr1_label=Label(self.booking_frame, text="Address Line 1")
        self.addr1_label.grid(row=1, column=2, padx=(20,0),sticky=E)
        self.addr1_entry=Entry(self.booking_frame, width=50)
        self.addr1_entry.grid(row=1, column=3, padx=5, pady=5)

        self.addr2_label=Label(self.booking_frame, text="Address Line 2")
        self.addr2_label.grid(row=2, column=2, padx=(20,0), sticky=E)
        self.addr2_entry=Entry(self.booking_frame, width=50)
        self.addr2_entry.grid(row=2, column=3, padx=5, pady=5)

        self.city_label=Label(self.booking_frame, text="City")
        self.city_label.grid(row=3, column=2, padx=(20,0), sticky=E)
        self.city_entry=Entry(self.booking_frame, width=50)
        self.city_entry.grid(row=3, column=3, padx=5, pady=5)

        self.postcode_label=Label(self.booking_frame, text="Postcode")
        self.postcode_label.grid(row=4, column=2, padx=(20,0), sticky=E)
        self.postcode_entry=Entry(self.booking_frame, width=25)
        self.postcode_entry.grid(row=4, column=3, padx=5, pady=5, sticky=W)

        self.castle_label=Label(self.booking_frame, text="Bouncy Castle")
        self.castle_label.grid(row=6, column=0, sticky=E)
        self.castle_entry=Entry(self.booking_frame, width=50)
        self.castle_entry.grid(row=6, column=1, padx=5, pady=5)

        self.date_label=Label(self.booking_frame, text="Date")
        self.date_label.grid(row=7, column=0, sticky=E)
        self.date_entry=Entry(self.booking_frame, width=25)
        self.date_entry.grid(row=7, column=1, padx=5, pady=5, sticky=W)

        self.price_label=Label(self.booking_frame, text="Price")
        self.price_label.grid(row=8, column=0, sticky=E)
        self.price_entry=Entry(self.booking_frame, width=25)
        self.price_entry.grid(row=8, column=1, padx=5, pady=5, sticky=W)

        self.delivery_label=Label(self.booking_frame, text="Delivery Address")
        self.delivery_label.grid(row=5, column=3, padx=5, pady=5, sticky=W)
        self.check_var=IntVar()
        self.addr_checkbutton=ttk.Checkbutton(self.booking_frame, 
                                              text="Same As Billing Address", 
                                              variable=self.check_var, 
                                              onvalue=1, 
                                              offvalue=0, 
                                              command=self.checked)
        
        self.addr_checkbutton.grid(row=5, column=3, sticky=E)
        self.del_addr1_label=Label(self.booking_frame, text="Address Line 1")
        self.del_addr1_label.grid(row=6, column=2, padx=(20,0),sticky=E)
        self.del_addr1_entry=Entry(self.booking_frame, width=50)
        self.del_addr1_entry.grid(row=6, column=3, padx=5, pady=5)

        self.del_addr2_label=Label(self.booking_frame, text="Address Line 2")
        self.del_addr2_label.grid(row=7, column=2, padx=(20,0), sticky=E)
        self.del_addr2_entry=Entry(self.booking_frame, width=50)
        self.del_addr2_entry.grid(row=7, column=3, padx=5, pady=5)

        self.del_city_label=Label(self.booking_frame, text="City")
        self.del_city_label.grid(row=8, column=2, padx=(20,0), sticky=E)
        self.del_city_entry=Entry(self.booking_frame, width=50)
        self.del_city_entry.grid(row=8, column=3, padx=5, pady=5)

        self.del_postcode_label=Label(self.booking_frame, text="Postcode")
        self.del_postcode_label.grid(row=9, column=2, padx=(20,0), sticky=E)
        self.del_postcode_entry=Entry(self.booking_frame, width=25)
        self.del_postcode_entry.grid(row=9, column=3, padx=5, pady=5, sticky=W)

        self.btn_frame=Frame(self, borderwidth=0, highlightthickness=0)
        self.btn_frame.pack(padx=(0,40), pady=(20,0), anchor=NE)

        self.cancel_btn=Button(self.btn_frame, text="Cancel", width=12, command=self.destroy)
        self.cancel_btn.grid(row=0, column=0, padx=20)

        self.add_btn=Button(self.btn_frame, text="Add Booking", width=12, command=self.save)
        self.add_btn.grid(row=0, column=1)

        self.populate_customer_listbox(self.customers)
        self.update_castle_listbox()
        self.calendar_select()

    def search_focus_out(self, e: Event) -> None:
        if not self.customer_search.get():
            self.customer_search.insert(0, self.search_hint)
    
    def checked(self) -> None:
         self.del_addr1_entry.delete(0, END)
         self.del_addr2_entry.delete(0, END)
         self.del_city_entry.delete(0, END)
         self.del_postcode_entry.delete(0, END)

         if self.check_var.get():
              
              customer=next(filter(lambda x: 
                       str(x)==self.customer_box.get(ANCHOR), 
                       self.customers), None)

              if customer is not None:
                address=customer.address
                self.del_addr1_entry.insert(0, address.address_line_1)
                self.del_addr2_entry.insert(0, address.address_line_2)
                self.del_city_entry.insert(0, address.postcode.city.name)
                self.del_postcode_entry.insert(0, address.postcode.postcode)
         

    def update_castle_listbox(self, *args) -> None:
            available_castles=self.dbh.get_castles_for_adding_new_booking(self.cal.selection_get())
            self.castles_box.delete(0, END)
            if available_castles:
                for castle in available_castles:
                    self.castles_box.insert(END, castle.name)
           

    def populate_customer_listbox(self, customers: list) -> None:
            self.customer_box.delete(0, END)        
            for customer in customers:
                self.customer_box.insert(END, str(customer))

    def filter_customers(self, *args):
        filtered_customers=list(filter(lambda x: 
                                  self.customer_search.get() in str(x).lower(), 
                                  self.customers))
        self.populate_customer_listbox(filtered_customers)

    def calendar_select(self, *args) -> None:
        self.update_castle_listbox()
        self.date_entry.delete(0, END)
        self.date_entry.insert(0, self.cal.selection_get())
        self.castle_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def update_castle_fields(self, e: Event) -> None:
        castle=next(filter(lambda x: x.name==self.castles_box.get(ANCHOR), self.dbh.bouncy_castles), None)    
        if castle is not None:
            self.castle_entry.delete(0, END)
            self.price_entry.delete(0, END)
            self.castle_entry.insert(0, castle.name)
            self.price_entry.insert(0, castle.price)

    def populate_customer_listbox(self, customers: list) -> None:
         self.customer_box.delete(0, END)
         for customer in customers:
              self.customer_box.insert(0, str(customer))

    def clear_customer_entry_fields(self) -> None:       
         self.fn_entry.delete(0, END)
         self.ln_entry.delete(0, END)
         self.phone_entry.delete(0, END)
         self.email_entry.delete(0, END)
         self.addr1_entry.delete(0, END)
         self.addr2_entry.delete(0, END)
         self.city_entry.delete(0, END)
         self.postcode_entry.delete(0, END)

    def clear_booking_entry_fields(self) -> None:
         self.castle_entry.delete(0, END)
         self.price_entry.delete(0, END)
         self.date_entry.delete(0, END)

    def update_customer_fields(self, e: Event) -> None:
         customer=next(filter(lambda x: 
                       str(x)==self.customer_box.get(ANCHOR), 
                       self.customers), None)
         self.clear_customer_entry_fields()

         if customer is not None:
            address=customer.address
            self.fn_entry.insert(0, customer.first_name)
            self.ln_entry.insert(0, customer.last_name)
            self.phone_entry.insert(0, customer.phone_num)
            self.email_entry.insert(0, customer.email)
            self.addr1_entry.insert(0, address.address_line_1)
            self.addr2_entry.insert(0, address.address_line_2)
            self.city_entry.insert(0, address.postcode.city.name)
            self.postcode_entry.insert(0, address.postcode.postcode)
            self.addr_checkbutton.state(["selected"])
            address=customer.address
            self.del_addr1_entry.insert(0, address.address_line_1)
            self.del_addr2_entry.insert(0, address.address_line_2)
            self.del_city_entry.insert(0, address.postcode.city.name)
            self.del_postcode_entry.insert(0, address.postcode.postcode)

    def save(self) -> None:        
         customer=next(filter(lambda x: str(x)==self.customer_box.get(ANCHOR), 
                                         self.customers), None)
         customer_err=""
         castle_err=""

         if customer==None:
             customer_err=messagebox.showerror("No customer seleced",
                                   "Please select a customer to save booking",
                                   parent=self)
             
             
         castle=next(filter(lambda x: x.name==self.castle_entry.get(), 
                                         self.dbh.bouncy_castles), None)    
             
         if castle==None:
             castle_err=messagebox.showerror("No bouncy castle selected", 
                                   "Please select a bouncy castle to save booking",
                                   parent=self)
             
         if not customer_err and not castle_err:
            delivery_address=customer.address if self.check_var.get() else self.save_delivery_address()

            booking_new=Booking(None,
                                self.date_entry.get(),
                                customer,
                                castle,
                                delivery_address)
                    
            self.dbh.insert_or_update_booking(booking_new)
            self.dbh.update()
            self.main_win.change_tree_data(main_window.ViewCommand.REFRESH)
            self.destroy()


    def save_delivery_address(self):
        del_city=self.save_delivery_city()
        del_postcode=self.save_del_postcode(del_city)   

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

    def save_delivery_city(self) -> City:
        del_city=next(filter(lambda x: x.name==self.city_entry.get(), self.dbh.cities), None)

        if del_city == None:
            del_city=City(None, self.del_city_entry.get())
            del_city.id=self.dbh.insert_or_update_city(del_city)

        return del_city
    
    def save_del_postcode(self, del_city: City) -> Postcode:
        del_postcode=next(filter(lambda x: x.postcode==self.del_postcode_entry.get(), 
                                self.dbh.postcodes), None)

        if del_postcode == None:
            del_postcode=Postcode(None, self.del_postcode_entry.get(), del_city)
            del_postcode.id=self.dbh.insert_or_update_postcode(del_postcode)

        return del_postcode

