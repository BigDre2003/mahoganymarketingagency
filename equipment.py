import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from data.database import Database

db = Database()

def generate_pdf_report():
    # 1️⃣ Create reports folder
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # 2️⃣ Create timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = os.path.join(output_dir, f"weekly_report_{timestamp}.pdf")

    # 3️⃣ Get data from database
    checkout_rows, request_rows, maintenance_rows = db.generate_all_report()

    # 4️⃣ Setup PDF
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

    print(f"Report generated: {filename}")
    return filename

pdf_path = generate_pdf_report()
print("PDF saved at:", pdf_path)



# style.configure("TFrame", font=("Arial", 11), padding=6, background="dark gray")

#         style.configure("TButton", font=("Arial", 12), padding=6, foreground="black", 
#                 background="#f4f4f9")
#         style.configure("TLabel", font=("Arial", 12), foreground="white", background="dark gray")
#         style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="dark gray")

#         style.configure("Treeview",
#                 background="dark gray",       # row background
#                 foreground="black",         # text color
#                 rowheight=25,               # row height
#                 fieldbackground="dark gray")  # background for empty space
        
#         style.configure("Treeview.Heading",
#                 font=("Arial", 12, "bold"),
#                 background="gray",
#                 foreground="black")

#         # Style the selected row
#         style.map("Treeview",
#                 background=[("selected", "#347083")],
#                 foreground=[("selected", "white")])


