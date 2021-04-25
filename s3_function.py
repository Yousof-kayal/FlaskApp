import boto3
global bucket
bucket = 'qrgenerator-code'

def upload_file(filename: object, bucket: object) -> object:
    object_name = (f'{filename}')
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket, object_name)

    return response

def download_file(filename, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"{filename}"
    s3.Bucket(bucket).download_file(filename, output)

    return output

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents