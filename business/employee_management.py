from data.database import Database

class EmployeeManager:
    def __init__(self):
        self.db = Database()

    def employee_search(self, user)-> tuple[bool, list]:
        success = self.db.employee_search(user)
        employees_data = []
        if success:
            for item in success:
                employees_data.append({
                    "username": item[0],
                    "role": item[1],
                    "employment_status": item[2],
                    
                })
            return True, employees_data
        else: 
            return False, employees_data
        
    def view_employees(self) -> tuple[bool, list]:
        success = self.db.view_employees()
        employees_data = []
        if success:
            for item in success:
                employees_data.append({
                    "username": item[0],
                    "role": item[1],
                    "employment_status": item[2],
                    
                })
            return True, employees_data
        else: 
            return False, employees_data
        
    def change_role_or_employment_status(self, user, role_or_status) -> tuple[bool, str]:
        success = self.db.change_role_or_employment_status(user, role_or_status)

        if success:
            return True, "Success"
        else:
            return False, "Unknown error. Please try again"
        
    def get_all_skills(self) -> tuple[bool, list]:
        success = self.db.get_all_skills()
        skills_data = []
        if success:
            for item in success:
                skills_data.append({
                    "skills_id": item[0],
                    "skills_name": item[1],
                    
                })
            return True, skills_data
        else: 
            return False, skills_data
        
    def get_search_skill(self, name)-> tuple[bool, list]:
        success = self.db.get_search_skill(name)
        skills_data = []
        if success:
            for item in success:
                skills_data.append({
                    "skills_id": item[0],
                    "skills_name": item[1],
                    
                })
            return True, skills_data
        else: 
            return False, skills_data
    
    def insert_employee_skill(self, eid, user) -> tuple[bool, str]:
        success = self.db.insert_employee_skill(eid, user)
        if success:
            return True, f"Skill Added to {user}."
        else: 
            return False, "Unknown error!!! Please try again."
        
    def get_employee_skills(self, user):
        success = self.db.get_employee_skills(user)
        skills_data = []
        if success:
            for item in success:
                skills_data.append({
                    "username": item[0],
                    "skills_name": item[1],
                    
                })
            return True, skills_data
        else: 
            return False, skills_data
        pass