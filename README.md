
# Introduction

Onmode is a **multi-vendor E-commerce platform** targeting fashion retailers.
Onmode aimed to empower retailers by providing them with basic online shopping capabilities including customer management, sales management, product management, and order management, and especially, undertakes the process of shipping parcels, tracking them, and handling related issues. Forthemore, All User activities and other informations including (products, shops, orders,...) may be accessed via REST API endpoints, which facilitates the development of custom apps, robots, and analyzers.

# Features
- **For users**:
    - Simple dashboard for users to handle their activities including, tracking orders, listing their desired products on wishlist, and managing their comments, wallets, and tickets.
    - Any user may demand having a custom shoppage, selling products, and managing orders and sales.
    - The shop may have an URL like : https://onmode.ir/<desired_shop_name>/
    - Ticket system for answering users questions and problems.
    - Custom shopping cart specialized for multi-vendor shopping.
    - Rating system for shopkeepers and products.
    
- **For admin**:
    - Customized Django admin panel for site management.
    - Categories up to 5 nested levels.
    - Create customizable collections of products.
    - Three levels of discount:
        - The shopkeeper can define discounts for his(or her) products.
        - Admin users can define discounts for any product.
        - Admin users can define discounts for a collection that may apply to some (or all) products belonging to that collection.
    - Create collections of shops.
    - Coupon system.
    - Create an arbitrary static page.
    - Flitering, importing, and exporting information(ex. Products, Orders,... ) in common formats (ex. XML, JSON, XLSX,..).
    - SMS services for user activities.
    - All site static files and user uploaded files may be served through any S3 compatible service (ex. Amazon S3, Arvan cloud)
    (**I used Arvancloud for CND and file serving**)

    - Admin can configure the following properties for each shop individually:
        - The maximum number of products a shop can have.
        - The maximum file storage size a shop can use.
        - Fee per transaction of a shop.
        **Also, the Default values for each of the above fields can be configured via Environment variables**

## Technologies
- Backend: 
    - Programming: Pyhton, Django, Django Rest Framework
    - Deployment: Gunicorn
    - Database: Postgresql, SQLite
    - Other modules:
        - venv for virtual environment
        - IPPanel for sms service
        - Boto3 for S3 storage
        - MPTT for implementing nested category architecture.
        - tinymce (a simple WYSIWYG editor)
        - django_jalai_date
        - django_filters 
        - Spectacular for API Doumentation and schema.
        - Spinx for project documentation
        - Black for code formatting
        - mypy for static code analysis
        - faker for dump data generation
        - locust for API load testing
        - python_decouple for env variable management
        - precommit for checking coding style, format,... before commit
        - django-silk for profiling
        - allauth for provides social media login
        - simple_jwt 
        - corsheaders
        - django_imports_exports for importing, and exporting data in common formats (ex. XML, JSON,...)
- Frontend: Tailwind css, Django templates


# Installation

1) clone the repository: `git clone ...`
2) change to the directory: `cd ...`
3) [Optional]: create a virtual environment: 'python3 -m venv venv'
4) [Optiona]: activate the virtual environment: `source venv/bin/activate`
5) install the requirements: `pip install -r requirements.txt`
6) Run the development server: `python manage.py runserver`

# Contribute & Support
- This repository was a private project and currently, I have no plan for further development or support!



# License






