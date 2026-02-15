from data.database import Database
import random

class RequestManager:
    def __init__(self):
        self.db = Database()
    
    def maintenance_request(self, item_id_or_all, item_equipment_name, user) -> tuple[bool, str]:
        success = self.db.maintenance_request(item_id_or_all, item_equipment_name, user)
        if success:
            return True, "Maintenance request successful."
        else:
            return False, "Error. Please try again."
        
    def view_maintenance_request(self) -> tuple[bool, list]:
        success = self.db.view_maintenance_request()
        maintenance_data = []
        if success:
            for item in success:
                maintenance_data.append({
                    "maintenance_id": item[0],
                    "equipment_name": item[1],
                    "maintenance_status": item[2],
                    "request_date": item[3],
                    "return_date": item[4],
                    
                })
            return True, maintenance_data
        else: 
            return False, maintenance_data
                
    def update_maintenance_status(self, status, eid, name) -> tuple[bool, str]:
        success = self.db.update_maintenance_status(status, eid, name)
        if success:
            return True, "Sent for maintenance."
        else:
            return False, "Error. Please try again."
        
    def set_request(self, equipment_request, new_request, user) -> tuple[bool, str]:
        try: 
            eid = random.randint(1000, 9999)
            success = self.db.set_request(eid, equipment_request, new_request, user)
            if success:
                return True, "Request created."
            else:
                return False, "An unexpected error occurred. Please try again."
        except Exception as e:
            print("Error in request:", e)
            return False, "An unexpected error occurred. Please try again."
    
    def get_all_request(self, user) -> tuple[bool, list]:
        success = self.db.get_all_request(user)
        request_data = []
        if success:
            for item in success:
                request_data.append({
                    "request_id": item[0],
                    "equipment_request": item[1],
                    "new_request": item[2],
                    "request_status": item[3],
                    
                })
            return True, request_data
        else: 
            return False, request_data
        
    def get_all_request_admin(self, user) -> tuple[bool, list]:
        success = self.db.get_all_request_admin(user)
        request_data = []
        if success:
            for item in success:
                request_data.append({
                    "request_id": item[0],
                    "equipment_request": item[1],
                    "new_request": item[2],
                    "user": item[3],
                    "request_status": item[4],
                    "request_at": item[5],
                    "arrive_at": item[6],
                    
                })
            return True, request_data
        else: 
            return False, request_data
        
    def update_request_status(self, eid, status) -> tuple[bool, str]:
        success = self.db.update_request_status(eid, status)
        if success:
            return True, "Request status updated."
        else:
            return False, "Error! Please try again."
        
    def generate_all_report(self) -> tuple[bool, list, list, list]:
        checkout_rows, request_rows, maintenance_rows = self.db.generate_all_report()
        return checkout_rows, request_rows, maintenance_rows
        # try:
        #     checkout_rows, request_rows, maintenance_rows = self.db.generate_all_report()

        #     if checkout_rows and request_rows and maintenance_rows:
        #         return True, checkout_rows, request_rows, maintenance_rows
        #     else:
        #         return False, checkout_rows, request_rows, maintenance_rows
        # except Exception as e:
        #     print("Error in generating reprot:", e)
        #     return False, "An unexpected error occurred. Please try again"

     