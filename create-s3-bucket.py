import boto3
import json
from botocore.exceptions import ClientError

def create_public_s3_bucket(bucket_name, region="us-east-2"):
    # Create S3 client
    s3 = boto3.client('s3', region_name=region)

    try:
        # Create the S3 bucket
        if region == "us-east-2":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created successfully.")

        # Configure the bucket to allow public access
        # Apply a bucket policy for public access
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        # Attach the policy to the bucket
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(public_policy)
        )
        print(f"Public read access granted for bucket '{bucket_name}'.")

        # Disable Block Public Access (if enabled)
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False
            }
        )
        print(f"Public access block disabled for bucket '{bucket_name}'.")

    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True


# Usage
bucket_name = "workout-mobile-app"
region = "us-east-2"  # Use the desired AWS region
create_public_s3_bucket(bucket_name, region)