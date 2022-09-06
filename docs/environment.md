
# Environment varaible

## Django Settings
- SECRET_KEY : Django secret key
- ALLOWED_HOSTS : List of allowed hosts separeted by comma(,)
- DJANGO_SETTINGS_MODULE = path to the Django settings module

## Database configuration
- DB_NAME : Name of the database
- DB_USER_NAME : Username of the database user
- DB_PASSWORD : Corresponding passwor for the user

## S3 Storage
> In Onmode, the files have been separated into three categories namely, static, media, and private.
> **NOTE: each category must have its own bucket**.
> - static files: all files related to site configuration and templates
> - media files: all user uploaded files
> - private: collection and category poster, site logo, site fav icon,...

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_S3_ENDPOINT_URL
- PUBLIC_MEDIA_BUCKET_NAME : bucket name specified to user uploaded files
- STATIC_FILES_BUCKET_NAME : bucket name specified to static files
- PRIVATE_MEDIA_BUCKET_NAME : bucket name specified to admin uploaded files

## SMS Setup
Based on ippanle, in Onmode, there are three different API KEY (or branch) for handling SMS
- SELLER_SMS_API_KEY : This KEY only used for **Shopkeepers**
- CUSTOMER_SMS_API_KEY : This KEY only used for **Customers**
- VERIFICATION_SMS_API_KEY : This key only use for **OTP**
- VERIFICATION_CODE_SMS_CODE : A pattern code for **OTP** that has _code_ parameter
- SMS_NUMBER : The SMS service specified **number**

# Shop and Users
- MAX_STORAGE: Maximum size of storage allocated for each shopkeeper to upload the product images.

- SHOP_MAX_PRODUCT : Maximum number of products that a shop can have.
