from dataclasses import dataclass

from frappe.types import DF


@dataclass
class PostEntity:
    dfqintuser_id: DF.Int
    dfqintid: DF.Int
    dfqdtatitle: DF.Data
    dfqtxtbody: DF.Text
