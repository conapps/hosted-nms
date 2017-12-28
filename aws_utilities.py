"""
Script to upload files and folders to Amazon S3 service
"""

# import boto3 SDK
import boto3
# import system module to handle local folders and files
import os
# import sys module to use some variables used by the interpreter
import sys
# import exceptions to handle connectivity and AWS S3 authentication errors
from botocore.exceptions import EndpointConnectionError, ClientError

s3 = boto3.client('s3')
# define the name of the AWS S3 bucket to use
bucket = 'conapps-cloud-pbx'


def upload_file(file_name, target_name, delete=False):
    """
    Function to upload an object called file_name within target_name folder in AWS S3. If delete parameter
    is true, it also remove file_name from source.
    :param file_name: Name of the file to upload/delete
    :param target_name: Full path where the file will be upload into the bucket
    :param delete: This function will also delete file_name from local disk if: the upload was successfully and delete=True
    :return: Return true/false boolean if the operation was successfully
    """
    print("Uploading file... " + target_name)
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, bucket, target_name)
        if delete:
            print("Deleting file... " + file_name)
            os.remove(file_name)


def upload_dir_content(local_directory, cloud_directory, delete=False):
    """
    Function that go through local file system and upload files and folders into AWS S3
    :param local_directory: local directory of the file system
    :param cloud_directory: remote directory of the AWS S3 where the file/folder will be created
    :param delete: This function will also delete the folder from local disk if delete flag is True
    :return: void
    """
    for item in os.scandir(path=local_directory):
        if item.is_dir():
            upload_dir_content(local_directory + item.name + "/", cloud_directory + item.name + "/")
            if delete:
                print("Deleting folder..." + item.name)
                os.rmdir(item.path)
        else:
            upload_file(local_directory + item.name, cloud_directory + item.name, delete)


if __name__ == "__main__":
    folder = os.getcwd() + "/"
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    finish = False
    response = input("Are you sure do you want to upload: " + folder + " and all its contents to S3? (y or n): ")
    while not finish:
        if response.lower() == "n":
            exit()
        elif response.lower() == "y":
            finish = True
        else:
            response = input("Don't play with me! (y or n)")
    upload_dir_content(folder, '')