class DriverRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label  == "driverForm":
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'driverForm':
            return 'default'
        return None

class HospitalRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label  == "dashboard":
            return 'hospital_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'dashboard':
            return 'hospital_db'
        return None