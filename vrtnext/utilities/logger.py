import frappe


class Logger:
    VRTNext = frappe.logger("vrtnext")
    Controller = frappe.logger("vrtnext.controllers")
