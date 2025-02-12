# Dulnext - Virtual Doctype Frappe Template

A custom Frappe template built and maintained by Myself.
This project is focused on building Doctypes using Virtual Doctype for better flexibility and performance.

## Project Structure

The project follows the structure below:

```bash
/TUTORIAL.md # Documentation on how to set up, develop, and contribute to the project.
/site-config.example.json # Equivalent to .env.example but in frappe version
/dulnext               # Root project directory
├── /dulnext           # Core Frappe files
├── /controllers       # Custom controllers
├── /jobs             # Cron job tasks
├── /libs             # Third-party libraries
├── /models           # Application models
├── /setup            # Configuration used in hooks.py
├── /translations     # CSV files for translations
├── /utilities        # Shared utility functions
└── /custom           # Custom Doctype and other customizations
```

## Getting Started

To set up and develop this project, please refer to the following guides:

- **Installation Guide**: Learn how to install and configure the project using frappe-bench in our [Installation Guide](./docs/installation.md).
- **Tutorial**: For best practices on working with Virtual Doctypes, please refer to our [comprehensive tutorial](./TUTORIAL.md).

These documents cover everything from prerequisites and setup to advanced usage and recommended conventions for Virtual Doctypes.

## Disclaimer

**Dulnext** is an independent project and is not affiliated with, endorsed by, or associated with **ERPNext**, **Frappe Technologies**, or any of their products. The name **"Dulnext"** was inspired by **ERPNext** but is a separate and **standalone project**. All trademarks, product names, and logos mentioned are the property of their respective owners.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.
