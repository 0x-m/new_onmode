from importlib import import_module
from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = "public-read-write"
    bucket_name = config("PUBLIC_MEDIA_BUCKET_NAME", "")
    custom_domain = "%s.s3.ir-thr-at1.arvanstorage.com" % bucket_name


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    bucket_name = config("STATIC_FILES_BUCKET_NAME", "")
    custom_domain = "%s.s3.ir-thr-at1.arvanstorage.com" % bucket_name


class SiteStorage(S3Boto3Storage):
    location = "site"
    default_acl = "public-read"
    bucket_name = config("PRIVATE_MEDIA_BUCKET_NAME", "")
    custom_domain = "%s.s3.ir-thr-at1.arvanstorage.com" % bucket_name
