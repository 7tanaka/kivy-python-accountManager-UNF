from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
import sqlite3
import re

from matplotlib.pyplot import table
Window.size = (350, 580)

# from android.permission request_permission,Permission
# from jnius import autoclass
# Environment = autoclass('android.os.Environment')
# path = Environment.getExternalStorageDirectory().getAbsolutePath()



class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass

class UplockPage(MDApp):
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
   
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    database = sqlite3.connect(f"db/loginform.db")
    cursor = database.cursor()
    
    
    #? for login and signup database
    cursor.execute("create table if not exists logindata(email text, username text, password text)")
    #? for EZNOTES database
    #cursor.execute('DROP TABLE  notesdata1')
    cursor.execute("create table if not exists notesdata1( username text,title text, subject text, content text)")
        
    for row in cursor.execute("select * from notesdata1"): #! CHECLKING IF THE DATABASE IS WORKING!!
        print(row)
    
    def build(self):
       
        screen_manager = ScreenManager()
        
        screen_manager.add_widget(Builder.load_file(f"kvFiles/main.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/eznotes.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/accountslist.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/mainPanel.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/passgen.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/settings.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/signup.kv"))
        screen_manager.add_widget(Builder.load_file(f"kvFiles/login.kv"))
        
        
        return screen_manager
    
    def on_start(self):
        email = self.root.get_screen('login').ids.email.text
        password = self.root.get_screen('login').ids.password
        
        print(email)
    
    #? Button Animation for Toggling the Drawer Image
    def drawer_on(self):
        self.ids.my_image.source = 'assets/Images/logoBtn1.png'
    def drawer_off(self):
        self.ids.my_image.source = 'assets/Images/logoBtn2.png'

    #? Using the eye button to act as a button to see and unsee password              
    def toggle_visibility(self, password1):
        self.password1 = password1
        if self.password1.password == True:
            self.password1.password = False
        else:
            self.password1.password = True
    
    def current_user(self, email, password):
        a = self.receive_data(email, password)
        user_data = []
        #emailb = self.root.get_screen('login').ids.email.text
        
        #? checking if the email that was logged in is a username or a legit one
        #? the following line of code will be use to get the data about the user inside the database
        if(re.fullmatch(self.regex, email.text)): #! CHECKS IF THE USER INPUTS AT EMAIL OR NOT
            for row in self.cursor.execute(f"select * from logindata where email= '{email.text}'"):
                print(row)
                for i in row:
                    user_data.append(i)
        else:
             #TODO I CONVERTED THE EMAIL TO THE USERNAME IF ITS NOT AN EMAIL
            for row in self.cursor.execute(f"select * from logindata where username= '{email.text}'"):
                print(row)
                for i in row:
                    user_data.append(i)
        self.root.get_screen('mainPanel').ids.username1.text = user_data[1]
        self.root.get_screen('mainPanel').ids.email1.text = user_data[0]
        return a[0], a[1], user_data[1]

    def recNotes(self, username):
        
        self.cursor.execute(f"select title, subject, content from notesdata1 where username = '{username.text}'") #! SELECTS ALL THE DATA INSIDE THE LOGINDATA TABLE
        
        table = MDDataTable( #pos_hint ={'center_x': .5, 'center_y': .5},
                            #size_hint=(0.9, 0.6),
                column_data = [
                    ("Title", dp(15)),
                    ("Subject", dp(15)),
                    ("Content", dp(30))]
                # ],
                # row_data = [
                #     ('{title.text}'),
                #     ('{subject.text}'),
                #     ('{content.text}')
                # ]
                )
        
        
        return table
    
    
    def createNotes(self,username,title , subject, content):   
        
        self.cursor.execute(f"insert into notesdata1 values('{username.text}','{title.text}','{subject.text}','{content.text}')")
        self.database.commit() #! important to insert query to database
        title.text = ""
        subject.text = ""
        content.text = ""
        
     #! use for SIGN-UP FORM to send DATA TO THE DB
    def send_data(self,email,username, password): 
        if(re.fullmatch(self.regex, email.text)):
            self.cursor.execute(f"insert into logindata values('{email.text}','{username.text}','{password.text}')")
            self.database.commit() #! important to insert query to database
            email.text = ""
            username.text = ""
            password.text = ""
      
    #! function to receive data from mysql to python and validate it with textfield text
    def receive_data(self,email, password, state=False):
        self.state = state
        self.email = email #! I DECLARED THE EMAIL SO THAT IF ITS NOT AN EMAIL I CAN USE IT STILL
        self.cursor.execute("select * from logindata") #! SELECTS ALL THE DATA INSIDE THE LOGINDATA TABLE
        email_list = []
        username_list = []
        for i in self.cursor.fetchall(): #? ITERATE ALL THE DATA INSIDE AND APPENDS IT
            email_list.append(i[0])
            username_list.append(i[1])
        if(re.fullmatch(self.regex, email.text)): #! CHECKS IF THE USER INPUTS AT EMAIL OR NOT
           
            if email.text in email_list and email.text != "":
                self.cursor.execute(f"select password from logindata where email='{email.text}'")
                for j in self.cursor:
                    if password.text == j[0]:
                        print("You have Successfully Logged In!")
                       
                        
                        print(email.text)
                        return True, email.text
                    else:
                        print("Incorrect password!")
            else:
                print("incorrect Email")
                
            
        else:
            #TODO I CONVERTED THE EMAIL TO THE USERNAME IF ITS NOT AN EMAIL
            username = self.email
            if username.text in username_list and username.text != "":
                self.cursor.execute(f"select password from logindata where username='{username.text}'")
                for j in self.cursor:
                    if password.text == j[0]:
                        print("You have Successfully Logged In!")
                       
                        #print(username.text)
                        return True, username.text
                    else:
                        print("Incorrect password!")
                        return False
            else:
                print("incorrect username")
                return False
        
   
        
    
if __name__ == '__main__':
    LabelBase.register(name="Gonzi", fn_regular="C:\\Users\\mteno\\OneDrive\\Documents\\1myLearning\\CCNA-PYTHON ESSENTIALS\\1a-Python Projects\\Mine\\password_manager-UNFINISH\\gui_2\\assets\\fonts\\Gonzi-Light.otf")
    LabelBase.register(name="Theo", fn_regular="C:\\Users\\mteno\OneDrive\\Documents\\1myLearning\\CCNA-PYTHON ESSENTIALS\\1a-Python Projects\\Mine\\password_manager-UNFINISH\\gui_2\\assets\\fonts\\TheoriesRegular.ttf")
    LabelBase.register(name="stud", fn_regular="C:\\Users\\mteno\OneDrive\\Documents\\1myLearning\\CCNA-PYTHON ESSENTIALS\\1a-Python Projects\\Mine\\password_manager-UNFINISH\\gui_2\\assets\\fonts\\StudentReg.ttf")
    LabelBase.register(name="ranger", fn_regular="C:\\Users\\mteno\OneDrive\\Documents\\1myLearning\\CCNA-PYTHON ESSENTIALS\\1a-Python Projects\\Mine\\password_manager-UNFINISH\\gui_2\\assets\\fonts\\spacerangerbold.ttf")
    LabelBase.register(name="louis", fn_regular="C:\\Users\\mteno\OneDrive\\Documents\\1myLearning\\CCNA-PYTHON ESSENTIALS\\1a-Python Projects\\Mine\\password_manager-UNFINISH\\gui_2\\assets\\fonts\\LouisGeorge.ttf")
    
    
    
    UplockPage().run()
   