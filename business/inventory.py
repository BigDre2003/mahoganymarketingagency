from data.database import Database
import random

class InventoryManager:
    def __init__(self):
        self.db = Database()
    #grab all equipment from the database
    def list_equipment(self) -> tuple[bool, list]:
        success = self.db.get_all_equipment()
        equipmentList_data = []
        if success:
            for item in success:
                equipmentList_data.append({
                    "id": item[0],
                    "name": item[1],
                    "quantity": item[2]
                })
            return True, equipmentList_data
        else: 
            return False, equipmentList_data
        
    def get_equipment_from_secondWarehouse(self, name) -> tuple[bool, list]:
        success = self.db.get_secondWarehouse_equipment(name)
        equipmentList_data = []
        if success:
            for item in success:
                equipmentList_data.append({
                    "id": item[0],
                    "name": item[1],
                    "quantity": item[2]
                })
            return True, equipmentList_data
        else: 
            return False, equipmentList_data

        
    def get_search_equipment(self, equipment_name) -> tuple[bool, list]:
        success = self.db.get_search_equipment(equipment_name)
        equipmentList_data = []
        if success:
            for item in success:
                equipmentList_data.append({
                    "id": item[0],
                    "name": item[1],
                    "quantity": item[2]
                })
            return True, equipmentList_data
        else: 
            return False, equipmentList_data
    
    #add equipment to the database
    def add_equipment(self, name: str, quantity: int, skill: str)  -> tuple[bool, str]:
        success = self.db.add_equipment(name, quantity, skill)
        if success:
            return True, "Equipment Added"
        else:
            return False, "Error. Please try again"
        
    #remove equipment from the database
    def remove_equipment(self, eid: int) -> tuple[bool, str]:
        success = self.db.remove_equipment(eid)
        if success:
            return True, "Equipment Remove"
        else:
            return False, "Error. Please try again"
    
    #grab all the equipment quantity from the database
    def get_all_equipment_quantity(self):
        #quantity = self.db.get_equipment_quantity()
        return self.db.get_all_equipment_quantity()
    
    #grab the specific equipment quantity from the database
    def get_equipment_quantity_by_id(self, eid):
        return self.db.get_equipment_quantity_by_id_or_name(eid, 'none')
    
    
    #update equipment quantity in the database
    def update_equipment_quantity(self, quantity: int, eid: int):
        return bool(self.db.update_equipment_quantity(quantity, eid, 'none'))
        # if success:
        #     return True
        # else:
        #     return False
        
    def verify_skills(self, eid:int, user:str):
        equipment_skill_rows_success, user_skill_rows_success = self.db.skills_check(eid, user)
        equipment_skill_rows = []
        user_skill_rows = []
        if equipment_skill_rows_success and user_skill_rows_success:
            for item in equipment_skill_rows_success:
                equipment_skill_rows.append({
                    "skill_id": item[0],
                })
            
            for item in user_skill_rows_success:
                user_skill_rows.append({
                    "skill_id": item[0],
                })
            common = [eq for eq in equipment_skill_rows if eq in user_skill_rows]
            if not common:
                return False
            else:
                return True
        else:
            return False


    #checkout the equipment from the database
    def checkout_equipment(self, eid: int, total: int, user:str) -> tuple[bool, str]:
        skills_check = self.verify_skills(eid, user)
        if skills_check:
            quantity = self.db.checkout(eid)
            new_quantity = quantity
            if new_quantity > 0:
                new_quantity = new_quantity - total
                success = self.update_equipment_quantity(new_quantity, eid)
                if success:
                    return True, "Checkout successful"
                else:
                    return False, "Unknown Error. Please try again"
            elif new_quantity == 0:
                return False, "Out of stock"      
            else:
                return False, "Equipment Unavailable"
        else:
                return False, "User doesn't have required skills."
        
    
    #insert data into checkout_records
    def checkout_records(self, user: str, equipment_name: str, total: int) -> tuple[bool, str]:
        try: 
           
            for _ in range(total):
                eid = random.randint(1000, 9999)
                success = self.db.employee_checkout_records(eid, user, equipment_name)
                if not success:
                    return False, "An unexpected error occurred. Please try again"
            return True, "Checkout Successful"
        except Exception as e:
            print("Error in checkout_records:", e)
            return False, "An unexpected error occurred. Please try again"
        

    #retrieve employee_checkout_records data
    def get_return_equipment(self, user:str ) -> tuple[bool, list]:
        success = self.db.get_return_equipment(user)
        equipment_data = []
        if success:
            for item in success:
                equipment_data.append({
                    "ID": item[0],
                    "username": item[1],
                    "equipment_name": item[2],
                    "checkout_at": item[3]
                })
            return True, equipment_data
        else: 
            return False, equipment_data
        

    #update the employee_checkout_records and checkout_records
    def update_return_equipment(self, item_id_or_all, user) -> tuple[bool, str]:
        success = self.db.return_equipment(item_id_or_all, user)
        if success:
            return True, "Return Successful"
        else:
            return False, "Error. Please try again."

    def return_search(self, user:str) -> tuple[bool, list]:
        success = self.db.return_search(user)
        return_data = []
        if success:
            for item in success:
                return_data.append({
                    "ID": item[0],
                    "username": item[1],
                    "equipment_name": item[2],
                    "equipment_return": item[3],
                    "checkout_at": item[4],
                    "return_at": item[5]
                })
            return True, return_data
        else: 
            return False, return_data
        
    def view_all_return(self) -> tuple[bool, list]:
        success = self.db.view_all_return()
        return_data = []
        if success:
            for item in success:
                return_data.append({
                    "ID": item[0],
                    "username": item[1],
                    "equipment_name": item[2],
                    "equipment_return": item[3],
                    "checkout_at": item[4],
                    "return_at": item[5]
                })
            return True, return_data
        else: 
            return False, return_data
    
        
    def set_skill(self, skill_name) -> tuple[bool, str]:
        success = self.db.set_skill(skill_name)
        if success:
            return True, "Skill added!!!"
        else:
            return False, "Unknown Error. Please try again"

        
    
