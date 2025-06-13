import boto3
import click
import os
from pathlib import Path

class S3Uploader:
    def __init__(self, bucket_name, region='us-east-1'):
        """Initialize the S3 uploader with bucket name and region."""
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
        self.region = region

    def create_bucket(self):
        """Create an S3 bucket with static website hosting enabled."""
        try:
            # Create bucket
            if self.region == 'us-east-1':
                self.s3.create_bucket(Bucket=self.bucket_name)
            else:
                location = {'LocationConstraint': self.region}
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration=location
                )
            
            # Enable static website hosting
            website_config = {
                'ErrorDocument': {'Key': 'error.html'},
                'IndexDocument': {'Suffix': 'index.html'}
            }
            self.s3.put_bucket_website(
                Bucket=self.bucket_name,
                WebsiteConfiguration=website_config
            )
            
            # Set bucket policy for public access
            bucket_policy = {
                'Version': '2012-10-17',
                'Statement': [{
                    'Sid': 'PublicReadGetObject',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': f'arn:aws:s3:::{self.bucket_name}/*'
                }]
            }
            
            self.s3.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            
            print(f" Bucket '{self.bucket_name}' created and configured for static website hosting.")
            return True
            
        except Exception as e:
            print(f" Error creating bucket: {str(e)}")
            return False

    def upload_directory(self, path):
        """Upload a directory to the S3 bucket."""
        try:
            path = Path(path).resolve()
            
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = Path(root) / file
                    s3_path = str(file_path.relative_to(path))
                    
                    # Set content type based on file extension
                    content_type = 'text/html' if file.endswith('.html') else 'text/plain'
                    
                    # Upload file
                    self.s3.upload_file(
                        str(file_path),
                        self.bucket_name,
                        s3_path,
                        ExtraArgs={
                            'ContentType': content_type,
                            'ACL': 'public-read'
                        }
                    )
                    print(f"Uploaded: {s3_path}")
            
            website_url = f"http://{self.bucket_name}.s3-website-{self.region}.amazonaws.com"
            print(f"\n Website URL: {website_url}")
            return True
            
        except Exception as e:
            print(f" Error uploading files: {str(e)}")
            return False

@click.command()
@click.argument('local_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--bucket', '-b', required=True, help='Name for the S3 bucket')
@click.option('--region', '-r', default='us-east-1', help='AWS region (default: us-east-1)')
@click.option('--create-bucket/--no-create-bucket', default=True, help='Create the bucket if it does not exist')
def main(local_dir, bucket, region, create_bucket):
    """Upload a local directory to an S3 bucket configured for static website hosting."""
    uploader = S3Uploader(bucket, region)
    
    try:
        if create_bucket:
            print(f" Creating bucket '{bucket}' in region '{region}'...")
            uploader.create_bucket()
        
        print(f"\n Uploading files from '{local_dir}' to bucket '{bucket}'...")
        uploader.upload_directory(local_dir)
        
    except Exception as e:
        print(f" An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    import json  # Moved here to be available for the entire module
    main()
