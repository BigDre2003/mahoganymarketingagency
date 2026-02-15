import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from business.authentication import AuthenticationService
from business.inventory import InventoryManager
from business.employee_management import EmployeeManager
from business.request import RequestManager
from datetime import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class EquipmentApp:
    def __init__(self, root):
        #Create a window and center it
        self.root = root
        self.root.title("Equipment Tracking System")
        appWidth = 700
        appHeight = 520
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.root.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")
        
        # Business logic instances
        self.auth = AuthenticationService()
        self.inventory = InventoryManager()
        self.employee = EmployeeManager()
        self.request = RequestManager()

        #create list for equipment stock
        self.quantityList = []
        self.user = ''
        self.equipment_name = ''

        # Use ttk styles for a cleaner look
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6, foreground="white", 
                background="#f4f4f9")
        style.configure("TLabel", font=("Arial", 11), background="#f4f4f9")
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#f4f4f9")

        self.build_login_screen()

    #Build the login screen
    def build_login_screen(self):
        self.clear_root()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="Equipment Tracking System", style="Header.TLabel").pack(pady=15)

        ttk.Button(frame, text="Admin Login", command=lambda: self.handle_login('a')).pack(pady=15)
        ttk.Button(frame, text="Employee Login", command=lambda: self.handle_login('e')).pack(pady=15)
        ttk.Button(frame, text="New Account", command=lambda: self.handle_login('n')).pack(pady=15)

    def handle_login(self, role):
        #clear the previous widgets
        self.clear_root()

        #Create new frame for login/new user screen
        self.new_frame = ttk.Frame(self.root, padding=30)
        self.new_frame.pack(expand=True)
        
        #create if statments to determine who is logging in
        if role == 'a':
            ttk.Label(self.new_frame, text="Username").pack(anchor="w")
            self.username_entry = ttk.Entry(self.new_frame, width=30)
            self.username_entry.pack(pady=5)

            ttk.Label(self.new_frame, text="Password:").pack(anchor="w")
            self.password_entry = ttk.Entry(self.new_frame, show="*", width=30)
            self.password_entry.pack(pady=5)
            ttk.Button(self.new_frame, text="Login", command=lambda: self.loginCheck('a')).pack(pady=15)
            ttk.Button(self.new_frame, text="Login as an Employee", command=lambda: self.handle_login('e')).pack(pady=15)

        elif role == 'e':
            ttk.Label(self.new_frame, text="Username").pack(anchor="w")
            self.username_entry = ttk.Entry(self.new_frame, width=30)
            self.username_entry.pack(pady=5)

            ttk.Label(self.new_frame, text="Password:").pack(anchor="w")
            self.password_entry = ttk.Entry(self.new_frame, show="*", width=30)
            self.password_entry.pack(pady=5)
            ttk.Button(self.new_frame, text="Login", command=lambda: self.loginCheck('e')).pack(pady=15)
            ttk.Button(self.new_frame, text="Login as a Admin", command=lambda: self.handle_login('a')).pack(pady=15)
            ttk.Button(self.new_frame, text="Create an account", command=lambda: self.handle_login('n')).pack(pady=15)

        elif role == 'n':
            instrustions = "Password must contain:\n\n At least one uppercase letter\n\n At least one lowercase letter\n\n Minimum length: 8\n\n At least one special character(@#!$)"
            ttk.Label(self.new_frame, text="Last Name").pack(anchor="w")
            self.lastname_entry = ttk.Entry(self.new_frame, width=30)
            self.lastname_entry.pack(pady=5)

            ttk.Label(self.new_frame, text=instrustions).pack(anchor="w", pady=20)
            ttk.Label(self.new_frame, text="Password:").pack(anchor="w")
            self.password_entry = ttk.Entry(self.new_frame, show="*", width=30)
            self.password_entry.pack(pady=5)

            ttk.Label(self.new_frame, text="Reenter Password:").pack(anchor="w")
            self.second_password_entry = ttk.Entry(self.new_frame, show="*", width=30)
            self.second_password_entry.pack(pady=5)

            # ttk.Label(self.new_frame, text="Role:").pack(anchor="w")
            # self.role = ttk.Combobox(self.new_frame, values=['Employee', 'Admin'])
            # self.role.pack(pady=5)

            ttk.Button(self.new_frame, text="Create Account", command=lambda: self.newAccount()).pack(pady=15)
            ttk.Button(self.new_frame, text="Main Menu", command=lambda: self.build_login_screen()).pack(pady=15)

    def loginCheck(self, role: str):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.user = self.username_entry.get()

        if role == 'a':
            success, msg = self.auth.login(username, password, role)
            if success:
                self.user = username
                self.admin_main_menu()
            else:
                messagebox.showerror("Login Error", msg)
                return
        
        elif role == 'e':
            success, msg = self.auth.login(username, password, role)
            if success:
                self.user = username
                self.employee_main_menu()
            else:
                messagebox.showerror("Login Error", msg)
                return


    def newAccount(self):
        lName = self.lastname_entry.get()
        first_password = self.password_entry.get()
        second_password = self.second_password_entry.get()
        #role = self.role.get()
        min_length = 8
        allowed_specials = '@#!$'


        #check to see if the password meet the requirements and if both passwords match
        if len(first_password) < min_length:
            messagebox.showerror("New Account", "Password too short.")
            return
            
        if not any(c.isupper() for c in first_password):
            messagebox.showerror("New Account", "Password must have at least one uppercase letter")
            return

        if not any(c.islower() for c in first_password):
            messagebox.showerror("New Account", "Password must have at least one lowercase letter")
            return
                

        # Check for number
        if not any(c.isdigit() for c in first_password):
            messagebox.showerror("New Account", "Password must have at least one number")
            return
                

        # Check for special character from allowed set
        if not any(c in allowed_specials for c in first_password):
            messagebox.showerror("New Account", f"Password must have at least one special character from {allowed_specials}")
            return

        if first_password == second_password:
            success, user = self.auth.new_user(lName, first_password)
            if success:
                self.user = user
                self.employee_main_menu()
            else:
                messagebox.showerror("New Account", "Error. Please try again.")
                return

            
        else: 
                messagebox.showerror("New Account", "Passwords don't match!")

    #employee screen

    def employee_main_menu(self):
        self.clear_root()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")



        ttk.Label(frame, text=f"Welcome {self.user}", style="Header.TLabel", anchor="center").pack(pady=15)


        menu_sections = {
            "Equipment": [
                ("Equipment", lambda: self.list_equipment('e')),
                ("Return Equipment", self.return_equipment),
                ("Equipment At Second Warehouse", self.second_warehouse),
                ("View Request", self.view_request),
            ],
        }

        for section, options in menu_sections.items():
            # Section Label (centered)
            ttk.Label(frame, text=section, font=("Arial", 13, "bold")).pack(pady=(10, 5))

            # Section Frame for buttons
            section_frame = ttk.Frame(frame)
            section_frame.pack(pady=5)

            # Place buttons in a grid (2 per row)
            for i, (label, command) in enumerate(options):
                row, col = divmod(i, 2)
                btn = ttk.Button(section_frame, text=label, width=25, command=command)
                btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")

        # Exit button centered at bottom
        ttk.Button(frame, text="Exit", command=self.build_login_screen).pack(pady=15)



    def on_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            eid = str(values[0])
            item_name = values[2]

            quantities = self.inventory.get_all_equipment_quantity()
            item_quantity = int(quantities.get(eid, 0))

            if item_quantity <= 0:
                # Deselect 
                tree.selection_remove(item_id)
            else:
                self.equipment_options(eid, item_name, item_quantity)

    def create_treeview(self, frame, data_list, columns, headings=None, column_widths=None, auto_number_col=None):

        if headings is None:
            headings = columns
        if column_widths is None:
            column_widths = [100] * len(columns)

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        y_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Configure headings and columns
        for i, col in enumerate(columns):
            tree.heading(col, text=headings[i], anchor="center")
            stretch = False if col.lower() in ["id"] else True
            tree.column(col, anchor="center", width=column_widths[i], stretch=stretch)

        # Insert data
        for idx, row in enumerate(data_list, start=1):
            values = []
            for col in columns:
                if auto_number_col and col == auto_number_col:
                    values.append(idx)
                else:
                    values.append(row.get(col, ""))
            tree.insert("", "end", values=values)

        return tree


    def display_treeview(self, eq_list, columns, headings, widths, role, close_target):
        """Display equipment list in a frame with proper buttons and bindings."""
        self.clear_root()

        # Search Frame
        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        self.search_entry = ttk.Entry(frameTitle, width=20)
        self.search_entry.grid(row=0, column=2, padx=5, sticky="e")
        ttk.Button(frameTitle, text="Search", width=15, 
                   command=lambda: self.complete_search(self.search_entry.get(), role)).grid(row=0, column=1, padx=5, sticky="e")

        # Treeview Frame
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Bind Treeview selection based on role
        if role == 'e':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col="NO")
            tree.bind("<<TreeviewSelect>>", self.on_select)
            ttk.Button(self.root, text="Close", command= lambda: self.close(close_target)).pack(pady=5)
        elif role == 'a':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col="NO")
            tree.bind("<<TreeviewSelect>>", self.admin_on_select)
            ttk.Button(self.root, text="Add Equipment", command=self.add_equipment_entry).pack(pady=5)
            ttk.Button(self.root, text="Close", command= lambda: self.close('a')).pack(pady=5)
        elif role == 'empReturn':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            tree.bind("<<TreeviewSelect>>", self.on_return_select)
            ttk.Button(self.root, text="Return all equipment", command=lambda: self.return_all_equipment('all')).pack(pady=5)
            ttk.Button(self.root, text="Send all equipment for maintenance", command=lambda: self.all_maintenance_request('all')).pack(pady=5)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
        elif role == 'empRequest':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
        elif role == 'adminReturn':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
        elif role == 'adminMaintenance':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            tree.bind("<<TreeviewSelect>>", self.maintenance_on_select)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
        elif role == 'adminEmployee':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            tree.bind("<<TreeviewSelect>>", self.employee_on_select)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
        elif role == 'adminViewEmployeeSkill':
            tree = self.create_treeview(frame, eq_list, columns, headings, widths, auto_number_col=None)
            ttk.Button(self.root, text="Close", command=lambda: self.close(close_target)).pack(pady=5)
            


    def list_equipment(self, role):
        success, eq_list = self.inventory.list_equipment()
        if success:
            self.emp_equipment_columns = ["id", "NO", "name", "quantity"]
            self.emp_equipment_headings = ["ID", "NO.", "Name", "In Stock"]
            self.emp_equipment_widths = [0, 50, 150, 100]
            self.display_treeview(eq_list, self.emp_equipment_columns, self.emp_equipment_headings, self.emp_equipment_widths , role, 'e')
        else:
            messagebox.showerror("Error", 'Please try again')
            self.employee_main_menu()


    def complete_search(self, get_search, role):
        if role == 'e' or role == 'a':
            success, eq_list = self.inventory.get_search_equipment(get_search)
            if success:
                self.display_treeview(eq_list, self.emp_equipment_columns, self.emp_equipment_headings, self.emp_equipment_widths , role, 'list_equipment')
            else:
                messagebox.showerror("Error", 'Please try again')
                return
        elif role == 'adminReturn':
            success, return_list = self.inventory.return_search(get_search)
            if success:
                self.display_treeview(return_list, self.admin_return_columns, self.admin_return_headings, self.admin_return_widths, role, 'adminReturnSearch')
            else:
                messagebox.showerror("Error", 'Please try again')
                return
        elif role == 'adminEmployee':
            pass
        else:
            messagebox.showerror("Error", 'Please try again')
            return


    def equipment_options(self, eid, name, quantity):
        self.dialogE = tk.Toplevel(self.root)
        self.dialogE.title(f"{name} Details")
        appWidth = 300
        appHeight = 300
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogE.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")
        
        self.equipment_name = name

        ttk.Label(self.dialogE, text=f"Name: {name}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.dialogE, text=f"In Stock: {quantity}", font=("Arial", 12)).pack(pady=5)

        ttk.Button(self.dialogE, text="Check Out", command=lambda: self.checkout_equipment(eid, name, quantity)).pack(pady=5)
        ttk.Button(self.dialogE, text="Send for maintenance", command=lambda: self.single_maintenance_request(eid, name)).pack(pady=5)
        ttk.Button(self.dialogE, text="Close", command=self.dialogE.destroy).pack(pady=5)

    def checkout_equipment(self, eid: int, name: str, quantity: int):
        self.clear_dialog(self.dialogE)

        self.dialogE.columnconfigure(0, weight=1)
        self.dialogE.columnconfigure(1, weight=1)
        self.dialogE.columnconfigure(2, weight=1)
        self.dialogE.rowconfigure(0, weight=1)
        self.dialogE.rowconfigure(1, weight=1)

        

        self.total = 1

        self.subtractBtn = ttk.Button(self.dialogE, text="-", state="disabled", command=lambda: self.subtractQuantity())
        self.subtractBtn.grid(row=0, column=0, pady=5, padx=5)
    
        self.totalLabel = ttk.Label(self.dialogE, text="1", font=("Arial", 12))
        self.totalLabel.grid(row=0, column=1, pady=5, padx=15)

        self.addBtn = ttk.Button(self.dialogE, text="+", command=lambda: self.addQuantity(eid))
        self.addBtn.grid(row=0, column=2, pady=5, padx=5)

        ttk.Button(self.dialogE, text="Complete Checkout", command=lambda: self.complete_checkout(eid)).grid(row=1, column=0, columnspan=3, pady=5)

        ttk.Button(self.dialogE, text="Close", command=self.dialogE.destroy).grid(row=2, column=0, columnspan=3, pady=5)


    #create function to add towards the total of equipment to checkout
    def addQuantity(self, eid):
        quantity = self.inventory.get_equipment_quantity_by_id(eid)
        totalEquipment = quantity[0]
        if self.total >= int(totalEquipment):
            self.addBtn.config(state='disabled')
        else:
            self.total +=1
            self.totalLabel.config(text=f'{self.total}')
            self.subtractBtn.config(state='normal')

    #create function to add towards the total of equipment to checkout
    def subtractQuantity(self):
        if self.total == 1:
            self.subtractBtn.config(state='disabled')
        else:
            self.total-=1
            self.totalLabel.config(text=f'{self.total}')
            self.addBtn.config(state='normal')
    
    
    def complete_checkout(self, eid):
        success, msg = self.inventory.checkout_equipment(eid, self.total, self.user)
        if success:
            record_success, record_msg = self.inventory.checkout_records(self.user, self.equipment_name, self.total)
            if record_success:
                messagebox.showinfo("Checkout Equipment", msg)
                self.dialogE.destroy()
            else:
                messagebox.showerror("Error", record_msg)
        else: 
           messagebox.showerror("Error", msg) 
        
    def on_return_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            eid = str(values[0])
            item_username = values[1]
            item_equipment_name = values[2]
            self.return_details(eid, item_equipment_name)

    def return_equipment(self):
        success, return_list = self.inventory.get_return_equipment(self.user)
        if success:
            columns = ["ID", "username", "equipment_name"]
            headings = ["ID", "Username", "Equipment"]
            widths = [50, 150, 100]
            self.display_treeview(return_list, columns, headings, widths, 'empReturn', 'e')
        else:
            messagebox.showerror("Error", "No equipment to return") 
            self.employee_main_menu() 
        
    def return_details(self, eid, item_equipment_name):
        self.dialogS = tk.Toplevel(self.root)
        self.dialogS.title(f"Return Equipment")
        appWidth = 300
        appHeight = 280
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogS.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogS, text="Return equipment", command=lambda: self.return_single_equipment(eid)).pack(pady=5)
        ttk.Button(self.dialogS, text="Send equipment for maintenance", command=lambda: self.single_maintenance_request(eid, item_equipment_name)).pack(pady=5)
        ttk.Button(self.dialogS, text="Close", command=self.dialogS.destroy).pack(pady=5)

    def return_all_equipment(self, return_all):
        success, msg = self.inventory.update_return_equipment(return_all, self.user)
        if success:
            messagebox.showinfo("Return Equipment", msg)
            self.employee_main_menu()
        else:
            messagebox.showerror("Error", msg)

    def return_single_equipment(self, eid):
        success, msg = self.inventory.update_return_equipment(eid, self.user)  
        if success:
            messagebox.showinfo("Return Equipment", msg)
            self.dialogS.destroy()
        else:
            messagebox.showerror("Error", msg)        

    def single_maintenance_request(self, eid, item_equipment_name):
        success, msg = self.request.maintenance_request(eid, item_equipment_name, self.user)
        if success:
            messagebox.showinfo("Maintenance Request", msg)
            
        else:
            messagebox.showerror("Error", msg) 

    def all_maintenance_request(self, send_all):
        success, msg = self.request.maintenance_request(self.return_list, 'all', self.user)
        if success:
            messagebox.showinfo("Maintenance Request", msg)
            self.employee_main_menu()
        else:
            messagebox.showerror("Error", msg)

    def second_warehouse(self):
        self.clear_root()
        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)

        centerFrame = ttk.Frame(frameTitle)
        centerFrame.pack(pady=10)

        ttk.Button(centerFrame, text="Search", width=15,
                command=lambda: self.complete_secondWarehouse_search(
                    self.search_secondWarehouse_entry.get()
                )).grid(row=0, column=0, padx=5)

        self.search_secondWarehouse_entry = ttk.Entry(centerFrame, width=20)
        self.search_secondWarehouse_entry.grid(row=0, column=1, padx=5)

        ttk.Button(centerFrame, width=50, text="Close",
                command=lambda:self.close('employee_main_menu', 'e')).grid(row=1, column=0, padx=5, columnspan=2)


    def complete_secondWarehouse_search(self, get_search):
        self.clear_root()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        success, eq_list= self.inventory.get_equipment_from_secondWarehouse(get_search)
        if success:
            record = eq_list[0]
            name = record["name"]
            quantity = record["quantity"]

            ttk.Label(frame, text=f"Name: {self.name}", font=("Arial", 18)).pack(pady=5)
            ttk.Label(frame, text=f"In Stock: {quantity}", font=("Arial", 18)).pack(pady=5)

            ttk.Button(frame, text="Request Equipment", command=lambda: self.send_request(get_search, 'none')).pack(pady=5)
            ttk.Button(frame, text="Close", command=self.second_warehouse).pack(pady=5)
        else:
            ttk.Label(frame, text="Equipment Not Found", font=("Arial", 18)).pack(pady=5)
            ttk.Button(frame, text="Place order for equipment", command=lambda: self.send_request('none', get_search)).pack(pady=5)
            ttk.Button(frame, text="Close", command=self.second_warehouse).pack(pady=5)

    def send_request(self, request_name, new_request):
        success, msg = self.request.set_request(request_name, new_request, self.user)
        if success:
            messagebox.showinfo("Request Equipment", msg)
            self.second_warehouse
        else:
            messagebox.showerror("Error", msg) 

    def view_request(self):
        self.clear_root()

        success, rq_list = self.request.get_all_request(self.user)
        if success:
            columns = ["request_id", "equipment_request", "new_request", "request_status"]
            headings = ["ID", "Equipment Requested", "Equipment Ordered", "Request Status"]
            widths = [50, 50, 150, 100]
            self.display_treeview(rq_list, columns, headings, widths, 'empRequest', 'e')
        else:
            messagebox.showerror("Error", "No request made.") 
            self.employee_main_menu()

    #admin screen
    def admin_main_menu(self):
        self.clear_root()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=f"Welcome {self.user}", style="Header.TLabel", anchor="center").pack(pady=15)


        menu_sections = {
            "Equipment": [
                ("List Equipment", lambda: self.list_equipment('a')),
                ("Return Equipment", self.view_return_equipment),
                ("Maintenance Request", self.view_maintenance_request),
                ("List Employees", self.view_employee_list),
                ("Add Skill", self.add_new_skill),
                ("View Equipment Request", self.view_equipment_request),
                ("Generate Report", self.generate_report),
            ],
        }

        for section, options in menu_sections.items():
            # Section Label (centered)
            ttk.Label(frame, text=section, font=("Arial", 13, "bold")).pack(pady=(10, 5))

            # Section Frame for buttons
            section_frame = ttk.Frame(frame)
            section_frame.pack(pady=5)

            # Place buttons in a grid (2 per row)
            for i, (label, command) in enumerate(options):
                row, col = divmod(i, 2)
                btn = ttk.Button(section_frame, text=label, width=25, command=command)
                btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")

        # Exit button centered at bottom
        ttk.Button(frame, text="Exit", command=self.build_login_screen).pack(pady=15)

    def admin_on_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            eid = str(values[1])
            item_name = values[2]

            quantities = self.inventory.get_all_equipment_quantity()
            item_quantity = quantities.get(eid, 0)

            self.admin_equipment_options(eid, item_name, item_quantity)
   

    def admin_equipment_options(self, eid, name, quantity):
        self.dialogE = tk.Toplevel(self.root)
        self.dialogE.title(f"{name} Details")
        appWidth = 300
        appHeight = 320
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogE.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")
        
        self.equipment_name = name

        ttk.Label(self.dialogE, text=f"Name: {name}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.dialogE, text=f"In Stock: {quantity}", font=("Arial", 12)).pack(pady=5)

        #ttk.Button(self.dialogE, text="Check Out", command=lambda: self.checkout_equipment(eid)).pack(pady=5)
        ttk.Button(self.dialogE, text="Remove Equipment", command=lambda: self.remove_equipment(eid)).pack(pady=5)
        ttk.Button(self.dialogE, text="Send for maintenance", command=lambda: self.single_maintenance_request(eid, name)).pack(pady=5)
        ttk.Button(self.dialogE, text="Close", command=self.dialogE.destroy).pack(pady=5)

    #dialog for adding new equipment
    def add_equipment_entry(self):
        self.dialogA = tk.Toplevel(self.root)
        self.dialogA.title(f"Add Equipment")
        appWidth = 300
        appHeight = 320
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogA.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        new_frame = ttk.Frame(self.dialogA, padding=30)
        new_frame.pack(expand=True)

        ttk.Label(new_frame, text="Equipment Name").pack(anchor="w")
        self.equipment_name_entry = ttk.Entry(new_frame, width=30)
        self.equipment_name_entry.pack(pady=5)

        ttk.Label(new_frame, text="Equipment Total").pack(anchor="w")
        self.total_entry = ttk.Entry(new_frame, width=30)
        self.total_entry.pack(pady=5)

        ttk.Label(new_frame, text="Skill Require For Equipment").pack(anchor="w")
        self.skill_entry = ttk.Entry(new_frame, width=30)
        self.skill_entry.pack(pady=5)

        ttk.Button(new_frame, text="Add Equipment", command=self.complete_add_equipment).pack(pady=5)
        ttk.Button(new_frame, text="Close", command=self.dialogA.destroy).pack(pady=5)

    def complete_add_equipment(self):
        equipment_name = self.equipment_name_entry.get()
        total_equipment = self.total_entry.get()
        skill = self.skill_entry.get()

        success, msg = self.inventory.add_equipment(equipment_name, total_equipment, skill)
        if success:
            messagebox.showinfo("Add Equipment", msg)
            self.dialogA.destroy()
        else:
            messagebox.showerror("Error", msg)

    def remove_equipment(self, eid):
        success, msg = self.inventory.remove_equipment(eid)
        if success:
            messagebox.showinfo("Remove Equipment", msg)
            self.dialogE.destroy()
        else:
            messagebox.showerror("Error", msg)

    def view_return_equipment(self):
        success, return_list = self.inventory.view_all_return()
        if success:
            self.admin_return_columns = ["ID", "username", "equipment_name", "equipment_return", "checkout_at", "return_at"]
            self.admin_return_headings = ["ID", "Username", "Equipment Name", "Equipment Return", "Checkout At", "Return At"]
            self.admin_return_widths = [50, 150, 150, 150, 150, 150]
            self.display_treeview(return_list, self.admin_return_columns, self.admin_return_headings, self.admin_return_widths, 'adminReturn', 'a')
        else:
            messagebox.showerror("Error", 'Please try again')
            self.admin_main_menu()

    def maintenance_on_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            eid = str(values[0])
            item_name = values[1]
            item_status = values[2]

            if item_status == 'pending':
                self.maintenance_pending_options(eid, item_name)
            elif item_status == 'in progress':
                self.maintenance_in_progess_options(eid, item_name)
            else:
                messagebox.showerror("Error", "Maintenance complete.")    

    def view_maintenance_request(self):
        success, maintenance_list = self.request.view_maintenance_request()
        if success:
            self.admin_maintenance_columns = ["maintenance_id", "equipment_name", "maintenance_status", "request_date", "return_date"]
            self.admin_maintenance_headings = ["ID", "Equipment Name", "Maintenance Status", "Request Date", "Return Date"]
            self.admin_maintenance_widths = [50, 150, 150, 150, 150]
            self.display_treeview(maintenance_list, self.admin_maintenance_columns, self.admin_maintenance_headings, self.admin_maintenance_widths, 'adminMaintenance', 'a')
        else:
            messagebox.showerror("Error", 'Please try again')
            self.admin_main_menu()
        
    #option for equipment with pending as its status
    def maintenance_pending_options(self, eid, name):
        self.dialogPR = tk.Toplevel(self.root)
        self.dialogPR.title(f"Maintenance Request")
        appWidth = 400
        appHeight = 420
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogPR.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogPR, text="Approve Maintenance Request", command=lambda: self.send_for_maintenance(eid, name)).pack(pady=5)
        ttk.Button(self.dialogPR, text="Deny Maintenance Request", command=lambda: self.maintenance_complete(eid, name)).pack(pady=5)
        ttk.Button(self.dialogPR, text="Close", command=self.dialogPR.destroy).pack(pady=5)


    def maintenance_in_progess_options(self, eid, name):
        self.dialogIPR = tk.Toplevel(self.root)
        self.dialogIPR.title(f"Maintenance Request")
        appWidth = 400
        appHeight = 420
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogIPR.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogIPR, text="Return Equipment", command=lambda: self.maintenance_complete(eid, name)).pack(pady=5)

    #update the maintenane on the equipment to in progess
    def send_for_maintenance(self, eid, name):
        success, msg = self.request.update_maintenance_status('in progress', eid, name)
        if success:
            messagebox.showinfo("Maintenance Request", msg)
            self.dialogPR.destroy()
        else:
            messagebox.showerror("Error", msg)

    def maintenance_complete(self, eid, name):
        success, msg = self.request.update_maintenance_status('completed', eid, name)
        if success:
            messagebox.showinfo("Maintenance Request", "Equipment return successful.")
            self.dialogPR.destroy()
        else:
            messagebox.showerror("Error", msg)

