provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "workout_mobile_app" {
  bucket = "workout-mobile-app"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "Workout Mobile App Bucket"
    Environment = "Development"
  }
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket                  = aws_s3_bucket.workout_mobile_app.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "public_read_policy" {
  bucket = aws_s3_bucket.workout_mobile_app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.workout_mobile_app.arn}/*"
      }
    ]
  })
}