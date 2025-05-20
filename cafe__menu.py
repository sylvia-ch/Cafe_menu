
# Cafe Click and Collect App
import os
import sys
import random

USER_FILE = "user_data.txt"
MENU_FILE = "menu_data.txt"


# Entry
def main():
    users = load_users()
    menu = load_menu()

    print("Welcome to Café Click and Collect App")
    if input("Do you have an account? (yes/no): ").strip().lower() == "yes":
        login(users)
    else:
        register(users)

    main_menu(menu)


def load_users() -> dict:
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":", 1)
                    users[u] = p
    return users


def save_user(username: str, password: str) -> None:
    with open(USER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{password}\n")


def load_menu() -> dict:
    menu = {}
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    name, price = line.strip().split(",", 1)
                    menu[name] = float(price)
    else: 
        menu = {"Coffee": 2.5, "Hot Chocolate": 2.0, "Sandwich": 4.5}
    print("DEBUG menu dict ->", menu) 
    return menu

def login(users: dict) -> bool:
    while True:
        user = input("Enter Username: ").strip()
        pwd = input("Enter Password: ").strip()
        if users.get(user) == pwd:
            print("Login successful!\n")
            return True
        print("Invalid credentials, try again\n")


def register(users: dict) -> bool:
    while True:
        user = input("Create Username: ").strip()
        if user in users:
            print("Username already exists, try again\n")
            continue
        pwd = input("Create Password (≥6 chars): ").strip()
        if len(pwd) < 6:
            print("Password too short, try again\n")
            continue
        # Save and undate users
        save_user(user, pwd)
        users[user] = pwd
        print("Registration successful!\n")
        return True


# Main menu and order
def main_menu(menu: dict):
    order = []
    total = 0.0
    while True:
        print("\nCafe Menu")
        for item, price in menu.items():
            print(f"{item:<15} ${price:.2f}")
        sel = input("\nEnter item to order (or 'done' to finish): ").strip()
        if sel.lower() == "done":
            break
        if sel not in menu:
            print("Item not found, try again")
            continue
        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity, try again")
            continue
        order.append((sel, qty, menu[sel]))
        total += menu[sel] * qty
        print(f"Added {qty} x {sel}\n")
    display_summary(order, total)


# Order checkout
def display_summary(order: list, total: float):
    print("\n===== Your Order =====")
    for item, qty, price in order:
        print(f"{item:<15} ×{qty:<3} ${price*qty:.2f}")
    print(f"\nTotal Price: ${total:.2f}")
    order_no = random.randint(100000, 999999)
    print(f"Order Number: {order_no}")
    print("Thank you for your order! See you next time\n")
    sys.exit()



if __name__ == "__main__":
    main()
