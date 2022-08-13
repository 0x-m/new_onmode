
Onmode fashion shopping platform
==========================

Onmode is an E-commerce platform that helps fashion vendors to have their shopping webpage,  connect to their customers and manage their sales.


==========================
Features 
==========================

1) Simple signup process, only a phone number is needed and authentication will be done through a code sent to the user's phone. after signup, users may need to complete their profile information.

2) Users have a simple and intuitive dashboard for managing their activities including wishlist, comments, orders, personal information, wallet, tickets, and their shop if have any.



3) Users could have a shop page with their desired name (if available)  to sell their products. 
 The Shop page has a customizable header (poster), logo, and shop description.

3) SEO friendly, products and shop pages have meta title, meta keywords, and meta description fields, all user's uploaded images also have alt text field.

4) Categories up to 5 nested levels!

5) Ticket system for solving user problems.

8) Intuitive Shopping Cart specialized for multi-vendor shopping

9) 

Administration
==============
A) Customized Django Admin Panel for site management

B) Creating customizable collections of products, each collection has its customizable page. 

C) Three levels of Discount,
        each vendor user could define a discount on his(her) product (via sales price field)
        admin could define discount for any product (by creating an discount instance through the admin panel)
        each collection could have a discount model which may be applied to the selected products belongs to that collection

D) Create a collection of shops

E) Coupon system

F) Create customizable static pages. (ex. About-us, contact-us, policies,...)

G) Admin can adjust the number of products that a user could add to his(her) shop, the maximum size of images users upload, the transaction fee for each shop, and ...

H) All media and static files can be served through a S3 compatible service (ex. Amazon S3, Arvan Cloud Storage,..)

I) Import and export in many formats (pdf, xml, json, xls, xslx,...)

J) 

=================
Technologies
=================
Programming language: Python 3.10
Web framework: Django 4.0
Database: Tested with SQLite, Postgresql, MYSQL (needs additional configuration)
Other modules:
    ippanel SMS
    boto3 for s3 storage (Can be configured through env variables)
    pytest
    Django Rest Framework for REST API
    Sphinx for documentation

=================
Installation
=================
1) clone the repository: `git clone ...`
2) change to the directory: `cd ...`
3) [Optional]: create a virtual environment: 'python3 -m venv venv'
4) [Optiona]: activate the virtual environment: `source venv/bin/activate`
5) install the requirements: `pip install -r requirements.txt`
6) Run the development server: `python manage.py runserver`


=================
Contribute
=================

=================
Support
=================

=================
License
=================

The project is licensed under the BSD license.







