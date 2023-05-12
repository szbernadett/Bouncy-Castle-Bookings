from tkinter import *
from db_helper import DBHelper
from PIL import ImageTk, Image

class SQLWindow(Toplevel):
    def __init__(self, dbh: DBHelper):
        super().__init__()

        self.dbh=dbh

        self.title("Execute SQL")
        self.geometry("1200x550")
        self.resizable(False, False)

        self.canvas=Canvas(self, width=700, height=480, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas.pack(padx=20, pady=20, side=LEFT, anchor=NE)
            
        self.img=Image.open("erd4.jpg")
        self.img=self.img.resize((700, 450), Image.ANTIALIAS)
        self.img=ImageTk.PhotoImage(self.img)
        self.canvas.create_image(10, 10, anchor=NW, image=self.img)

        self.query_frame=Frame(self, borderwidth=0, highlightthickness=0)
        self.query_frame.pack(padx=(10,30), pady=30, side=RIGHT, anchor=NW)

        self.query_label=Label(self.query_frame, text="SQL Query / Statement:")
        self.query_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.sql_txt=Text(self.query_frame, height=6, width=50, padx=10, pady=5)
        self.sql_txt.grid(row=1, column=0, padx=5, pady=5)

        self.execute_btn=Button(self.query_frame, text="Execute", width=12, command=self.execute_sql)
        self.execute_btn.grid(row=2, column=0, pady=(20,0))

        self.output_label=Label(self.query_frame, text="Output:")
        self.output_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.output_txt=Text(self.query_frame, height=12, width=50, padx=10, pady=5)
        self.output_txt.grid(row=4, column=0, padx=5, pady=5)

        self.close_btn=Button(self.query_frame, text="Close", width=12, command=self.destroy)
        self.close_btn.grid(row=5, column=0, pady=20)

    def execute_sql(self) -> None:

        self.output_txt.delete("1.0", END)

        sql=self.sql_txt.get("1.0", "end-1c")

        results=self.dbh.custom_sql(sql)

        self.output_txt.insert(END, sql+"\n\n")
        self.sql_txt.delete("1.0", END)

        for res in results:
            self.output_txt.insert(END, str(res)+"\n")