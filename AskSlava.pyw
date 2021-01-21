import kivy 
import sqlite3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image


#SQLite connection#
conn = sqlite3.connect("data.db")
c = conn.cursor()



class MainWindow(Screen):
    pass

class Input(Screen):
    problem = ObjectProperty(None)
    solution = ObjectProperty(None) 
   ### Functions for inserting data into SQLite ###
    def btn(self):
       c.execute ("INSERT INTO issues VALUES (?,?)", (self.problem.text, self.solution.text))
       conn.commit()
       self.problem.text="Successfuly inputed Issue"  
       self.solution.text="Successfuly inputed Solution"
    def clear(self):
       self.problem.text=""  
       self.solution.text=""

class EditDelete(Screen):
    problemsrc = ObjectProperty(defaultvalue="Solution")
    solution = ObjectProperty(defaultvalue="The current solution will appear here")
    result = ObjectProperty(defaultvalue="The issue you're editing will appear here")
    updatesol= ObjectProperty(None)
    ### Functions for editing data into SQLite called from the KV file####
    def btnsrc(self):
       try:
           c.execute ("SELECT * FROM issues WHERE issue LIKE  ?", (self.problemsrc.text,))
           self.result = (c.fetchone()[0])
           c.execute ("SELECT * FROM issues WHERE issue LIKE  ?", (self.problemsrc.text,))
           self.solution = (c.fetchone()[1])
           
       except TypeError:
           self.solution = "Please dont use spaces and try using % at the end of your search"

    def btnupdate(self):
        c.execute("UPDATE issues SET solution =? WHERE issue = ?", (self.updatesol.text, self.result))
        self.solution = "Problem updated"
        self.result = ""
        conn.commit()
    def btndelete(self):
        c.execute("DELETE FROM issues WHERE issue = ?", (self.result,))
        self.solution = "Problem deleted"
        self.result = ""
        conn.commit()
    def clear(self):
        self.problemsrc.text = ""

class Search(Screen):
    result = ObjectProperty(defaultvalue="Your issue name will appear here.\n Your solution will appear here --->")
    solution = ObjectProperty(defaultvalue="Your solution will appear here.")
    problemsrc = ObjectProperty(defaultvalue="Solution")
    updatesrc = ObjectProperty(defaultvalue="Update here", rebind=True)
    
    ### Function for querying data from SQLite called from the KV file####
    def btnsrc(self):
       try:
           c.execute ("SELECT * FROM issues WHERE issue LIKE ? ", ('%'+self.problemsrc.text+'%',))
           self.result = (c.fetchone()[0])
           c.execute ("SELECT * FROM issues WHERE issue LIKE  ?", ('%'+self.problemsrc.text+'%',))
           self.solution = (c.fetchone()[1])
       except TypeError:
           self.solution = "Please dont use spaces and try using % at the end of your search"
    def clear(self):
        self.problemsrc.text = ""



   # kv class to organize screen order #    
class WindowManager(ScreenManager):
    pass


    # Kv file referance #            
kv = Builder.load_file("Style.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()