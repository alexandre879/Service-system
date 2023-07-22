import random
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Menu dictionary with items and prices
menu = {
    1: {'food': 'Pizza', 'price': 3.50},
    2: {'food': 'Hamburger', 'price': 2.50},
    3: {'food': 'Hotdog', 'price': 1.50},
    4: {'food': 'Salad', 'price': 1.80},
    5: {'food': 'Fries', 'price': 1.50},
}

# Dictionary to store selected items and quantities
selected_items = {}
total_price = 0

def show_menu():
    choice_entry.config(state='enabled')
    menu_text.configure(state='normal')
    for key, item in menu.items():
        menu_text.insert(END, f"{key}) {item['food']} - ${item['price']:.2f}\n")
    menu_text.insert(END, 'Press (0) to quit the menu.\n')
    menu_text.insert(END, 'Press (R) for a random recommendation.\n')
    menu_text.insert(END, 'Press (S) to view selected items.\n')
    menu_text.insert(END, 'Press (P) to proceed to checkout.\n')
    menu_text.insert(END, '__________________\n\n')
    menu_text.configure(state='disabled')
    choice_button.configure(state='enabled')
    menu_button.configure(state='enabled')
    menu_button.configure(state='enabled')

    
    if len(menu_text.get(1.0, END).strip()) > 0:
        clear_button.configure(state='enabled')
        menu_button.configure(state='disabled')
    
    else:
        clear_button.configure(state='disabled')
        menu_button.configure(state='enabled')




        


def process_choice():
    global total_price
    global selected_items

    choice = choice_entry.get().strip().lower()

    if choice.isdigit():
        choice = int(choice)
        
        if choice in menu:
            quantity = 1 
            if choice in selected_items:
                quantity += selected_items[choice]
            
            selected_items[choice] = quantity
            selected_item = menu[choice]
            price = selected_item['price'] * quantity
            total_price += price
            menu_text.configure(state='normal')
            menu_text.insert(END, f'\nYou have ordered ({selected_item["food"]} - x{quantity}) for (${price:.2f})\n')
            menu_text.configure(state='disabled')
        
        elif choice == 0:
            exit_request = messagebox.askquestion('Confirmation', 'Are you sure you want to quit the menu?')
            
            if exit_request == 'yes':
                messagebox.showinfo('Menu', 'Menu canceled. Thank you for using our menu.')
                root.destroy()
        
        else:
            messagebox.showerror('Error', 'Invalid input. Please enter a number within our menu range.')
    
    elif choice == 'r':
        random_item = random.choice(list(menu.values()))
        quantity = 1
        
        if random_item in selected_items:
            quantity += selected_items[random_item]
        
        selected_items[random_item] = quantity
        price = random_item['price'] * quantity
        total_price += price
        menu_text.configure(state='normal')
        menu_text.insert(END, f"We recommend ({random_item['food']}) x {quantity} for (${price:.2f})\n")
        menu_text.configure(state='disabled')

    elif choice == 's':
        
        if len(selected_items) > 0:
            menu_text.configure(state='normal')
            menu_text.insert(END, 'You have selected the following items:\n')
            
            for choice, quantity in selected_items.items():
                item = menu[choice]
                price = item['price'] * quantity
                menu_text.insert(END, f"({item['food']} x {quantity}) - (${price:.2f})\n")
            menu_text.configure(state='disabled')
        
        else:
            messagebox.showinfo('Information', 'To view selected items, you must select at least one item.')

    elif choice == 'p':
        if len(selected_items) > 0:
            checkout_request = messagebox.askquestion('Confirmation', 'Are you sure you want to proceed to checkout?')
            if checkout_request == 'yes':
                menu_text.configure(state='normal')
                menu_text.insert(END, '\nProceeding to checkout..\n')
                menu_text.insert(END, 'You have ordered the following items:\n')
                for choice, quantity in selected_items.items():
                    item = menu[choice]
                    menu_text.insert(END, f"({item['food']} - x{quantity})\n")
                menu_text.insert(END, f'Your total payable is (${total_price:.2f})\n')
                menu_text.configure(state='disabled')
                choice_entry.config(state='disabled')
            
            else:
                messagebox.showinfo('Menu', 'Menu is still in process. Please continue selecting an item.')
        
        else:
            messagebox.showinfo('Information', 'To proceed to checkout, you must order at least one item.')
    
    else:
        messagebox.showerror('Error', 'Invalid input! Please enter a number or letter within our menu range.')

    choice_entry.delete(0, END)

def clear_selection():
    clear_request = messagebox.askquestion('Confirmation', 'Are you sure you want to delete menu text and selected item together?')
    if clear_request == 'yes':
        selected_items.clear()
        menu_text.configure(state='normal')
        menu_text.delete(1.0, END)
        menu_text.configure(state='disabled')
        clear_button.configure(state='disabled')
        choice_button.configure(state='disabled')
        menu_button.configure(state='enabled')

root = Tk()
root.title('Menu Service')

# Styling
root.geometry("400x400")
root.config(bg="#f2f2f2")
root.resizable(0, 0)

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Arial", 12),
                padding=5,
                background="#f39c12",
                foreground="#ffffff")
style.map("TButton",
          background=[('active', '#e67e22')])
style.configure("TLabel",
                font=("Arial", 12),
                background="#f2f2f2",
                foreground="#333333")
style.configure("TEntry",
                font=("Arial", 12),
                padding=5)

title_label = ttk.Label(root, text='Menu', style="TLabel")
title_label.pack(pady=10)

menu_frame = Frame(root, bg="#f2f2f2")
menu_frame.pack(pady=10)

menu_text = Text(menu_frame, height=10, width=40, font=('Arial', 12), bd=0)
menu_text.pack(side=LEFT, padx=10)
menu_text.configure(state='disabled')

menu_scrollbar = Scrollbar(menu_frame)
menu_scrollbar.pack(side=RIGHT, fill=Y)


menu_text.config(yscrollcommand=menu_scrollbar.set)
menu_scrollbar.config(command=menu_text.yview)

choice_frame = Frame(root, bg="#f2f2f2")
choice_frame.pack(pady=10)

choice_label = ttk.Label(choice_frame, text='Enter your choice:', style="TLabel")
choice_label.pack(side=LEFT, padx=10)

choice_entry = ttk.Entry(choice_frame, width=30)
choice_entry.pack(side=LEFT)

button_frame = Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

menu_button = ttk.Button(button_frame, text='Show Menu', command=show_menu, style="TButton")
menu_button.pack(side=LEFT, padx=10)

choice_button = ttk.Button(button_frame, text='Submit', command=process_choice, style="TButton", state='disabled')
choice_button.pack(side=LEFT)

clear_button = ttk.Button(button_frame, text='Clear Selection', command=clear_selection, style="TButton", state='disabled')
clear_button.pack(side=LEFT)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', pady=10)

footer_label = ttk.Label(root, text='🍔 www.websitename.com 🍔', style="TLabel")
footer_label.pack()

root.mainloop()
