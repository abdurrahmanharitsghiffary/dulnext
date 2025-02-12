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

To learn how to set up and develop this project, check out the [Tutorial Guide](./TUTORIAL.md).
This guide covers installation, configuration, and best practices for working with Virtual Doctypes.

## License

This project is licensed under the MIT License.
