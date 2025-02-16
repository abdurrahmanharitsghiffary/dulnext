import frappe


class Constants:
    DEFAULT_CREATED_ROLES = ["Meteor Employee", "Bati Employee"]
    IS_DEVELOPMENT_MODE = frappe.conf.get("development_mode") == 1
