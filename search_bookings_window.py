from tkinter import *
from db_helper import DBHelper
from tkinter import ttk
from datetime import date

class SearchBookingsWindow(Toplevel):
    def __init__(self, dbh: DBHelper):
        super().__init__()

        self.dbh=dbh
        self.customer_names=[str(cust) for cust in self.dbh.customers]
        self.castle_names=[str(castle) for castle in self.dbh.bouncy_castles]
        self.title("Search Bookings")
        self.geometry("900x400")
        self.resizable(False, False)

        
        self.tree_frame=Frame(self)
        self.tree_frame.grid(row=0, column=0, padx=(40,20), pady=20)
        self.tree_scroll=Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.booking_tree=ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set) 
        self.booking_tree.pack(fill="x")

        self.tree_scroll.config(command=self.booking_tree.yview)

        self.booking_tree["columns"] = ("Date", "Bouncy Castle", "Customer Name", "Postcode", "Phone Number")

        self.booking_tree.column("#0", width=0, stretch=NO)
        self.booking_tree.column("Date", anchor=W, width=100)
        self.booking_tree.column("Bouncy Castle", anchor=W, width=200)
        self.booking_tree.column("Customer Name", anchor=W, width=200)
        self.booking_tree.column("Postcode", anchor=W, width=100)
        self.booking_tree.column("Phone Number", anchor=W, width=140)

        self.booking_tree.heading("#0", text="", anchor=W)
        self.booking_tree.heading("Date", text="Date",anchor=CENTER)
        self.booking_tree.heading("Bouncy Castle", text="Bouncy Castle",anchor=CENTER)
        self.booking_tree.heading("Customer Name", text="Name",anchor=CENTER)
        self.booking_tree.heading("Postcode", text="Postcode",anchor=CENTER)
        self.booking_tree.heading("Phone Number", text="Phone Number",anchor=CENTER)

        self.search_frame=Frame(self)
        self.search_frame.grid(row=1, column=0)

        self.customer_label=Label(self.search_frame, text="Search by customer")
        self.customer_label.grid(row=0, column=0, pady=(0, 5))
        self.castle_label=Label(self.search_frame, text="Search by bouncy castle")
        self.castle_label.grid(row=0, column=1, pady=(0, 5))
        self.date_label=Label(self.search_frame, text="Search by date (YYYY-MM-DD)")
        self.date_label.grid(row=0, column=2, pady=(0, 5))

        self.customer_combobox=ttk.Combobox(self.search_frame, width=25, values=self.customer_names )
        self.customer_combobox.grid(row=1, column=0, padx=20)
        self.castle_combobox=ttk.Combobox(self.search_frame, width=25, values=self.castle_names)
        self.castle_combobox.grid(row=1, column=1, padx=(0,18))
        self.date_entry=Entry(self.search_frame, width=25)
        self.date_entry.grid(row=1, column=2, padx=(0,20))
        
        self.search_cust_btn=Button(self.search_frame, text="Search", width=12, command=self.search_by_customer)
        self.search_cust_btn.grid(row=2, column=0, pady=20)
        self.search_castle_btn=Button(self.search_frame, text="Search", width=12, command=self.search_by_castle)
        self.search_castle_btn.grid(row=2, column=1, pady=20)
        self.search_date_btn=Button(self.search_frame, text="Search", width=12, command=self.search_by_date)
        self.search_date_btn.grid(row=2, column=2, pady=20)
        self.exit_btn=Button(self.search_frame, text="Exit", width=12, command=self.destroy)
        self.exit_btn.grid(row=2, column=3, pady=20, padx=(40,20))

        self.insert_data_into_treeview(self.dbh.bookings)

    

    def create_data_from_bookings(self, bookings: list):
        data=[]
        for booking in bookings:
            booking_details=(booking.date,
                            booking.bouncy_castle.name,
                            booking.customer,
                            booking.delivery_address.postcode,
                            booking.customer.phone_num)
            
            data.append(booking_details)         
        return data

    def insert_data_into_treeview(self, bookings: list) -> None:      
        data=self.create_data_from_bookings(bookings)
        self.booking_tree.delete(*self.booking_tree.get_children())
        count=0
        for row in data:
            self.booking_tree.insert(parent="", index="end", iid=count, text="", values=row) 
            count+=1 

    def search_by_customer(self) -> list:
        customer=next(filter(lambda x: x.first_name + " "+ x.last_name == self.customer_combobox.get(), self.dbh.customers), None)
        results=self.dbh.search_bookings_by_customer(customer)
        self.insert_data_into_treeview(results)

    def search_by_castle(self) -> list:
        castle=next(filter(lambda x: x.name == self.castle_combobox.get(), self.dbh.bouncy_castles), None)
        results=self.dbh.search_bookings_by_bouncy_castle(castle)
        self.insert_data_into_treeview(results)

    def search_by_date(self) -> list:
        search_date=self.date_entry.get()
        if not search_date:
           search_date=str(date.today())
        self.date_label.grid(row=0, column=2, pady=(0, 5))
        results=self.dbh.search_bookings_by_date(search_date)
        self.insert_data_into_treeview(results)