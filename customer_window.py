from tkinter import *
from tkinter import ttk
from db_helper import DBHelper
from postcode import Postcode
from address  import Address
from city import City
import main_window

class CustomerWindow(Toplevel):
    def __init__(self, dbh: DBHelper, main_win: main_window):
        super().__init__()

        self.dbh=dbh
        self.main_win=main_win
        self.customer=None
        self.title("View and Edit Customers")
        self.geometry("900x520")
        self.resizable(False, False)

        self.tree_frame=Frame(self)
        self.tree_frame.pack(padx=20, pady=20)
        
        self.tree_yscroll=Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_yscroll.pack(side=RIGHT, fill=Y)
        self.tree_xscroll=Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.tree_xscroll.pack(side=BOTTOM, fill=X)

        self.customer_tree=ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_yscroll.set, xscrollcommand=self.tree_xscroll.set, selectmode="extended") 
        self.customer_tree.pack()

        self.tree_yscroll.config(command=self.customer_tree.yview)
        self.tree_xscroll.config(command=self.customer_tree.xview)

        
        self.customer_tree["columns"] = ("First Name", "Last Name", "Phone Number", "Email", "Post Code", "City", "Address Line 1", "Address Line 2")
                                    

        for col in self.customer_tree["columns"]:
            self.customer_tree.heading(col, text=f"{col}", anchor=CENTER)
            self.customer_tree.column(col, anchor=W, width=80) # initially smaller size
        self.customer_tree.update()
        
        for col in self.customer_tree["columns"]:
            self.customer_tree.column(col, width=140, stretch=NO)

        self.customer_tree.column("#0", width=0, stretch=NO)
        self.customer_tree.heading("#0", text="", anchor=E)
        self.customer_tree.bind("<<TreeviewSelect>>", self.treeview_select)

        self.customer_frame=LabelFrame(self, padx=20, pady=10)
        self.customer_frame.pack(pady=20)

        self.fn_label=Label(self.customer_frame, text="First Name")
        self.fn_label.grid(row=0, column=0, sticky=E)
        self.fn_entry=Entry(self.customer_frame, width=50)
        self.fn_entry.grid(row=0, column=1, padx=5, pady=5)

        self.ln_label=Label(self.customer_frame, text="Last Name")
        self.ln_label.grid(row=1, column=0, sticky=E)
        self.ln_entry=Entry(self.customer_frame, width=50)
        self.ln_entry.grid(row=1, column=1, padx=5, pady=5)

        self.phone_label=Label(self.customer_frame, text="Phone Number")
        self.phone_label.grid(row=2, column=0, sticky=E)
        self.phone_entry=Entry(self.customer_frame, width=50)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        self.email_label=Label(self.customer_frame, text="Email")
        self.email_label.grid(row=3, column=0, sticky=E)
        self.email_entry=Entry(self.customer_frame, width=50)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        self.addr1_label=Label(self.customer_frame, text="Address Line 1")
        self.addr1_label.grid(row=0, column=2, padx=(20,0),sticky=E)
        self.addr1_entry=Entry(self.customer_frame, width=50)
        self.addr1_entry.grid(row=0, column=3, padx=5, pady=5)

        self.addr2_label=Label(self.customer_frame, text="Address Line 2")
        self.addr2_label.grid(row=1, column=2, padx=(20,0), sticky=E)
        self.addr2_entry=Entry(self.customer_frame, width=50)
        self.addr2_entry.grid(row=1, column=3, padx=5, pady=5)

        self.city_label=Label(self.customer_frame, text="City")
        self.city_label.grid(row=2, column=2, padx=(20,0), sticky=E)
        self.city_entry=Entry(self.customer_frame, width=50)
        self.city_entry.grid(row=2, column=3, padx=5, pady=5)

        self.postcode_label=Label(self.customer_frame, text="Postcode")
        self.postcode_label.grid(row=3, column=2, padx=(20,0), sticky=E)
        self.postcode_entry=Entry(self.customer_frame, width=25)
        self.postcode_entry.grid(row=3, column=3, padx=5, pady=5, sticky=W)

        self.delete_btn_frame=Frame(self, borderwidth=0, highlightthickness=0)
        self.delete_btn_frame.pack(padx=(0, 20), pady=(10,0), side=LEFT, anchor=NW)      

        self.delete_btn=Button(self.delete_btn_frame, text="Delete", width=12, command=self.delete)  
        self.delete_btn.grid(row=0, column=0, padx=20)    

        self.btn_frame=Frame(self, borderwidth=0, highlightthickness=0)
        self.btn_frame.pack(padx=(0, 20), pady=(10,0), side=RIGHT, anchor=NE)

        self.close_btn=Button(self.btn_frame, text="Close", width=12, command=self.destroy)
        self.close_btn.grid(row=0, column=0, padx=20)

        self.save_button=Button(self.btn_frame, text="Save Changes", width=12, command=self.save)
        self.save_button.grid(row=0, column=1)

        self.insert_data_into_treeview()
        self.init_customer_fields()

    def create_data_from_list(self)->list:
            data=[]
            for c in self.dbh.customers:
                customer_details=(c.first_name,
                                  c.last_name,
                                  c.phone_num,
                                  c.email,
                                  c.address.postcode.postcode,
                                  c.address.postcode.city.name,
                                  c.address.address_line_1,
                                  c.address.address_line_2)
                                  
                data.append(customer_details)

            return data

    def insert_data_into_treeview(self) -> None:
        data=self.create_data_from_list()
        self.customer_tree.delete(*self.customer_tree.get_children())
        count=0
        for row in data:
            self.customer_tree.insert(parent="", index="end", iid=count, text="", values=row) 
            count+=1   

    def init_customer_fields(self) -> None:

        self.fn_entry.delete(0, END)
        self.ln_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.addr1_entry.delete(0, END)
        self.addr2_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.postcode_entry.delete(0, END)

        if self.customer is not None:

            address=self.customer.address

            self.fn_entry.insert(0, self.customer.first_name)
            self.ln_entry.insert(0, self.customer.last_name)
            self.email_entry.insert(0, self.customer.email)
            self.phone_entry.insert(0, self.customer.phone_num)
            self.addr1_entry.insert(0, address.address_line_1)
            self.addr2_entry.insert(0, address.address_line_2)
            self.city_entry.insert(0, address.postcode.city.name)
            self.postcode_entry.insert(0, address.postcode.postcode)

    def set_selected_customer(self) -> None:
        selected=self.customer_tree.focus()
        values=self.customer_tree.item(selected, "values")

        if values:
            self.customer=next(filter(lambda x: x.last_name==values[1] and x.email==values[3], 
                                      self.dbh.customers), None)
            
    def treeview_select(self, e: Event) -> None:
        self.set_selected_customer()
        self.init_customer_fields()
    
    def save(self) -> None:
        if self.customer is not None:
            address=self.customer.address
            postcode=address.postcode
            city=postcode.city

            if self.city_entry.get() != city.name:
                city=City(None, self.city_entry.get())
                city.id=self.dbh.insert_or_update_city(city)

            if self.postcode_entry.get() != postcode.postcode:
                postcode=Postcode(None, self.postcode_entry.get(), city)
                postcode.id=self.dbh.insert_or_update_postcode(postcode)

            addr1=self.addr1_entry.get()
            addr2=self.addr2_entry.get()

            if address.postcode.postcode==postcode.postcode:
                address.address_line_1=addr1
                address.address_line_2=addr2
            else:
                address=Address(None, addr1, addr2, postcode)

            address.id= self.dbh.insert_or_update_address(address)

            self.customer.first_name=self.fn_entry.get()
            self.customer.last_name=self.ln_entry.get()
            self.customer.email=self.email_entry.get()
            self.customer.phone_num=self.phone_entry.get()
            self.customer.address=address # do i need this? i don't think so

            self.dbh.insert_or_update_customer(self.customer)
            self.dbh.update()
            self.insert_data_into_treeview()
            self.clear_customer_fields()
            self.main_win.change_tree_data(main_window.ViewCommand.REFRESH)


    def delete(self) -> None:
        self.set_selected_customer()
        self.dbh.delete_customer(self.customer)
        self.dbh.update()
        self.insert_data_into_treeview()
        self.clear_customer_fields()
        self.main_win.change_tree_data(main_window.ViewCommand.REFRESH)

    def clear_customer_fields(self) -> None:

        self.fn_entry.delete(0, END)
        self.ln_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.addr1_entry.delete(0, END)
        self.addr2_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.postcode_entry.delete(0, END)
