# S3 Static Site Uploader

A simple Python CLI tool to upload static websites to AWS S3 with proper configuration for static website hosting.

## Features

- Create a new S3 bucket with static website hosting enabled
- Upload local files to the bucket
- Set proper content types for common file types
- Configure bucket policy for public read access
- Simple command-line interface

## Prerequisites

- Python 3.7+
- AWS CLI configured with appropriate credentials
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd s3-static-site-uploader
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```


### Basic Usage

```bash
python s3_uploader.py ./public --bucket your-unique-bucket-name
```

### Options

- `--bucket`, `-b`: Name of the S3 bucket (required)
- `--region`, `-r`: AWS region (default: us-east-1)
- `--create-bucket/--no-create-bucket`: Create the bucket if it doesn't exist (default: True)

### Example

1. First, create a `public` directory and add your static files (HTML, CSS, JS, etc.)
2. Run the uploader:
   ```bash
   python s3_uploader.py ./public --bucket my-awesome-website-123 --region us-west-2
   ```
3. The tool will output the website URL once complete

### IAM Permissions

The AWS user needs the following permissions:

- `s3:CreateBucket`
- `s3:PutBucketWebsite`
- `s3:PutBucketPolicy`
- `s3:PutObject`
- `s3:ListBucket`
- `s3:GetObject`

### Important Notes
- Bucket names must be globally unique across all AWS accounts
- The first time you create a bucket, you might need to wait a few minutes for DNS propagation
- For production use, consider adding CloudFront in front of your S3 bucket for better performance and HTTPS support


