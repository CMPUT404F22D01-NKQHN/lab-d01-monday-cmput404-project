from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'bucketeer-dd7c6bfa-8eae-4046-855d-2ca11cc087e6'
    location = 'media'
    object_parameters = {
        'CacheControl': 'max-age=31536000',
    }
    
