from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import main_window
from db_helper import DBHelper
from bouncycastle import BouncyCastle


class CastleAddWindow(Toplevel):
    def __init__(self, dbh: DBHelper):
        super().__init__()

        self.dbh=dbh
        self.dimensions=self.dbh.dimensions
        self.colours=dbh.colours
        self.prices=dbh.prices

        self.dimension_values=[d.values for d in self.dimensions]
        self.colour_names=[c.name for c in self.colours]
        self.price_values=[p.value for p in self.prices]

        self.title("Add New Bouncy Castle")
        self.geometry("700x460")
        self.resizable(False, False)

        self.tree_frame=Frame(self)
        self.tree_frame.pack(padx=20, pady=(20,0))
        
        self.tree_yscroll=Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_yscroll.pack(side=RIGHT, fill=Y)
 

        self.castle_tree=ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_yscroll.set) 
        self.castle_tree.pack()

        self.tree_yscroll.config(command=self.castle_tree.yview)

        self.castle_tree["columns"] = ("Bouncy Castle Name", "Dimensions", "Main Colour", "Price")

        
        for col in self.castle_tree["columns"]:
            self.castle_tree.heading(col, text=f"{col}", anchor=CENTER)
        
        
        self.castle_tree.column("Bouncy Castle Name", width=200, stretch=NO)
        self.castle_tree.column("Dimensions", width=150, stretch=NO)
        self.castle_tree.column("Main Colour", width=150, stretch=NO)
        self.castle_tree.column("Price", width=100, stretch=NO)

        self.castle_tree.column("#0", width=0, stretch=NO)
        self.castle_tree.heading("#0", text="", anchor=E)

        self.castle_frame=LabelFrame(self, padx=20, pady=10, borderwidth=0, highlightthickness=0)
        self.castle_frame.pack(padx=20, pady=20, side=LEFT, anchor=SE)

        self.castle_label=Label(self.castle_frame, text="Bouncy Castle Name")
        self.castle_label.grid(row=0, column=0, sticky=E)
        self.castle_entry=Entry(self.castle_frame, width=33)
        self.castle_entry.grid(row=0, column=1, padx=5, pady=10)

        self.dimension_label=Label(self.castle_frame, text="Dimension")
        self.dimension_label.grid(row=1, column=0, sticky=E)
        self.dimension_combobox=ttk.Combobox(self.castle_frame, width=30, values=self.dimension_values)
        self.dimension_combobox.grid(row=1, column=1, padx=5, pady=10, sticky=W)

        self.colour_label=Label(self.castle_frame, text="Main Colour")
        self.colour_label.grid(row=2, column=0, sticky=E)
        self.colour_combobox=ttk.Combobox(self.castle_frame, width=30, values=self.colour_names)
        self.colour_combobox.grid(row=2, column=1, padx=5, pady=10, sticky=W)

        self.price_label=Label(self.castle_frame, text="Price")
        self.price_label.grid(row=3, column=0, sticky=E)
        self.price_combobox=ttk.Combobox(self.castle_frame, width=30, values=self.price_values)
        self.price_combobox.grid(row=3, column=1, padx=5, pady=10, sticky=W)


        self.btn_frame=Frame(self, borderwidth=0, highlightthickness=0)
        self.btn_frame.pack(padx=(0, 30), pady=(10,0), side=RIGHT, anchor=SE)

        self.save_btn=Button(self.btn_frame, text="Add Bouncy Castle", width=15, command=self.save)
        self.save_btn.grid(row=0, column=0, padx=(10,20), pady=20)
        
        self.close_btn=Button(self.btn_frame, text="Close", width=15, command=self.destroy)
        self.close_btn.grid(row=1, column=0, padx=(10,20), pady=(0,40))

        self.init_castle_fields()
        self.insert_data_into_treeview()

    def init_castle_fields(self) -> None:
        self.castle_entry.delete(0,END),
        self.dimension_combobox.current(0)
        self.colour_combobox.current(0)
        self.price_combobox.current(0)

    def save(self) -> None:
        bouncy_castles=self.dbh.get_all_bouncy_castles()
        castle_names=[c.name for c in bouncy_castles]

        name_error=""

        if self.castle_entry.get() in castle_names:
            messagebox.showerror("Duplicate name", "This name already belongs to abouncy castle, please modify it or choose another one.", parent=self)
            
        if not self.castle_entry.get():
            messagebox.showerror("Empty field", "Please specify a name to save bouncy castle.", parent=self)
            
        if not name_error:
            bouncy_castle=BouncyCastle(None, 
                                       self.castle_entry.get(),
                                       next(filter(lambda x: x.values==self.dimension_combobox.get(), 
                                                   self.dimensions), None),
                                       next(filter(lambda x: x.name==self.colour_combobox.get(), 
                                                   self.colours), None),
                                       next(filter(lambda x: x.value==self.price_combobox.get(), 
                                                   self.prices), None))
                        
            self.dbh.insert_or_update_bouncy_castle(bouncy_castle)
            self.dbh.update()
            self.insert_data_into_treeview()
            self.init_castle_fields()

    def create_data_from_castles(self):
                data=[] 
                for castle in self.dbh.bouncy_castles:
                    castle_details=(castle.name,
                                    castle.dimension.values,
                                    castle.colour.name,
                                    castle.price.value)                  
                    data.append(castle_details)
                
                return data        
            
    def insert_data_into_treeview(self) -> None: 
            data=self.create_data_from_castles()
            self.castle_tree.delete(*self.castle_tree.get_children())
            count=0
            for row in data:
                self.castle_tree.insert(parent="", index="end", iid=count, text="", values=row) 
                count+=1   
            
            
