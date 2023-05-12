from tkinter import *
from tkinter import ttk
import booking_edit_window
from booking_add_window import BookingAddWindow
from booking_view_window import BookingViewWindow
from customer_window import CustomerWindow
from customer_add_window import CustomerAddWindow
from castle_window import CastleWindow
from castle_add_window import CastleAddWindow
from db_helper import DBHelper
from context_manager import ContextManager
from booking import Booking
from enum import Enum
from sql_window import SQLWindow
from search_bookings_window import SearchBookingsWindow

class MainWindow(Tk):
    
    
    def __init__(self):
        super().__init__()
        self.cm=ContextManager("BouncyCastleBookings.db")
        self.dbh=DBHelper(self.cm)
        self.booking=None

        self.title("Bouncy Castles Bookings")
        self.geometry("950x500")
        self.resizable(False, False)

        self.main_menu=Menu(self)
        self.config(menu=self.main_menu)

        self.castle_menu=Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Bouncy Castles", menu=self.castle_menu)
        self.castle_menu.add_command(label="View and Edit", command=lambda: CastleWindow(self.dbh, self))
        self.castle_menu.add_command(label="Add New", command=lambda: CastleAddWindow(self.dbh))

        self.customer_menu=Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Customers", menu=self.customer_menu)
        self.customer_menu.add_command(label="View and Edit", command=lambda: CustomerWindow(self.dbh, self))
        self.customer_menu.add_command(label="Add New", command=lambda: CustomerAddWindow(self.dbh))

        self.sql_menu=Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="SQL", menu=self.sql_menu)
        self.sql_menu.add_command(label="Execute SQL", command=lambda: SQLWindow(self.dbh))

        self.search_menu=Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Search", menu=self.search_menu)
        self.search_menu.add_command(label="Search Bookings", command=lambda: SearchBookingsWindow(self.dbh))

    

        self.current_view=ViewMode.TODAY
        self.view_mode_data={ViewMode.TODAY: self.dbh.get_bookings_today,
                             ViewMode.BEFORE: self.dbh.get_bookings_previous_day,
                             ViewMode.AFTER: self.dbh.get_bookings_next_day,
                             ViewMode.ALL: self.dbh.get_all_bookings}
                
        self.button_frame=LabelFrame(self, text="Select day")
        self.button_frame.grid(row=0, column=0, pady=20)

        self.before_button=Button(self.button_frame, text="<", padx=20, command=lambda: 
                             self.change_tree_data(ViewCommand.PREVIOUS))
        self.before_button.grid(row=0, column=0, padx=10, pady=10)
        self.day_label=Label(self.button_frame, text=self.current_view, width=20)
        self.day_label.grid(row=0, column=1, padx=10, pady=10)
        self.after_button=Button(self.button_frame, text=">", padx=20, command=lambda: 
                            self.change_tree_data(ViewCommand.NEXT))
        self.after_button.grid(row=0, column=2, padx=10, pady=10)

        self.tree_frame=Frame(self)
        self.tree_frame.grid(row=1, column=0, padx=(40,20))
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
        self.booking_tree.bind("<ButtonRelease-1>", self.get_selected_booking)   

        self.button_frame_side=LabelFrame(self, borderwidth=0, highlightthickness=0)
        self.button_frame_side.grid( row=1, column=1)

        self.edit_button=Button(self.button_frame_side, text="Edit", padx=5,
                                command=lambda: booking_edit_window.BookingEditWindow(self.booking, 
                                                                                      self.dbh, 
                                                                                      self))
        self.edit_button.grid(row=1,column=0, padx=10, pady=10, sticky="ew")

        self.delete_button=Button(self.button_frame_side, text="Delete", padx=5, command=lambda: 
                                  self.delete_booking())
        self.delete_button.grid(row=2,column=0, padx=10, pady=10, sticky="ew")

        self.view_details_button=Button(self.button_frame_side, text="View Details", padx=5, 
                                 command=lambda: BookingViewWindow(self.booking))
        self.view_details_button.grid(row=3,column=0, padx=10, pady=10, sticky="ew")

        self.view_all_button=Button(self.button_frame_side, text="View All", padx=5, 
                              command=lambda: self.change_tree_data(ViewCommand.SHOW_ALL))
        self.view_all_button.grid(row=4,column=0, padx=10, pady=10, sticky="ew")

        self.reset_button=Button(self.button_frame_side, text="Reset View", padx=5, command=lambda: 
                            self.change_tree_data(ViewCommand.RESET))
        self.reset_button.grid(row=5,column=0, padx=10, pady=10, sticky="ew")


        self.add_button=Button(self, text="Add", padx=20, pady=20, 
                               command=lambda: BookingAddWindow(self.dbh, self))
        self.add_button.grid(row=2, column=0, padx=20, pady=20)

        self.exit_button=Button(self, text="Exit", padx=20, pady=20, command=self.destroy)
        self.exit_button.grid(row=2, column=1)

        self.insert_data_into_treeview(self.dbh.get_bookings_today())
        self.change_tree_data(ViewCommand.REFRESH)
    
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

    def get_selected_booking(self, *args) -> None:
        selected=self.booking_tree.focus()
        values=self.booking_tree.item(selected, "values")

        if values:
            self.booking=next(
                    filter(lambda x: x.date==values[0] 
                           and x.bouncy_castle.name==values[1], 
                           self.dbh.bookings), 
                           None)
            

    def swap_view_mode(self, view_mode: Enum, bookings: list) -> None:
        self.insert_data_into_treeview(bookings)
        self.day_label.config(text=view_mode.value)
        self.current_view=view_mode

    def change_tree_data(self, view_command: Enum) -> None:

            
        match view_command:

            case ViewCommand.NEXT:
                match self.current_view:
                    case ViewMode.BEFORE:
                        self.swap_view_mode(ViewMode.TODAY, self.view_mode_data[ViewMode.TODAY]())
                    case ViewMode.TODAY:
                        self.swap_view_mode(ViewMode.AFTER, self.view_mode_data[ViewMode.AFTER]())        
                        
            case ViewCommand.PREVIOUS:
                match self.current_view:
                    case ViewMode.TODAY:
                        self.swap_view_mode(ViewMode.BEFORE, self.view_mode_data[ViewMode.BEFORE]())
                    case ViewMode.AFTER:
                        self.swap_view_mode(ViewMode.TODAY, self.view_mode_data[ViewMode.TODAY]())

            case ViewCommand.SHOW_ALL:
                self.swap_view_mode(ViewMode.ALL, self.view_mode_data[ViewMode.ALL]())
                self.after_button.config(state="disabled")
                self.before_button.config(state="disabled")

            case ViewCommand.RESET:
                self.swap_view_mode(ViewMode.TODAY, self.view_mode_data[ViewMode.TODAY]())
                self.after_button.config(state="normal")
                self.before_button.config(state="normal")

            case ViewCommand.REFRESH:
                self.swap_view_mode(self.current_view, self.view_mode_data[self.current_view]())

        self.booking=self.get_selected_booking() 


    def delete_booking(self) -> None:
            if self.booking is not None:
                self.dbh.delete_booking(self.booking)
                self.change_tree_data(ViewCommand.REFRESH)


    
       
        

class ViewMode(Enum):
        AFTER="Day After"
        TODAY="Today"
        BEFORE="Day Before"
        ALL="All Bookings"  


class ViewCommand(Enum):
        NEXT="next"
        PREVIOUS="previous"
        SHOW_ALL="all"
        REFRESH="refresh"
        RESET="reset"

        
    