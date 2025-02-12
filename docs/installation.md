# Installation Guide

This guide explains how to set up your Dulnext site using **frappe-bench**. For more detailed instructions, please refer to the [Frappe Documentation](https://docs.frappe.io/framework/user/en/introduction).

## Prerequisites

Before proceeding, ensure that you have the following installed:

- Python (version 3.6+ recommended)
- Node.js and Yarn
- Redis
- MariaDB/MySQL
- Bench CLI (Install via pip: pip install frappe-bench)

## Step 1: Install frappe-bench

If you haven’t already installed `frappe-bench`, follow the official [Frappe Installation](https://docs.frappe.io/framework/user/en/installation) Guide. For example, you can initialize a new bench with:

```bash
pip install frappe-bench
bench init my-bench --frappe-branch version-15
# This project only optimized for frappe version 15, it may be broken if using newer or older version.
```

## Step 2: Create a New Site

Navigate to your bench directory and create a new site. Replace your-site.local with your desired site name:

```bash
cd my-bench
bench new-site your-site.local
```

You will be prompted to enter your MySQL root password and set an Administrator password for the new site.

## Step 3: Configure the Site

Our Dulnext project includes a sample configuration file, site-config.example.json, which is analogous to a .env.example file for Frappe. Copy this file to your site’s configuration file:

```bash
cp site-config.example.json sites/your-site.local/site_config.json
```

Edit sites/your-site.local/site_config.json as needed to customize the settings for your environment.

## Step 4: Install the Dulnext App

Within your bench directory, add and install the Dulnext app:

Get the Dulnext App:

```bash
bench get-app https://github.com/abdurrahmanharitsghiffary/dulnext.git
```

Install the App on Your Site:

```bash
bench --site your-site.local install-app dulnext
```

## Step 5: Start the Bench

Once everything is installed and configured, start the bench server:

```bash
bench start
```

Your site should now be up and running. You can access it via your browser at http://your-site.local:8000 (or the configured host/port).

## Troubleshooting

- **Dependencies**: Double-check that all required dependencies are installed.
- **Configuration**: Review your site_config.json for any errors.
- **Frappe Docs**: Refer to the [Frappe Framework Documentation](https://docs.frappe.io/framework/user/en/introduction) for additional troubleshooting and advanced configuration options.
