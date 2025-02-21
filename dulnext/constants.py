import frappe


class Constants:
    # Add more values to create more roles
    DEFAULT_CREATED_ROLES = ["Meteor Employee", "Bati Employee"]
    IS_DEVELOPMENT_MODE = frappe.conf.get("developer_mode") == 1
