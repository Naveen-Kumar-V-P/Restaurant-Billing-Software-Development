
import csv

Menu_File = 'Training Project\Menu.csv'

class MenuManager():
    def __init__(self):
        self.menu=[]
        self.load_menu()

    def load_menu(self):
        try:
            with open(Menu_File , mode='r') as file:
                reader= csv.DictReader(file)
                self.menu = [row for row in reader]
        except FileNotFoundError :
            self.menu = []
    def Save_Menu(self):
        with open (Menu_File , mode = 'w' , newline = '') as file:
            field_Names = ['Code','Name','Price']
            writer = csv.DictWriter (field_Names=field_Names)
            writer.writeheader()
            writer.writeheader (self.menu)

    def add_item(self):
        Code = input("Enter item code:")
        Name = input("Enter item name:")
        Price = input("Enter item Price:")
        self.menu.append ({'Code': Code,'Name' : Name, 'Price' : Price})
        self.Save_Menu()
        print (f"Item {Name} added Sucessfully.")

    def View_Menu(Self):
        print ("\n ----------Menu----------")
        for item in Self.Menu:
            print (f"{item['Code']} - {item['Name']} - ${item['Price']}")
            print ("-------------------------------------------\n")