#list employee section
    def employee_on_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            item_name = values[0]

            

            self.employee_options(item_name)

    def view_employee_list(self):
    
        success, employee_list = self.employee.view_employees()
        if success:
            self.admin_employee_columns = ["username", "role", "employment_status"]
            self.admin_employee_headings = ["Username", "Role", "Employment Status"]
            self.admin_employee_widths = [150, 100, 150]
            self.display_treeview(employee_list, self.admin_employee_columns, self.admin_employee_headings, self.admin_employee_widths, 'adminEmployee', 'a')
        else:
            messagebox.showerror("Error", 'Please try again')
            self.admin_main_menu()
       

    def complete_employee_search(self, get_search):
        self.clear_root()
        

        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_employee_search(self.search_employee_entry.get())).grid(row=0, column=1, padx=5, sticky="e")
        self.search_employee_entry = ttk.Entry(frameTitle, width=20)
        self.search_employee_entry.grid(row=0, column=2, padx=5, sticky="e")

        success, employee_list = self.employee.employee_search(get_search)
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        x_scroll = ttk.Scrollbar(frame, orient="horizontal")

        if success:
            tree = ttk.Treeview(frame, columns=("Username", "Role", "Employment Status"), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")

            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")

            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            tree.heading("Username", text="Username", anchor="center")
            tree.heading("Role", text="Role", anchor="center")
            tree.heading("Employment Status", text="Employment Status", anchor="center")

            tree.column("Username", anchor="center", width=150)
            tree.column("Role", anchor="center", width=100)
            tree.column("Employment Status", anchor="center", width=150)
        
            

            for eq in employee_list:
                tree.insert("", "end", values=(eq['username'], eq['role'], eq['employment_status']))

            # Bind single-click selection
            tree.bind("<<TreeviewSelect>>", self.employee_on_select)
            
            ttk.Button(self.root, text="Back", command=self.view_employee_list).pack(pady=5)
        else:
            messagebox.showerror("Error", "Unknown Error. Please try again.")  
            self.view_employee_list()

   


    def employee_options(self, user):
        self.clear_root()

        ttk.Button(self.root, text="Change Role", command=lambda: self.change_role(user)).pack(pady=20)
        ttk.Button(self.root, text="Add Skill", command=lambda: self.add_employee_skill(user)).pack(pady=20)
        ttk.Button(self.root, text="View Skills", command=lambda: self.view_employee_skills(user)).pack(pady=20)
        ttk.Button(self.root, text="Close", command=self.view_employee_list).pack(pady=20)

    def change_role(self, user):
        self.dialogCR = tk.Toplevel(self.root)
        self.dialogCR.title(f"Change Role")
        appWidth = 400
        appHeight = 200
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogCR.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogCR, text="Promote to admnin", command=lambda: self.promote_to_admin_or_terminate(user, 'admin')).pack(pady=5)
        ttk.Button(self.dialogCR, text="Terminate", command=lambda: self.promote_to_admin_or_terminate(user, 'terminated')).pack(pady=5)
        ttk.Button(self.dialogCR, text="Back", command= self.dialogCR.destroy).pack(pady=5)

    def promote_to_admin_or_terminate(self, user, role_or_status):
        success, msg = self.employee.change_role_or_employment_status(user, role_or_status)
        if success:
            messagebox.showinfo("Change role", msg)
            self.dialogCR.destroy()
        else:
            messagebox.showerror("Error", msg)


    def skill_on_select(self, event, user):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            item_id = values[0]
            item_name = values[1]

            

            self.skill_options(item_id, user)

    def add_employee_skill(self, user):
        self.clear_root()

        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_skill_search(self.search_skill_entry.get(), user)).grid(row=0, column=1, padx=5, sticky="e")
        self.search_skill_entry = ttk.Entry(frameTitle, width=20)
        self.search_skill_entry.grid(row=0, column=2, padx=5, sticky="e")
        
       


        success, skill_list = self.employee.get_all_skills()
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        x_scroll = ttk.Scrollbar(frame, orient="horizontal")

        if success:
            tree = ttk.Treeview(frame, columns=("ID", "Skill"), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")

            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")

            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            tree.heading("ID", text="ID", anchor="center")
            tree.heading("Skill", text="Skill.", anchor="center")
           
            tree.column("ID", anchor="center", width=25)
            tree.column("Skill", anchor="center", width=50)
                       

            for eq in skill_list:
                tree.insert("", "end", values=(eq['skills_id'], eq['skills_name']))

            # Bind single-click selection
            tree.bind("<<TreeviewSelect>>", lambda event :self.skill_on_select(event, user))
            
            ttk.Button(self.root, text="Back", command=lambda: self.employee_options(user)).pack(pady=5)
        else:
            messagebox.showerror("Error", "Unknown Error. Please try again.") 
            self.employee_options(user)

    def complete_skill_search(self, get_search, user):
        self.clear_root()

        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_skill_search(self.search_skill_entry.get(), user)).grid(row=0, column=1, padx=5, sticky="e")
        self.search_skill_entry = ttk.Entry(frameTitle, width=20)
        self.search_skill_entry.grid(row=0, column=2, padx=5, sticky="e")
        
       


        success, skill_list = self.employee.get_search_skill(get_search)
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        x_scroll = ttk.Scrollbar(frame, orient="horizontal")

        if success:
            tree = ttk.Treeview(frame, columns=("ID", "Skill"), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")

            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")

            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            tree.heading("ID", text="ID")
            tree.heading("Skill", text="Skill.", anchor="center")
           
            tree.column("ID", width=0, stretch=False)
            tree.column("Skill", anchor="center", width=50)
                       

            for eq in skill_list:
                tree.insert("", "end", values=(eq['skills_id'], eq['skills_name']))

            # Bind single-click selection
            tree.bind("<<TreeviewSelect>>", lambda event: self.skill_on_select(event, user))
            
            ttk.Button(self.root, text="Back", command=lambda: self.add_employee_skill(user)).pack(pady=5)
        else:
            messagebox.showerror("Error", "Unknown Error. Please try again.") 
            self.add_employee_skill(user)

    def skill_options(self, eid, user):
        confirm = messagebox.askyesno("Confirm Skill", "Are you sure you want to add this skill?")
        if confirm:
            success, msg = self.employee.insert_employee_skill(eid, user)
            if success:
                messagebox.showinfo("Add Skill", msg)
                self.add_employee_skill(user)
            else:
                messagebox.showerror("Error", msg) 
                self.view_employee_list()
        else:
            self.add_employee_skill(user)

    def view_employee_skills(self, user):
        success, skill_list = self.employee.get_employee_skills(user)
        if success:
            self.admin_employee_skills_columns = ["username", "skills_name"]
            self.admin_employee_skills_headings = ["Username", "Skill Name"]
            self.admin_employee_skills_widths = [150, 100]
            self.display_treeview(skill_list, self.admin_employee_skills_columns, self.admin_employee_skills_headings, self.admin_employee_skills_widths, 'adminViewEmployeeSkill', 'a')
        else:
            messagebox.showerror("Error", 'Please try again')
            self.admin_main_menu()


    def add_new_skill(self):
        self.dialogANS = tk.Toplevel(self.root)
        self.dialogANS.title(f"Add Skill")
        appWidth = 300
        appHeight = 320
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogANS.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        new_frame = ttk.Frame(self.dialogANS, padding=30)
        new_frame.pack(expand=True)

        ttk.Label(new_frame, text="Skill Name").pack(anchor="w")
        self.skill_name_entry = ttk.Entry(new_frame, width=30)
        self.skill_name_entry.pack(pady=5)

        ttk.Button(new_frame, text="Add Skill", command=self.complete_add_skill).pack(pady=5)
        ttk.Button(new_frame, text="Close", command=self.dialogANS.destroy).pack(pady=5)

    def complete_add_skill(self):
        skill_name = self.skill_name_entry.get()
        success, msg = self.inventory.set_skill(skill_name)
        if success:
            messagebox.showinfo("Add Skill", msg)
            self.dialogANS.destroy()
        else:
            messagebox.showerror("Error", msg)
            self.dialogANS.destroy()

    def request_on_select(self, event):
        tree = event.widget
        selected = tree.selection()

        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            item_id = values[0]
            item_status = values[4]

            if item_status == 'pending':
                self.view_request_pending(item_id)
            elif item_status == 'in progress':
                self.view_request_in_progress(item_id)
            else:
                messagebox.showerror("Error", "Request completed.")
            

    def view_equipment_request(self):
        self.clear_root()

        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_request_search(self.search_request_entry.get())).grid(row=0, column=1, padx=5, sticky="e")
        self.search_request_entry = ttk.Entry(frameTitle, width=20)
        self.search_request_entry.grid(row=0, column=2, padx=5, sticky="e")

        success, rq_list = self.request.get_all_request_admin('none')
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        x_scroll = ttk.Scrollbar(frame, orient="horizontal")

        if success:
            tree = ttk.Treeview(frame, columns=("ID", "Equipment Request", "Equipment Order", "Username", "Request Status", "Request At", "Request Completion"), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")

            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")

            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            tree.heading("ID", text="ID", anchor="center")
            tree.heading("Equipment Request", text="Equipment Request", anchor="center")
            tree.heading("Equipment Order", text="Equipment Order", anchor="center")
            tree.heading("Username", text="Username", anchor="center")
            tree.heading("Request Status", text="Request Status", anchor="center")
            tree.heading("Request At", text="Request At", anchor="center")
            tree.heading("Request Completion", text="Request Completion", anchor="center")

            tree.column("ID", anchor="center", width=150)
            tree.column("Equipment Request", anchor="center", width=100)
            tree.column("Equipment Order", anchor="center", width=150)
            tree.column("Username", anchor="center", width=150)
            tree.column("Request Status", anchor="center", width=150)
            tree.column("Request At", anchor="center", width=150)
            tree.column("Request Completion", anchor="center", width=150)
        
            

            for rq in rq_list:
                tree.insert("", "end", values=(rq['request_id'], rq['equipment_request'], rq['new_request'], rq['user'], rq['request_status'], rq['request_at'], rq['arrive_at']))

            # Bind single-click selection
            tree.bind("<<TreeviewSelect>>", self.request_on_select)
            ttk.Button(self.root, text="Close", command=self.admin_main_menu).pack(pady=5)
        else:
            messagebox.showerror("Error", "Unknown Error. Please try again.") 
            self.admin_main_menu() 

    def complete_request_search(self, get_search):
        self.clear_root()
        frameTitle = ttk.Frame(self.root)
        frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
        frameTitle.grid_columnconfigure(0, weight=1)

        ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_request_search(self.search_request_entry.get())).grid(row=0, column=1, padx=5, sticky="e")
        self.search_request_entry = ttk.Entry(frameTitle, width=20)
        self.search_request_entry.grid(row=0, column=2, padx=5, sticky="e")

        success, rq_list = self.request.get_all_request_admin(get_search)
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        y_scroll = ttk.Scrollbar(frame, orient="vertical")
        x_scroll = ttk.Scrollbar(frame, orient="horizontal")

        if success:
            tree = ttk.Treeview(frame, columns=("ID", "Equipment Request", "Equipment Order", "Username", "Request Status", "Request At", "Request Completion"), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")

            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")

            y_scroll.config(command=tree.yview)
            x_scroll.config(command=tree.xview)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            tree.heading("ID", text="ID", anchor="center")
            tree.heading("Equipment Request", text="Equipment Request", anchor="center")
            tree.heading("Equipment Order", text="Equipment Order", anchor="center")
            tree.heading("Username", text="Username", anchor="center")
            tree.heading("Request Status", text="Request Status", anchor="center")
            tree.heading("Request At", text="Request At", anchor="center")
            tree.heading("Request Completion", text="Request Completion", anchor="center")

            tree.column("ID", anchor="center", width=150)
            tree.column("Equipment Request", anchor="center", width=100)
            tree.column("Equipment Order", anchor="center", width=150)
            tree.column("Username", anchor="center", width=150)
            tree.column("Request Status", anchor="center", width=150)
            tree.column("Request At", anchor="center", width=150)
            tree.column("Request Completion", anchor="center", width=150)
        
            

            for rq in rq_list:
                tree.insert("", "end", values=(rq['request_id'], rq['equipment_request'], rq['new_request'], rq['user'], rq['request_status'], rq['request_at'], rq['arrive_at']))

            # Bind single-click selection
            tree.bind("<<TreeviewSelect>>", self.request_on_select)
            ttk.Button(self.root, text="Close", command=self.view_equipment_request).pack(pady=5)
        else:
            messagebox.showerror("Error", "Unknown Error. Please try again.") 
            self.view_equipment_request() 

    def view_request_pending(self, eid): 
        self.dialogVRP = tk.Toplevel(self.root)
        self.dialogVRP.title(f"Equipment Request")
        appWidth = 400
        appHeight = 420
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogVRP.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogVRP, text="Approve Request", command=lambda: self.update_request_status(eid, 'in progress', self.dialogVRP)).pack(pady=5)
        ttk.Button(self.dialogVRP, text="Deny Request", command=lambda: self.update_request_status(eid, 'complete', self.dialogVRP)).pack(pady=5)
        ttk.Button(self.dialogVRP, text="Close", command=self.dialogVRP.destroy).pack(pady=5)

    def view_request_in_progress(self, eid):
        self.dialogVRIP = tk.Toplevel(self.root)
        self.dialogVRIP.title("Equipment Request")
        appWidth = 400
        appHeight = 420
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        self.dialogVRIP.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

        ttk.Button(self.dialogVRIP, text="Complete Request", command=lambda: self.update_request_status(eid, 'complete', self.dialogVRIP)).pack(pady=5)
        ttk.Button(self.dialogVRIP, text="Close", command=self.dialogVRIP.destroy).pack(pady=5)

    def update_request_status(self, eid, status, dialogWindow):
        success, msg = self.request.update_request_status(eid, status)
        if success:
            messagebox.showinfo( "Equipment Request", msg)
            dialogWindow.destroy()
        else:
            messagebox.showerror("Error", msg)

    def generate_report(self):
        try:

            # Create reports folder
            output_dir = "reports"
            os.makedirs(output_dir, exist_ok=True)

            # Create timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = os.path.join(output_dir, f"weekly_report_{timestamp}.pdf")

            # Get data from database
            checkout_rows, request_rows, maintenance_rows = self.request.generate_all_report()


            # Setup PDF
            doc = SimpleDocTemplate(filename, pagesize=LETTER)
            styles = getSampleStyleSheet()
            content = []

            # Title
            content.append(Paragraph("Weekly Equipment Activity Report", styles["Title"]))
            content.append(Spacer(1, 20))

            # Helper function to add sections
            def add_section(title, rows):
                content.append(Paragraph(title, styles["Heading2"]))
                if rows:
                    # Convert SQLite tuples to lists if needed
                    if isinstance(rows[0], tuple):
                        table_data = [list(range(1, len(rows[0]) + 1))] + [list(x) for x in rows]
                    else:
                           table_data = [list(rows[0].keys())] + [list(x.values()) for x in rows]

                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER")
                    ]))
                    content.append(table)
                else:
                    content.append(Paragraph("No records found.", styles["BodyText"]))
                content.append(Spacer(1, 20))

            # Add sections
            add_section("Checkouts (Not Returned, Last 7 Days)", checkout_rows)
            add_section("Requests (Last 7 Days)", request_rows)
            add_section("Maintenance Records (Last 7 Days)", maintenance_rows)

            # Build PDF
            doc.build(content)
        except Exception as e:
            print("Error in generating reprot:", e)
            messagebox.showerror("Error", "Error! Please try again.")
        finally:
            messagebox.showinfo( "Generate Report", "Report generated")
        
        


    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_dialog(self, dialogWindow):
        for widget in dialogWindow.winfo_children():
            widget.destroy()
    def close(self, function_name):
        if function_name == 'list_equipment':
            self.list_equipment(function_name)

        elif function_name == 'e':
            self.employee_main_menu()
        elif function_name =='a':
            self.admin_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = EquipmentApp(root)
    root.mainloop()