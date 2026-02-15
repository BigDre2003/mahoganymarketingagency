import sqlite3
from collections import Counter


class Database:
    def __init__(self, db_name="equipment.db"):
        self.conn = sqlite3.connect(db_name)
        conn = self.conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")

    #insert new user data into database
    def create_user(self, username, password, salt, role):
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password_salt, password_hash, user_role) VALUES (?, ?, ?, ?)',
                    (username, salt, password, role))
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
        
        
        
    #verify user login info
    def verify_user(self, username):
        try:
            c = self.conn.cursor()
            c.execute("SELECT password_salt, password_hash, user_role FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            return row
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    

    #insert new equipment in the database
    def add_equipment(self, name, quantity, skill):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO equipment (name, quantity, skill_required) VALUES (?, ?, ?)",
                    (name, quantity, skill))
            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    #remove equipment from the database
    def remove_equipment(self, eid):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM equipment WHERE id = ?", (eid,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    
    #get the quantity for all equipment
    def get_all_equipment_quantity(self):
        try:
            c = self.conn.cursor()
            c.execute('SELECT id, quantity FROM equipment ORDER BY id')
            rows = c.fetchall()
            return {str(row[0]): row[1] for row in rows} 
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
        
    def get_equipment_quantity_by_id_or_name(self, eid, name):
        try:
            if name == 'none':
                c = self.conn.cursor()
                c.execute("SELECT quantity FROM equipment WHERE id = ?", (eid,))
                row = c.fetchone()
                return row
            else:
                c = self.conn.cursor()
                c.execute("SELECT name, quantity FROM equipment WHERE name = ?", (name,))
                rows = c.fetchall()
                return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    
    #get all equipment from database
    def get_all_equipment(self):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM equipment ORDER BY name')
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    
    def get_secondWarehouse_equipment(self, name):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM second_warehouse WHERE name = ?', (name,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    
    
    def get_search_equipment(self, equipment_name):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM equipment WHERE name = ?', (equipment_name,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    #update equipment quantity
    def update_equipment_quantity(self, quantity, eid, name):
        try:
            c = self.conn.cursor()
            if name == 'none':
                c.execute(
                    'UPDATE equipment SET quantity = ? WHERE id = ?',
                    (quantity, eid)
                )
                self.conn.commit()
                return True
            else:
                c.execute("UPDATE equipment SET quantity = ? WHERE name = ?",
                          (quantity, name))
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
      
    #checkout requested equipment
    def checkout(self, equipment_id):
        try:
            c = self.conn.cursor()
            c.execute('SELECT quantity FROM equipment WHERE id = ?', (equipment_id,))
            row = c.fetchone()  
            if isinstance(row, tuple):
                quantity = int(row[0])
            return quantity
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def skills_check(self, eid, user):
        try: 
            c = self.conn.cursor()
            c.execute('SELECT skill_id FROM equipment_skill WHERE equipment_id = ?', (eid,))
            equipment_skill_rows = c.fetchall()
            c.execute('SELECT skill_id FROM user_skill WHERE username = ?', (user,))
            user_skill_rows = c.fetchall()
            return equipment_skill_rows, user_skill_rows

        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
    #keep track of checkout equipment for employees
    def employee_checkout_records(self, checkout_id, user, equipment_name):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO employee_checkout_records (id, username, equipment_name) VALUES (?, ?, ?)',
                        (checkout_id, user, equipment_name)
                    )
            c.execute('INSERT INTO checkout_records (id, username, equipment_name) VALUES (?, ?, ?)',
                        (checkout_id, user, equipment_name)
                    )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Database error:", e)
            self.conn.rollback()
            return False
        finally:
            c.close()
        
    #keep track of checkout equipment of employees for admin
    def admin_checkout_records(self, checkout_id, user, equipment_name):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO checkout_records (id, username, equipment_name) VALUES (?, ?, ?)',
                        (checkout_id, user, equipment_name)
                    )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()
        
    def get_return_equipment(self, user):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM employee_checkout_records WHERE username = ?", (user,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def count_duplicates(self, duplicates_list):
        counts = {}
        for item in duplicates_list:
            name = item["equipment_name"]  # extract the string
            counts[name] = counts.get(name, 0) + 1
        return counts
    
        
    #delete the return equipment from the employee checkout record and update the amdin checkout record
    def return_equipment(self, item_id_or_all, user):
        try:

            if item_id_or_all == "all":
                c = self.conn.cursor()
                c.execute("SELECT equipment_name FROM employee_checkout_records WHERE username = ? ORDER BY equipment_name ASC", (user,))
                rows = c.fetchall()
                return_total =[{'equipment_name': r[0]} for r in rows]
                total = self.count_duplicates(return_total)
                
                # 3. Loop through each equipment name and update quantity
                for eq_name, returned_amount in total.items():

                    # Fetch current quantity
                    eq_data = self.get_equipment_quantity_by_id_or_name('none', eq_name)


                    # eq_data returns [(name, qty)] for name lookup
                    _, current_qty = eq_data[0]

                    # New quantity (return = add back)
                    new_quantity = int(current_qty) + int(returned_amount)

                    # Update DB using equipment name
                    success = self.update_equipment_quantity(new_quantity, 'none', eq_name)
                   
                #delete all records from the employee_checkout_record
                c.execute("DELETE FROM employee_checkout_records WHERE username = ?", (user,))
                #update all records from the checkout_record
                c.execute('UPDATE checkout_records SET equipment_return = ? WHERE username = ?',
                    ('yes',user))
                self.conn.commit()
                return True
            else:
                c = self.conn.cursor()
                #delete a single record from employee
                c.execute("DELETE FROM employee_checkout_records WHERE id = ?", (item_id_or_all,))
                #update a single record for the admin 
                c.execute('UPDATE checkout_records SET equipment_return = ? WHERE id = ?',
                    ('yes',item_id_or_all))
                self.conn.commit()
                return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        except Exception as e:
            print("Error in checkout_records:", e)
            return False
        finally:
            c.close()

    #grab the specific user return data from the database 
    def return_search(self, user):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM checkout_records WHERE username = ?", (user,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def view_all_return(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM checkout_records")
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def maintenance_request(self, item_id_or_all, item_equipment_name, user):
        try:
            c = self.conn.cursor()
            if isinstance(item_id_or_all, list):
                for eq in item_id_or_all:                 
                    c.execute('INSERT INTO maintenance_records (maintenance_id, equipment_name, maintenance_status) VALUES (?, ?, ?)',
                            (eq['id'], eq['equipment_name'], 'pending')
                        )
                    
                c.execute("DELETE FROM employee_checkout_records WHERE username = ?", (user,))
                #update all records from the checkout_record
                c.execute('UPDATE checkout_records SET equipment_return = ? WHERE username = ?',
                    ('sent for maintenance',user))
                self.conn.commit()
                return True
            else:
                c.execute('INSERT INTO maintenance_records (maintenance_id, equipment_name, maintenance_status) VALUES (?, ?, ?)',
                            (item_id_or_all, item_equipment_name, 'pending')
                        )          
                c.execute("DELETE FROM employee_checkout_records WHERE id = ?", (item_id_or_all,))
                #update a single record for the admin 
                c.execute('UPDATE checkout_records SET equipment_return = ? WHERE id = ?',
                    ('sent for maintenance',item_id_or_all))
                self.conn.commit()
                c.close()
                return True
            
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def view_maintenance_request(self):
        try:
           c = self.conn.cursor()
           c.execute("SELECT * FROM maintenance_records") 
           rows = c.fetchall()
           return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()
    def update_maintenance_status(self, status, eid, name):
        try:
            c = self.conn.cursor()
            if status == 'in progress':
                c.execute("UPDATE maintenance_records SET maintenance_status = ? WHERE maintenance_id = ?", 
                        (status, eid))
                self.conn.commit()
                return True
            elif status == 'completed':
                c.execute("UPDATE maintenance_records SET maintenance_status = ? WHERE maintenance_id = ?", 
                        (status, eid))
                c.execute("UPDATE equipment SET quantity = quantity + 1 WHERE name = ?",
                          (name,))
                self.conn.commit()
                return True
            else:
                return False
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    #changing and viewing employees 
    def employee_search(self, user):
        try:
            c = self.conn.cursor()
            c.execute("SELECT username, user_role, employment_status FROM users WHERE username = ?", (user,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def view_employees(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT username, user_role, employment_status FROM users")
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def change_role_or_employment_status(self, user, role_or_status):
        try:
            c = self.conn.cursor()
            if role_or_status == "admin":
                c.execute("UPDATE users SET user_role = ? WHERE username = ?", ('admin', user))
                self.conn.commit()
                return True
            elif role_or_status == 'terminated':
                c.execute("UPDATE users SET employment_status = ? WHERE username = ?", ('terminated', user))
                self.conn.commit()
                return True
            else:
                return False
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def get_all_skills(self):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM skills')
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()    

    def get_search_skill(self, name):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM skills WHERE skills_name = ?", (name,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def insert_employee_skill(self, eid, user):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO user_skill (skill_id, username) VALUES(?, ?)', (eid, user))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()  

    def set_skill(self, skill_name):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO skills (skills_name) VALUES (?)", (skill_name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()  
    
    def get_employee_skills(self, user):
        try:
            c = self.conn.cursor()
            c.execute("SELECT user_skill.username, skills.skills_name FROM user_skill JOIN skills ON user_skill.skill_id = skills.skills_id WHERE user_skill.username = ?", (user,))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()  
        

    def set_request(self, eid, equipment_request, new_request, user):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO request (request_id, equipment_requested, new_equipment_requested, user) VALUES (?,?,?,?)",
                       (eid, equipment_request, new_request, user))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def get_all_request(self, user):
        try:
            c = self.conn.cursor()
            c.execute("SELECT request_id, equipment_requested, new_equipment_requested, request_status FROM request WHERE user = ?",
                      (user, ))
            rows = c.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def get_all_request_admin(self, user):
        try:
            if user != 'none':
                c = self.conn.cursor()
                c.execute("SELECT * FROM request WHERE user = ?", (user,))
                rows = c.fetchall()
                return rows
            else: 
                c = self.conn.cursor()
                c.execute("SELECT * FROM request")
                rows = c.fetchall()
                return rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()

    def update_request_status(self, eid, status):
        try:
            if status == 'in progress':
                c = self.conn.cursor()
                c.execute("UPDATE request SET request_status = ? WHERE request_id = ?",
                        (status, eid))
                self.conn.commit()
                return True
            elif status == 'complete':
                c = self.conn.cursor()
                c.execute("UPDATE request SET request_status = ? WHERE request_id = ?",
                        (status, eid))
                self.conn.commit()
                return True
            else:
                return False

        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()
            
    def generate_all_report(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM checkout_records WHERE equipment_return = 'no' AND checkout_at >= datetime('now', '-14 days')")
            checkout_rows = c.fetchall()
            c.execute("SELECT * FROM request WHERE arrive_at >= datetime('now', '-14 days') ")
            request_rows = c.fetchall()
            c.execute("SELECT * FROM maintenance_records WHERE return_date >= datetime('now', '-14 days')")
            maintenance_rows = c.fetchall()
            return checkout_rows, request_rows, maintenance_rows
        except sqlite3.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            c.close()
            

    def close(self):
        self.conn.close()
        

