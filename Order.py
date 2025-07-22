from datetime import datetime
import random


class OrderManager:
    def __init__(self,menu_manager, db_manager):
        self.menu = menu_manager.menu
        self.db = menu_manager.db


    def take_order(self):
        print ("\nPlace a New Order... ")
        Customer_Name = input("Customer name:")
        items=[]
        total = 0    

        while True:
            code = input("Enter item code (or 'Done' to finish):")
            if code.lower == 'Done':
                break
            item = next((item for item in self.menu if ['code'] == code ),None)
            if item :
                Qty = int(input("Enter Quantity:"))
                subtotal = float(item['Price'])*Qty
                items.append ((item['Name'],Qty,subtotal))
                total+=subtotal

            else:
                print("Item Not Found")

        print("\n------------Bill-------------")
        for name,Qty,subtotyal in items:
            print (f"{name} x{Qty} = ${subtotal:.2f}")
        print (f"Total:${total:.2f}")  

        self.db.insert_order(Customer_Name,items,total)  
        print ("Order Saved Sucessfully\n")