# def list_equipment(self, role):
    #     self.clear_root()

    #     frameTitle = ttk.Frame(self.root)
    #     frameTitle.pack(expand=True, fill="both", padx=10, pady=5)
    #     frameTitle.grid_columnconfigure(0, weight=1)

    #     ttk.Button(frameTitle, text="Search", width=15, command=lambda: self.complete_equipment_search(self.search_equipment_entry.get(), role)).grid(row=0, column=1, padx=5, sticky="e")
    #     self.search_equipment_entry = ttk.Entry(frameTitle, width=20)
    #     self.search_equipment_entry.grid(row=0, column=2, padx=5, sticky="e")
       

    #     success, eq_list = self.inventory.list_equipment()


    #     frame = ttk.Frame(self.root)
    #     frame.pack(expand=True, fill="both", padx=10, pady=5)

    #     y_scroll = ttk.Scrollbar(frame, orient="vertical")
    #     x_scroll = ttk.Scrollbar(frame, orient="horizontal")

    #     if success:
    #         tree = ttk.Treeview(frame, columns=("ID", "NO", "Name", "Quantity"), show="headings")
    #         tree.grid(row=0, column=0, sticky="nsew")

    #         y_scroll.grid(row=0, column=1, sticky="ns")
    #         x_scroll.grid(row=1, column=0, sticky="ew")

    #         y_scroll.config(command=tree.yview)
    #         x_scroll.config(command=tree.xview)
            
    #         frame.grid_rowconfigure(0, weight=1)
    #         frame.grid_columnconfigure(0, weight=1)

    #         tree.heading("ID", text="ID")
    #         tree.heading("NO", text="NO.", anchor="center")
    #         tree.heading("Name", text="Name", anchor="center")
    #         tree.heading("Quantity", text="In Stock", anchor="center")
    #         tree.column("ID", width=0, stretch=False)
    #         tree.column("NO", anchor="center", width=50)
    #         tree.column("Name", anchor="center", width=150)
    #         tree.column("Quantity", anchor="center", width=100)

    #         for count, eq in enumerate(eq_list, start=1):
    #             tree.insert("", "end", values=(eq['id'], count, eq['name'], eq['quantity']))

            

    #         if role == 'e':
    #             # Bind single-click selection
    #             tree.bind("<<TreeviewSelect>>", self.on_select)
    #             ttk.Button(self.root, text="Close", command=lambda: self.close('employee_main_menu', 'e')).pack(pady=5)
    #         else:
    #             # Bind single-click selection
    #             tree.bind("<<TreeviewSelect>>", self.admin_on_select)
    #             ttk.Button(self.root, text="Add Equipment", command=self.add_equipment_entry).pack(pady=5)
    #             ttk.Button(self.root, text="Close", command=lambda: self.close('admin_main_menu', 'a')).pack(pady=5)
    #     else: 
    #         messagebox.showerror("Error", 'Please try again') 
    #         self.employee_main_menu()

    # def complete_equipment_search(self, get_search, role):
    #     self.clear_root()

    #     success, eq_list = self.inventory.get_search_equipment(get_search)

    #     frame = ttk.Frame(self.root)
    #     frame.pack(expand=True, fill="both", padx=10, pady=5)

    #     y_scroll = ttk.Scrollbar(frame, orient="vertical")
    #     x_scroll = ttk.Scrollbar(frame, orient="horizontal")

    #     if success:
    #         tree = ttk.Treeview(frame, columns=("ID", "NO", "Name", "Quantity"), show="headings")
    #         tree.grid(row=0, column=0, sticky="nsew")

    #         y_scroll.grid(row=0, column=1, sticky="ns")
    #         x_scroll.grid(row=1, column=0, sticky="ew")

    #         y_scroll.config(command=tree.yview)
    #         x_scroll.config(command=tree.xview)
            
    #         frame.grid_rowconfigure(0, weight=1)
    #         frame.grid_columnconfigure(0, weight=1)

    #         tree.heading("ID", text="ID")
    #         tree.heading("NO", text="NO.", anchor="center")
    #         tree.heading("Name", text="Name", anchor="center")
    #         tree.heading("Quantity", text="In Stock", anchor="center")
    #         tree.column("ID", width=0, stretch=False)
    #         tree.column("NO", anchor="center", width=50)
    #         tree.column("Name", anchor="center", width=150)
    #         tree.column("Quantity", anchor="center", width=100)

    #         for count, eq in enumerate(eq_list, start=1):
    #             tree.insert("", "end", values=(eq['id'], count, eq['name'], eq['quantity']))

            

    #         if role == 'e':
    #             # Bind single-click selection
    #             tree.bind("<<TreeviewSelect>>", self.on_select)
    #             ttk.Button(self.root, text="Close", command=lambda: self.close('list_equipment', 'e')).pack(pady=5)
    #         else:
    #             # Bind single-click selection
    #             tree.bind("<<TreeviewSelect>>", self.admin_on_select)
    #             ttk.Button(self.root, text="Add Equipment", command=self.add_equipment_entry).pack(pady=5)
    #             ttk.Button(self.root, text="Close", command=lambda: self.close('list_equipment', 'a')).pack(pady=5)
    #     else: 
    #         messagebox.showerror("Error", 'Please try again') 



     # if success:
        #     tree = ttk.Treeview(frame, columns=("ID", "Username", "Equipment"), show="headings")
        #     tree.heading("ID", text="ID", anchor="center")
        #     tree.heading("Username", text="Username", anchor="center")
        #     tree.heading("Equipment", text="Equipment", anchor="center")

        #     tree.column("ID", anchor="center", width=50)
        #     tree.column("Username", anchor="center", width=150)
        #     tree.column("Equipment", anchor="center", width=100)
        
        #     tree.pack(expand=True, fill="both", padx=10, pady=10)

        #     for eq in self.return_list:
        #         tree.insert("", "end", values=(eq['id'], eq['username'], eq['equipment_name']))

        #     # Bind single-click selection
        #     tree.bind("<<TreeviewSelect>>", self.on_return_select)

        #     ttk.Button(self.root, text="Return all equipment", command=lambda: self.return_all_equipment('all')).pack(pady=5)
        #     ttk.Button(self.root, text="Send all equipment for maintenance", command=lambda: self.all_maintenance_request('all')).pack(pady=5)

        #     ttk.Button(self.root, text="Close", command=self.employee_main_menu).pack(pady=5)
        # else:
        #     messagebox.showerror("Error", "No equipment to return") 
        #     self.employee_main_menu()