import frappe
from pydantic import BaseModel


# Sample ENV Variable from site-settings.json
class Settings(BaseModel):
    api_url: str = frappe.conf.get("api_url")
