from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_helper import DBHelper
import main_window


class CastleWindow(Toplevel):
     def __init__(self, dbh: DBHelper, main_win: main_window):
        super().__init__()

        self.dbh=dbh
        self.main_win=main_win
        self.castle=None
        self.dimension_values=[str(d) for d in self.dbh.dimensions]
        self.colour_names=[str(c) for c in self.dbh.colours]
        self.price_values=[str(p) for p in self.dbh.prices]

        self.title("View and Edit Bouncy Castles")
        self.geometry("700x500")
        self.resizable(False, False)

        self.tree_frame=Frame(self)
        self.tree_frame.pack(padx=20, pady=(20,0))
        
        self.tree_yscroll=Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_yscroll.pack(side=RIGHT, fill=Y)
 

        self.castle_tree=ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_yscroll.set, selectmode="extended") 
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

        self.castle_tree.bind("<<TreeviewSelect>>", self.treeview_select)

        self.castle_frame=LabelFrame(self, padx=20, pady=10, borderwidth=0, highlightthickness=0)
        self.castle_frame.pack(padx=20, pady=20, side=LEFT, anchor=NE)

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
        self.btn_frame.pack(padx=(20,40), pady=20, side=RIGHT)

        self.save_btn=Button(self.btn_frame, text="Save Changes", width=12, command=self.save)
        self.save_btn.grid(row=0, column=0, padx=(10,20), pady=20)

        self.delete_btn=Button(self.btn_frame, text="Delete", width=12, command=self.delete)
        self.delete_btn.grid(row=1, column=0, padx=(10,20))

        self.close_btn=Button(self.btn_frame, text="Close", width=12, command=self.destroy)
        self.close_btn.grid(row=2, column=0, padx=(10,20), pady=20)       

        self.insert_data_into_treeview()
        self.get_selected_castle()
        self.init_castle_fields()

     def create_data_from_castles(self) -> list:
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

     def get_selected_castle(self) -> None:
          selected=self.castle_tree.focus()
          values=self.castle_tree.item(selected, "values")

          if values:
                self.castle=next(filter(lambda x: x.name==values[0], self.dbh.bouncy_castles), None)  

     def init_castle_fields(self) -> None:
         if self.castle is not None:
              self.castle_entry.delete(0, END)
              self.castle_entry.insert(0, self.castle.name)
              self.dimension_combobox.current(self.dimension_values.index(str(self.castle.dimension)))
              self.colour_combobox.current(self.colour_names.index(str(self.castle.colour)))
              self.price_combobox.current(self.price_values.index(str(self.castle.price)))
         else:
              self.dimension_combobox.current(0)
              self.colour_combobox.current(0)
              self.price_combobox.current(0)      

     def treeview_select(self, e: Event) -> None:
         self.get_selected_castle()
         self.init_castle_fields()             


     def delete(self) -> None:
         if self.castle is not None:
              cname=self.castle_entry.get()
              castle_names=[str(c) for c in self.dbh.bouncy_castles]
              available_castles=self.dbh.get_all_non_booked_bouncy_castles();
              
              if cname not in castle_names:
                   messagebox.showerror("Cannot delete bouncy castle", 
                                        "Cannot delete a bouncy castle that is being edited", parent=self)
              elif not available_castles:
                    messagebox.showerror("No castles to delete", 
                                        "All the bouncy castles are booked, none can be deleted", parent=self)
              elif self.castle not in available_castles:
                    messagebox.showerror("Cannot delete bouncy castle", 
                                        "Cannot delete a bouncy castle that is booked", parent=self)
              else:
                   self.dbh.delete_bouncy_castle(self.castle)
                   self.dbh.update()
                   self.castle=None
                   self.insert_data_into_treeview()
                   self.init_castle_fields
                   self.main_win.change_tree_data(main_window.ViewCommand.REFRESH)
         else:
              messagebox.showerror("Castle None", "Please select a bouncy castle from the table to delete", parent=self)
                
     def save(self) -> None:   
         if self.castle is not None:
               self.castle.name=self.castle_entry.get()
               self.castle.dimension=next(filter(lambda x: str(x)==self.dimension_combobox.get(), 
                                                  self.dbh.dimensions), None)
               self.castle.colour=next(filter(lambda x: str(x)==self.colour_combobox.get(), 
                                                  self.dbh.colours), None)
               self.castle.price=next(filter(lambda x: str(x)==self.price_combobox.get(), 
                                                  self.dbh.prices), None)
               
               self.dbh.insert_or_update_bouncy_castle(self.castle)
               self.dbh.update()
               self.insert_data_into_treeview()
               self.get_selected_castle()  
         else:
              messagebox.showerror("Castle None", "Please select a bouncy castle from the table to edit", parent=self)

