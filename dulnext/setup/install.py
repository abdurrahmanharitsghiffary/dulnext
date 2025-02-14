import frappe


def after_install():
    add_standard_navbar_items()
    add_app_name()
    hide_workspaces()
    change_app_logo()
    # create_default_roles()
    # create_default_role_profiles()
    frappe.db.commit()


def add_company_to_session_defaults():
    settings = frappe.get_single("Session Default Settings")
    settings.append("session_defaults", {"ref_doctype": "Company"})
    settings.save()


def add_standard_navbar_items():
    navbar_settings = frappe.get_single("Navbar Settings")

    erpnext_navbar_items = [
        {
            "item_label": "Documentation",
            "item_type": "Route",
            "route": "https://docs.erpnext.com/",
            "is_standard": 1,
        },
        {
            "item_label": "User Forum",
            "item_type": "Route",
            "route": "https://discuss.frappe.io",
            "is_standard": 1,
        },
        {
            "item_label": "Frappe School",
            "item_type": "Route",
            "route": "https://frappe.school?utm_source=in_app",
            "is_standard": 1,
        },
        {
            "item_label": "Report an Issue",
            "item_type": "Route",
            "route": "https://github.com/frappe/erpnext/issues",
            "is_standard": 1,
        },
    ]

    current_navbar_items = navbar_settings.help_dropdown
    navbar_settings.set("help_dropdown", [])

    for item in erpnext_navbar_items:
        current_labels = [item.get("item_label") for item in current_navbar_items]
        if item.get("item_label") not in current_labels:
            navbar_settings.append("help_dropdown", item)

    for item in current_navbar_items:
        navbar_settings.append(
            "help_dropdown",
            {
                "item_label": item.item_label,
                "item_type": item.item_type,
                "route": item.route,
                "action": item.action,
                "is_standard": item.is_standard,
                "hidden": item.hidden,
            },
        )

    navbar_settings.save()


def add_app_name():
    frappe.db.set_single_value("System Settings", "app_name", "Synapsefi Baas")


def create_default_roles():
    for role in DEFAULT_ROLES:
        if not frappe.db.exists("Role", role):
            role_doc = frappe.new_doc("Role")
            role_doc.role_name = role
            role_doc.insert(ignore_permissions=True)

        add_permission_to_role(role, "Synapsefi Sample")


def add_permission_to_role(role, doctype):
    """Grant full access to synapsefi_sample for a role"""
    if not frappe.db.exists("Custom DocPerm", {"role": role, "parent": doctype}):
        docperm = frappe.new_doc("Custom DocPerm")
        docperm.parent = doctype
        docperm.parenttype = "DocType"
        docperm.parentfield = "permissions"
        docperm.role = role
        docperm.permlevel = 0
        docperm.read = 1
        docperm.write = 1
        docperm.create = 1
        docperm.delete = 1
        docperm.submit = 1
        docperm.cancel = 1


def create_default_role_profiles():
    for role_profile_name, roles in DEFAULT_ROLE_PROFILES.items():
        role_profile = frappe.new_doc("Role Profile")
        role_profile.role_profile = role_profile_name
        for role in roles:
            if not frappe.db.exists("Role Profile", role):
                role_profile.append("roles", {"role": role})

        role_profile.insert(ignore_permissions=True, ignore_if_duplicate=True)


def change_app_logo():
    frappe.db.set_single_value("Navbar Settings", "app_logo", "/assets/dulnext/images/pop-cat.jpg")


DEFAULT_ROLES = [
    "User Manager",
    "Nodes Manager",
    "Subnets Manager",
    "Shipments Manager",
    "Statements Manager",
    "Transactions Manager",
    "Subcriptions Manager",
    "Misc Manager",
]


DEFAULT_ROLE_PROFILES = {
    "Synapsefi Baas Administrator": [
        "User Manager",
        "Nodes Manager",
        "Subnets Manager",
        "Shipments Manager",
        "Statements Manager",
        "Transactions Manager",
        "Subcriptions Manager",
        "Misc Manager",
    ],
    "Synapsefi Baas Accounting": [
        "Statements Manager",
        "Transactions Manager",
    ],
    "Synapsefi Baas Operations": [
        "User Manager",
        "Nodes Manager",
        "Subnets Manager",
        "Shipments Manager",
    ],
    "Synapsefi Baas Compliance": [
        "User Manager",
        "Transactions Manager",
        "Statements Manager",
    ],
    "Synapsefi Baas Support": [
        "User Manager",
        "Subcriptions Manager",
        "Misc Manager",
    ],
}


def hide_workspaces():
    for ws in ["Integrations", "Settings"]:
        frappe.db.set_value("Workspace", ws, "is_hidden", 1)
