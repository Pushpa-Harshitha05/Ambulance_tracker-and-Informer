class DriverRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label  == "driverForm":
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'driverForm':
            return 'default'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'driverForm':
            return db == 'default'
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
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'dashboard':
            return db == 'hospital_db'
        return None