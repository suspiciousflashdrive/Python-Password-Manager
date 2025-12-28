import vault
import tkinter as tk
from tkinter import messagebox, ttk

tree = None
vault_pass = None
filename = None

def add_entry_gui():
    add_window = tk.Toplevel()
    add_window.title("Add Entry")
    add_window.geometry("300x180")
    add_window.resizable(False, False)

    tk.Label(add_window, text="URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    url_entry = tk.Entry(add_window, width=30)
    url_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    username_entry = tk.Entry(add_window, width=30)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(add_window, width=30, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    def confirm_add():
        url = url_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not url or not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        vault.add_entry(url, username, password)

        tree.insert(
            "",
            "end",
            values=(len(vault.data), url, username, password)
        )

        add_window.destroy()

    tk.Button(add_window, text="Add", command=confirm_add).grid(
        row=3, column=0, columnspan=2, pady=15
    )

def save_vault_gui():
    vault.save_vault(vault_pass, filename)
    messagebox.showinfo("Success", "Vault saved!")

def delete_selected():
    global tree
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected[0], "values")
    index = int(values[0]) - 1
    vault.delete(index)
    tree.delete(selected[0])

def show_vault_gui():
    global tree
    unlock_window.destroy()

    vault_window = tk.Tk()
    vault_window.title("Vault")
    vault_window.geometry("860x490")

    button_frame = tk.Frame(vault_window, bg="lightgray", height=40)
    button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,5))

    tk.Button(button_frame, text="Add Entry", command=add_entry_gui).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Delete Entry", command=delete_selected).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Save", command=save_vault_gui).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Quit", command=vault_window.destroy).grid(row=0, column=3, padx=5, pady=5)

    frame = tk.Frame(vault_window, bg="gray")
    frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    vault_window.grid_rowconfigure(1, weight=1)
    vault_window.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(frame, columns=("No.", "URL", "Username", "Password"), show="headings")
    tree.heading("No.", text="No.", anchor="w")
    tree.heading("URL", text="URL", anchor="w")
    tree.heading("Username", text="Username", anchor="w")
    tree.heading("Password", text="Password", anchor="w")
    tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

    tree.column("No.", width=40, anchor="w", stretch=False)
    tree.column("URL", width=200, anchor="w")
    tree.column("Username", width=200, anchor="w")
    tree.column("Password", width=200, anchor="w")

    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for i, entry in enumerate(vault.data, start=1):
        tree.insert("", "end", values=(i, entry["url"], entry["username"], entry["password"]))
    vault_window.mainloop()
# --- Unlock window ---
unlock_window = tk.Tk()
unlock_window.title("Password Manager")
unlock_window.geometry("350x137")

tk.Label(unlock_window, text="Vault filename:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
filename_entry = tk.Entry(unlock_window)
filename_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(unlock_window, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
password_entry = tk.Entry(unlock_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

def load_vault_gui():
    global filename, vault_pass
    vault_pass = password_entry.get()
    filename = filename_entry.get()
    try:
        vault.load_vault(password_entry.get(), filename_entry.get())
        messagebox.showinfo("Success", "Vault loaded!")
        show_vault_gui()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_vault_gui():
    try:
        vault.save_vault(password_entry.get(), filename_entry.get())
        messagebox.showinfo("Success", "Vault created!")
        show_vault_gui()
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(unlock_window, text="Load Vault", command=load_vault_gui).grid(row=2, column=0, padx=5, pady=10)
tk.Button(unlock_window, text="Create Vault", command=create_vault_gui).grid(row=2, column=1, padx=5, pady=10)

unlock_window.mainloop()
#choice = input("Enter 'load' or 'create': ")
#if choice == "load":
#    vault_file = input("Vault filename: ")
#    piss = input("Vault password: ")
#    vault.load_vault(piss, vault_file)  # updates vault.data
#elif choice == "create":
#    vault_file = input("Vault filename: ")
#    piss = input("Vault password: ")
#    vault.save_vault(piss, vault_file)

#while True:
#    choice2 = input("'add', 'remove', 'show', 'save', 'quit': ")
#    if choice2 == "add":
#        url = input("URL: ")
#        username = input("Username: ")
#        password = input("Password: ")
#        vault.add_entry(url, username, password)  # adds to vault.data
#    elif choice2 == "remove":
#        index = int(input("Index of entry to remove: ")) - 1
#        vault.delete(index)
#    elif choice2 == "show":
#        vault.show_vault()  # shows vault.data
#    elif choice2 == "save":
#        vault.save_vault(piss, vault_file)  # saves vault.data
#        print("Vault saved.")
#    elif choice2 == "quit":
#        break
