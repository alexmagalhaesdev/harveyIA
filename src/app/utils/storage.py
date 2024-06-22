import boto3
from botocore.client import Config
from typing import Union

from core.config import settings


class Storage:
    @staticmethod
    def __get_s3_client() -> boto3.client:
        """Returns an S3 client."""
        s3_client = boto3.client(
            "s3",
            endpoint_url=settings.storage.STORAGE_CONNECTION_URL,
            aws_access_key_id=settings.storage.STORAGE_KEY_ID,
            aws_secret_access_key=settings.storage.STORAGE_SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )
        return s3_client

    @staticmethod
    def list_objects_in_bucket(
        bucket: str = settings.storage.STORAGE_BUCKET_NAME,
    ) -> list:
        """Lists all objects in a bucket."""
        s3_client = Storage.__get_s3_client()

        try:
            response = s3_client.list_objects_v2(Bucket=bucket)
            if "Contents" in response:
                return [obj["Key"] for obj in response["Contents"]]
            else:
                return []
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def upload_to_s3(
        object_data: Union[str, bytes],
        bucket: str = settings.storage.STORAGE_BUCKET_NAME,
        file_path: str = settings.storage.STORAGE_DEFAULT_FILE_PATH,
    ) -> dict:
        """Uploads an object to Amazon S3."""
        s3_client = Storage.__get_s3_client()

        # Convert object data to bytes if it's a string
        if isinstance(object_data, str):
            object_data = object_data.encode()

        try:
            response = s3_client.put_object(
                Bucket=bucket, Key=file_path, Body=object_data
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def download_from_s3(bucket: str, file_path: str) -> Union[bytes, dict]:
        """Downloads an object from Amazon S3."""
        s3_client = Storage.__get_s3_client()

        try:
            response = s3_client.get_object(Bucket=bucket, Key=file_path)
            return response["Body"].read()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_from_s3(bucket: str, file_path: str) -> dict:
        """Deletes an object from Amazon S3."""
        s3_client = Storage.__get_s3_client()

        try:
            response = s3_client.delete_object(Bucket=bucket, Key=file_path)
            return response
        except Exception as e:
            return {"error": str(e)}
