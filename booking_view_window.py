from tkinter import *
from tkinter import ttk
from booking import Booking


class BookingViewWindow(Toplevel):
    def __init__(self, booking: Booking):
            super().__init__()

            self.title("Booking Details")
            self.geometry("950x430")
            self.resizable(False, False)

            self.booking=booking

            self.edit_frame=Frame(self, padx=20, pady=20, borderwidth=0, highlightthickness=0)
            self.edit_frame.pack(padx=20, pady=(20,10), anchor=W)
            
            self.customer_info_label=Label(self.edit_frame, text="Customer Info")
            self.customer_info_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
            self.fn_label=Label(self.edit_frame, text="First Name")
            self.fn_label.grid(row=1, column=0, sticky=E)
            self.fn_entry=Entry(self.edit_frame, width=50)
            self.fn_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

            self.ln_label=Label(self.edit_frame, text="Last Name")
            self.ln_label.grid(row=2, column=0, sticky=E)
            self.ln_entry=Entry(self.edit_frame, width=50)
            self.ln_entry.grid(row=2, column=1, padx=5, pady=5)

            self.phone_label=Label(self.edit_frame, text="Phone Number")
            self.phone_label.grid(row=3, column=0, sticky=NE)
            self.phone_entry=Entry(self.edit_frame, width=50)
            self.phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=N)

            self.email_label=Label(self.edit_frame, text="Email")
            self.email_label.grid(row=4, column=0, sticky=E)
            self.email_entry=Entry(self.edit_frame, width=50)
            self.email_entry.grid(row=4, column=1, padx=5, pady=5)

            self.billing_label=Label(self.edit_frame, text="Billing Address")
            self.billing_label.grid(row=5, column=1, padx=5, pady=(20,5), sticky=W)
            self.addr1_label=Label(self.edit_frame, text="Address Line 1")
            self.addr1_label.grid(row=6, column=0, padx=(20,0),sticky=E)
            self.addr1_entry=Entry(self.edit_frame, width=50)
            self.addr1_entry.grid(row=6, column=1, padx=5, pady=5)

            self.addr2_label=Label(self.edit_frame, text="Address Line 2")
            self.addr2_label.grid(row=7, column=0, padx=(20,0), sticky=E)
            self.addr2_entry=Entry(self.edit_frame, width=50)
            self.addr2_entry.grid(row=7, column=1, padx=5, pady=5)

            self.city_label=Label(self.edit_frame, text="City")
            self.city_label.grid(row=8, column=0, padx=(20,0), sticky=E)
            self.city_entry=Entry(self.edit_frame, width=50)
            self.city_entry.grid(row=8, column=1, padx=5, pady=5)

            self.postcode_label=Label(self.edit_frame, text="Postcode")
            self.postcode_label.grid(row=9, column=0, padx=(20,0), sticky=E)
            self.postcode_entry=Entry(self.edit_frame, width=25)
            self.postcode_entry.grid(row=9, column=1, padx=5, pady=5, sticky=W)

            self.booking_info_label=Label(self.edit_frame, text="Booking Details")
            self.booking_info_label.grid(row=0, column=3, padx=5, pady=5, sticky=W)
            self.castle_label=Label(self.edit_frame, text="Bouncy Castle")
            self.castle_label.grid(row=1, column=2, sticky=E)
            self.castle_entry=Entry(self.edit_frame, width=50)
            self.castle_entry.grid(row=1, column=3, padx=5, pady=5)

            self.date_label=Label(self.edit_frame, text="Date")
            self.date_label.grid(row=2, column=2, sticky=E)
            self.date_entry=Entry(self.edit_frame, width=25)
            self.date_entry.grid(row=2, column=3, padx=5, pady=5, sticky=W)

            self.price_label=Label(self.edit_frame, text="Price")
            self.price_label.grid(row=3, column=2, sticky=E)
            self.price_entry=Entry(self.edit_frame, width=25)
            self.price_entry.grid(row=3, column=3, padx=5, pady=5, sticky=W)

            self.delivery_label=Label(self.edit_frame, text="Delivery Address")
            self.delivery_label.grid(row=5, column=3, padx=5, pady=(20,5), sticky=W)

            self.del_addr1_label=Label(self.edit_frame, text="Address Line 1")
            self.del_addr1_label.grid(row=6, column=2, padx=(20,0),sticky=E)
            self.del_addr1_entry=Entry(self.edit_frame, width=50)
            self.del_addr1_entry.grid(row=6, column=3, padx=5, pady=5)

            self.del_addr2_label=Label(self.edit_frame, text="Address Line 2")
            self.del_addr2_label.grid(row=7, column=2, padx=(20,0), sticky=E)
            self.del_addr2_entry=Entry(self.edit_frame, width=50)
            self.del_addr2_entry.grid(row=7, column=3, padx=5, pady=5)

            self.del_city_label=Label(self.edit_frame, text="City")
            self.del_city_label.grid(row=8, column=2, padx=(20,0), sticky=E)
            self.del_city_entry=Entry(self.edit_frame, width=50)
            self.del_city_entry.grid(row=8, column=3, padx=5, pady=5)

            self.del_postcode_label=Label(self.edit_frame, text="Postcode")
            self.del_postcode_label.grid(row=9, column=2, padx=(20,0), sticky=E)
            self.del_postcode_entry=Entry(self.edit_frame, width=25)
            self.del_postcode_entry.grid(row=9, column=3, padx=5, pady=5, sticky=W)

            btn_frame=Frame(self, borderwidth=0, highlightthickness=0)
            btn_frame.pack(padx=(0, 50), anchor=NE)

            close_btn=Button(btn_frame, text="Close", width=12, command=self.destroy)
            close_btn.grid(row=0, column=0, padx=25)

            self.init_fields()


    def init_fields(self):
        if self.booking is not None:
            self.fn_entry.insert(0, self.booking.customer.first_name)
            self.ln_entry.insert(0, self.booking.customer.last_name)
            self.phone_entry.insert(0, self.booking.customer.phone_num)
            self.email_entry.insert(0, self.booking.customer.email)
            self.addr1_entry.insert(0, self.booking.customer.address.address_line_1)
            self.addr2_entry.insert(0, self.booking.customer.address.address_line_2)
            self.postcode_entry.insert(0, self.booking.customer.address.postcode.postcode)
            self.city_entry.insert(0, self.booking.customer.address.postcode.city.name)
            self.del_addr1_entry.insert(0, self.booking.delivery_address.address_line_1)
            self.del_addr2_entry.insert(0, self.booking.delivery_address.address_line_2)
            self.del_city_entry.insert(0, self.booking.delivery_address.postcode.city.name)
            self.del_postcode_entry.insert(0, self.booking.delivery_address.postcode.postcode)
            self.date_entry.insert(0, self.booking.date)
            self.castle_entry.insert(0, self.booking.bouncy_castle.name)
            self.price_entry.insert(0, self.booking.bouncy_castle.price.value)

            for child in self.edit_frame.winfo_children():
                 if child.__class__==Entry:
                    child.config(state=DISABLED, disabledbackground="white", disabledforeground="black")
         