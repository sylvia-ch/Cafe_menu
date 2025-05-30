
# Cafe Click and Collect App
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib # version 3 
import json
import os
import sys
import random

USER_FILE = "user_data.txt" #version3 
MENU_FILE = "menu_data.txt"

# hash

# GUI
class Cafeapp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Cafe Click and Collect App")
        self.win.geometry("500x400")

        # Data 
        self.users = self.load_users()
        self.menu = self.load_menu()
        self.order = []
        self.welcome_ui()
        self.win.mainloop()

    def clear(self):
        for w in self.win.winfo_children():
            w.destroy()

# Entry
# Welcome page
    def welcome_ui(self):
        self.clear()
        tk.Label(self.win, text="Welcome to Cafe Click and Collect",
                font=("Arial", 14)).pack(pady=30)
        bottns = tk.Frame(self.win)
        bottns.pack()
        tk.Button(bottns,text = "Login",width =12,
                command = self.login_ui).pack(side = "left", padx = 10)
        tk.Button(bottns,text = "Register",width =12,
                command = self.register_ui).pack(side = "left", padx = 10)   
        tk.Button(self.win,text = "Exit",
                command = self.win.quit).pack(pady = 25)


# Load user data
    def load_users(self):
        users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, encoding="utf-8") as f:
                for line in f:
                   if ":" in line:
                       username, psw = line.strip().split(":", 1)
                       users[username] = psw
        return users


    def append_user(self,username: str, psw: str):
        with open(USER_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username}:{psw}\n")
        self.users[username] = psw

# Menu
    def menu_ui(self):
        self.clear()
        self.menu = self.load_menu()
        tk.Label(self.win, text="Cafe Menu", font=("Arial", 15)).pack(pady=10)
    
        self.lst = tk.Listbox(self.win, width=40, height=10)
        for cai,value in self.menu.items():
            self.lst.insert(tk.END, f"{cai}: ${value:.2f}")
        self.lst.pack(pady=10)

        tk.Label(self.win, text="Quantity").pack()
        self.qty = tk.Spinbox(self.win, from_=1, to=10, width=5)
        self.qty.pack()
        
        f = tk.Frame(self.win); f.pack(pady=12)
        tk.Button(f, text="Add to Order", width=12,
                  command=self.add_to_order).grid(row=0, column=0, padx=8)
        tk.Button(f, text="Checkout", width=12,
                  command=self.checkout).grid(row=0, column=1, padx=8)
        tk.Button(self.win, text = "Logout",
                  command=self.welcome_ui).pack(pady=10)
        
    def add_to_order(self):
        sel = self.lst.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a menu item")
            return
        line = self.lst.get(sel[0])
        name = line.split(": $")[0]
        qty = int(self.qty.get())
        price = self.menu[name]
        self.order.append((name, price, qty))
        messagebox.showinfo("Item Added", f"{name} x {qty} added to your order")

        
    def load_menu(self) -> dict:
        if os.path.exists(MENU_FILE):
            menu = {}
            with open(MENU_FILE, encoding="utf-8") as f:
                for line in f:
                    if "," in line:
                       mingzi2,price = line.strip().split(",", 1)
                       menu[mingzi2] = float(price)
        print("DEBUG menu dict ->", menu) 
        return menu

# Login 
    def login_ui(self):
        self.clear()
        tk.Label(self.win, text="username",).pack(pady=4)
        self.ent_user = tk.Entry(self.win)
        self.ent_user.pack()
   
        tk.Label(self.win, text="password").pack(pady=4)
        self.ent_psw = tk.Entry(self.win, show="*")
        self.ent_psw.pack()
        box = tk.Frame(self.win)
        box.pack(pady=10)
        tk.Button(box, text="Login", width=10,
          command=self.do_login).pack(side="left", padx=6)
        tk.Button(box, text="Back", width=10,
          command=self.welcome_ui).pack(side="left", padx=6)


    def do_login(self):
        mingzi = self.ent_user.get().strip()
        psw = self.ent_psw.get().strip()
        stored_psw = self.users.get(mingzi)
        if self.users.get(mingzi) == psw:
           messagebox.showinfo("Login successful", f"Welcome {mingzi}!")
           self.menu_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        
# Register
    def register_ui(self):
       self.clear()
       tk.Label(self.win, text="Create Username").pack()
       self.ent_user = tk.Entry(self.win)
       self.ent_user.pack()

       tk.Label(self.win, text="Create Password,should be >=6").pack()
       self.ent_psw = tk.Entry(self.win, show="*")
       self.ent_psw.pack()

       f = tk.Frame(self.win); f.pack(pady=15)
       bottns = tk.Frame(self.win)
       bottns.pack(pady=10)
       tk.Button(f, text="Register", width=12,
                 command=self.do_register).grid(row=0, column=0, padx=8)
       tk.Button(f, text="Back", width=12,
                 command=self.welcome_ui).grid(row=0, column=1, padx=8)
       
    def do_register(self):
        mingzi = self.ent_user.get().strip()
        psw = self.ent_psw.get().strip()
        if not mingzi or mingzi in self.users:
            messagebox.showerror("Error", "Username exists or empty")
            return
        if len(psw) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        #psw_hash = hash_psw
        self.append_user(mingzi, psw)
        self.users[mingzi] = psw
        messagebox.showinfo("Registration Successful",
                    "You can now login with your credentials")
        self.welcome_ui()


# Order checkout
    def checkout(self):
        if not self.order:
            messagebox.showwarning("No Order", "Your order is empty")
            return
        total = sum(price*qty for _, price, qty in self.order)
        items = "\n".join(f"{items} * {price} = ${price*qty:.2f}" for items, price, qty in self.order)
        order_no = random.randint(100000, 999999)
        messagebox.showinfo("Order Confirmation",
                        f"{items}\n———\nTotal:${total:.2f}\nOrder Number: {order_no}")
        print("Thank you for your order! See you next time\n")
        self.order.clear()
        self.welcome_ui()
        

if __name__ == "__main__":
    Cafeapp()