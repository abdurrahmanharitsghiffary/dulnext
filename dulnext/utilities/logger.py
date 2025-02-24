import frappe


class Logger:
    Dulnext = frappe.logger("dulnext")
    Controller = frappe.logger("dulnext.controllers")
