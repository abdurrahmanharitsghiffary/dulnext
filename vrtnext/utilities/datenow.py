from datetime import datetime

import frappe
import frappe.utils
import pytz


def datenow(timezone: str):
    local_time = datetime.now()
    return pytz.timezone(timezone).localize(local_time)


def frappedatenow():
    """Get current time in frappe System Timezone."""

    return datenow(frappe.utils.get_system_timezone())
