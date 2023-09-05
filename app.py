from flask import Flask, render_template ,request
from db import AccountInventory , AccountBalance , History

app = Flask(__name__)

@app.route("/")
def mainpage():
    account_inventory = AccountInventory()
    account_balance = AccountBalance()

    return render_template("mainpage.html",account_inventory=account_inventory.inventory , account_balance=account_balance.balance)


@app.route("/purchase-form" , methods=("POST","get"))
def purchase_form():
    account_inventory = AccountInventory()
    account_balance = AccountBalance()
    history_summary = History()
    if request.method =="POST":
        print(request.form)
        command_for_purchase_name=request.form.get("product-name")
        command_for_purchase_price=request.form.get("unit-price")
        command_for_purchase_pieces=request.form.get("pieces")
        total_cost = int(command_for_purchase_pieces) * int(command_for_purchase_price)

        if account_balance.balance >= total_cost:
            account_balance.balance -= total_cost
            if command_for_purchase_name in account_inventory.inventory:
                account_inventory.inventory[command_for_purchase_name] += command_for_purchase_pieces
            else:
                account_inventory.inventory[command_for_purchase_name] = command_for_purchase_pieces
                account_inventory.save_inventory()
                account_balance.save_balance()
                history_summary.history.append(f"{command_for_purchase_name} {command_for_purchase_pieces}(s) purchased")
                history_summary.save_history()

        else:
            print("Account balance is not enough for this purchase")

    return render_template("purchase-form.html")
    

@app.route("/sale_form" , methods=("POST","get"))
def sale_form():
    account_inventory = AccountInventory()
    account_balance = AccountBalance()
    history_summary = History()
    if request.method =="POST":
        print(request.form)
        command_for_sale_name =request.form.get("product-name-sale")
        command_for_sale_price=request.form.get("unit-price-sale")
        command_for_sale_quantity=request.form.get("pieces-sale")

        if command_for_sale_name in account_inventory.inventory and account_inventory.inventory[command_for_sale_name] >= int(command_for_sale_quantity):
            revenue= int(command_for_sale_price) * int(command_for_sale_quantity)
            account_balance.balance += revenue
            account_inventory.inventory[command_for_sale_name] -= int(command_for_sale_quantity)

            account_inventory.save_inventory()
            account_balance.save_balance()
            history_summary.history.append(f"{command_for_sale_name} {command_for_sale_quantity}(s) sold")
            history_summary.save_history()

        else:print(f"Insufficient inventory for {command_for_sale_name}")


    return render_template("sale_form.html")

@app.route("/balance-change-form", methods = ("POST","get"))
def balance_change_form():
    account_balance = AccountBalance()
    history_summary = History()
    if request.method == "POST":
        print(request.form)
        command_for_balance = request.form.get("type")
        balance_value = request.form.get("balance")
        if command_for_balance == "add":
            account_balance.balance += int(balance_value )
            history_summary.history.append(f"{balance_value} is added to the account")
        else:
            account_balance.balance -= int(balance_value )
            history_summary.history.append(f"{balance_value} is subtracted from the account")

        account_balance.save_balance()
        history_summary.save_history()

        

    return render_template("balance_change_form.html")



@app.route("/history" )
def histroy_func ():
    history_summary = History()
    
    return render_template("history.html",history_summary=history_summary.history)
    



    

