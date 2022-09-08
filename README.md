
[![Visual Studio Code](https://img.shields.io/badge/--007ACC?logo=visual%20studio%20code&logoColor=ffffff)](https://code.visualstudio.com/)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)   [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![python version](https://img.shields.io/badge/Python-3.7-green.svg)](https://shields.io/) [![django version](https://img.shields.io/badge/Django-4.0-green.svg)](https://shields.io/) [![DRF](https://img.shields.io/badge/DRF-armygreen.svg)](https://shields.io/)
 [![Website fakesite.invalid](https://img.shields.io/website-up-down-green-red/http/fakesite.invalid.svg)](http://fakesite.invalid/) [![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

 # Introduction
Onmode is a **multi-vendor E-commerce platform** targeting fashion retailers.
Onmode is a multi-vendor E-commerce platform targeting fashion retailers. Onmode aimed to empower retailers by providing them with basic online shopping capabilities including customer management, sales management, product management, and order management, and especially, undertakes the process of shipping parcels, tracking them, and handling related issues. Furthermore, All User activities related to products, shops, and orders,... may be accessed via REST API endpoints, which facilitates the development of custom apps, robots, and analyzers.

### How Onmode works:

1. Customers may pick any number of products from different shops and add them to their cart, in the cart page, the added products are grouped by the shop and a new order is created per each of these groups.

2. Customer may pick an order up (let it belongs to the ABC shop!), check it out, and after completing some forms, and paying the order off (directly or via the wallet), the ABC shopkeeper receives an SMS containing information about the new order also, the shopkeeper can see the new registered order in the site's dashboard. The shopkeeper may confirm or cancel the order, Also the corresponding customer can cancel the order before the shopkeeper confirms it.

3. After the order confirmation, a new form below the order is appeared (for the shopkeeper) that asks for the Order tracking code, the shopkeeper must prepare and send the order to the customer, then fill the tracking code form.

4. After that the shopkeeper registered the tracking code, The Admin user must check the code and verify its validity. If the admin verifies the code then the order goes to the Sent state and the user can see the I have received the order button! pressing this button means the process is successfully terminated. If the code was invalid, the admin can leave a message for the shopkeeper and reject the code, in this case, the shopkeeper will be asked again to provide a valid tracking code.


**SMS Notification** is another onmode feature, the user will be touched after making an order or their orders got accepted (Rejected|canceled|prepared or sent) by the corresponding shopkeeper. Also, shopkeepers receive SMS when new orders arrived at their shops, users cancel their orders, or after users


**Onmode** extensible architecture provides for the definition of fully customizable products with custom-defined options and attributes, in which each attribute has a Type and Default value(s), and each product may have any number of options. (Currently, only the admin can define custom product options). In addition, products may be categorized or gathered into collections. (Currently, only the admin can define category and collection)

# Demo
A demo is available on [this link](https://oxm.pythonanywhere.com/)

![add-product-img](https://github.com/0x-m/new_onmode/blob/main/docs/img/add-product-3.png?raw=true)

**NOTE: SOME Features are disabled (including sms service) thus, it wouldn't be possible to regisert a new user!**
Inorder to login:
> goto [admin-login](https://oxm.pythonanywhere.com/admin)
> - phone number: 09919931212
> - password: 123

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
- Frontend: Tailwind css, Django templates
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
        - mkdocs for  documentation
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


# Installation

- Create and activate a new virtual environment

    > `python3 -m venv .env && source .env/bin/activate`

- Clone the this repository:

    > `git clone https://github.com/0x-m/new_onmode.git`

- Install dependencies

    > `python -m pip install -r requirements/dev.txt`

- Install all migrations

    > `python manage.py migrate`

- Run the development server

    > `python manage.py runserver --settings onmode.settings.dev`

## Using docker

**NOTE**: both way are for development only.

- Goto to the http://localhost:8000 to visit the site
- REST APIS URL: http://localhost:8000/api/v1/
- API DOCS URL: http://localhost:8000/api/v1/docs/swagger/
# Contribute & Support
- This repository was a private project and currently, I have no plan for further development or support!


# License
See the [LICENSE](https://github.com/0x-m/new_onmode/blob/main/LICENSE) file for licensing information.
