from apps.devdb2024.models import *
import pysnooper


# ROUTED_MODELS = ["Route", "Driver", "VehicleType", "Vehicle", "Passenger", "Schedule", "Ticket", "Test"]
class MyDBRouter(object):
    """
        A router to control all database operations on models in the
        auth application.
    """
    route_app_labels = {"devdb2024"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read remote models go to remote database.
        """
        if model._meta.app_label in self.route_app_labels:
            return "devdb"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write remote models go to the remote database.
        """
        if model._meta.app_label in self.route_app_labels:
            return "devdb"
        return None

    # def allow_relation(self, obj1, obj2, **hints):
    #     """
    #     Do not allow relations involving the remote database
    #     """
    #     if obj1._meta.app_label == 'remote' or \
    #             obj2._meta.app_label == 'remote':
    #         return False
    #     return None
    #
    # @pysnooper.snoop()
    def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     """
    #     Do not allow migrations on the remote database
    #     """
    #     if model._meta.app_label == 'remote':
    #         return False

        if app_label in self.route_app_labels:
            return db == "devdb"
        return None


class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    route_app_labels = {"auth", "contenttypes"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels
                or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "default"
        return None