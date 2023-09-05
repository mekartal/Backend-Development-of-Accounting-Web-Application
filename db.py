import os
import json

class AccountInventory:
    def __init__(self, db_path="database"):
        self.inventory = {}  
        self.inventory_db_path = os.path.join(db_path, "inventory.json")
        self.load_inventory()

    def load_inventory(self):
        with open(self.inventory_db_path) as f:
            data = json.load(f)
            self.inventory = data.get("inventory", {})
            for key, value in self.inventory.items():
                self.inventory[key] = int(value)

    def save_inventory(self):
        data = {"inventory": self.inventory}
        with open(self.inventory_db_path, "w") as f:
            json.dump(data, f)


class AccountBalance:
    def __init__(self,db_path="database"):
        self.balance = 0
        self.balance_db_path=os.path.join(db_path ,"balance.json")
        self.load_balance()

    def load_balance(self):
        with open (self.balance_db_path) as f:
            self.balance=json.load(f)

    def save_balance(self):
        with open (self.balance_db_path,"w")as f:
            json.dump(self.balance,f)

class History:
    def __init__(self,db_path= "database"):
        self.history=[]
        self.history_db_path = os.path.join(db_path, "history.json")
        self.load_history()

    def load_history(self):
        with open(self.history_db_path) as f:
            self.history=json.load(f)

    def save_history(self):
        with open (self.history_db_path,"w")as f:
            json.dump(self.history,f)

    

