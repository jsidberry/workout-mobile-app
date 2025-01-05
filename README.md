# workout-mobile-app

For development qork the source videos should be stored in `static/videos/` directory.

This is for development only. When ready for Stage and Prod, we will use a CDN intermediary and remote storage for source videos. 

## Roadmap for an AWS S3 deployment scenario
To achieve the goal of hosting videos in an AWS S3 bucket and making them accessible on a cellphone via a browser or app, served efficiently through AWS CloudFront, here’s a step-by-step plan:

### Store Videos in an S3 Bucket

Steps:
	1.	Create an S3 Bucket:
	•	Name your bucket (e.g., my-video-bucket).
	•	Enable public access only if required for demo purposes; otherwise, use signed URLs or OAI (Origin Access Identity) for secure access.
	2.	Upload Videos:
	•	Upload .mp4 videos to the bucket.
	•	Set appropriate permissions.
	3.	Enable Static Hosting (Optional):
	•	Configure the bucket to serve static content if you want direct access via URLs (not recommended for secure content).

### Set Up AWS CloudFront

Why CloudFront?
	•	CloudFront acts as a CDN to cache and distribute content globally, ensuring low-latency access.
	•	It integrates seamlessly with S3.

Steps:
	1.	Create a CloudFront Distribution:
	•	Origin: Select your S3 bucket as the origin.
	•	Cache Settings: Optimize for video streaming.
	•	Viewer Protocol Policy: Enforce HTTPS for secure content delivery.
	•	Add OAI (Origin Access Identity): Restrict bucket access to CloudFront.
	2.	Configure Behavior:
	•	Set allowed HTTP methods (GET, HEAD).
	•	Enable caching policies for efficient delivery.
	•	Use signed URLs for secure access to private content.
	3.	Obtain Distribution Domain:
	•	CloudFront provides a domain (e.g., d1234abcd.cloudfront.net) for accessing your content.

### Develop the App or Browser Interface

Options:
	1.	Web App (HTML + JavaScript):
	•	Use HTML5 <video> for video playback.
	•	JavaScript can dynamically load video sources (useful for signed URLs or playlists).
	2.	Mobile App:
	•	React Native / Flutter: Build a cross-platform app.
	•	Use SDKs (like AWS Amplify) to fetch videos from S3 securely.

Example Code for Browser:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Streaming</title>
</head>
<body>
    <h1>Video Player</h1>
    <video id="video_player" controls width="100%" height="auto">
        <source src="https://d1234abcd.cloudfront.net/my-video.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</body>
</html>
```

### Secure Content Delivery

Options:
	1.	Signed URLs:
	•	Generate short-lived URLs to allow secure access.
	•	Python Example:
```python
import boto3
from botocore.signers import CloudFrontSigner
import rsa
import datetime

def rsa_signer(message):
    with open('private_key.pem', 'rb') as key_file:
        private_key = rsa.PrivateKey.load_pkcs1(key_file.read())
    return rsa.sign(message, private_key, 'SHA-1')

cloudfront_signer = CloudFrontSigner('YOUR_PUBLIC_KEY_ID', rsa_signer)

url = cloudfront_signer.generate_presigned_url(
    url='https://d1234abcd.cloudfront.net/my-video.mp4',
    date_less_than=datetime.datetime.now() + datetime.timedelta(hours=1)
)

print("Signed URL:", url)
```
    2.	Bucket Policies:
	•	Restrict access to CloudFront or specific users.
	3.	IAM Roles:
	•	Use AWS Amplify or SDKs for authenticated access.

### Optimize for Mobile

Key Considerations:
	1.	Adaptive Streaming:
	•	Use AWS Elemental MediaConvert to convert videos into HLS/DASH formats for adaptive streaming.
	2.	Responsive Design:
	•	Ensure video players adapt to screen size and orientation.
	3.	Preloading & Lazy Loading:
	•	Optimize loading times by preloading or lazy-loading videos.

### Monitor and Optimize
	1.	CloudWatch Metrics:
	•	Monitor usage and performance.
	2.	CloudFront Logs:
	•	Analyze access patterns.
	3.	Cost Optimization:
	•	Use storage classes like S3 Intelligent-Tiering for infrequently accessed videos.

This roadmap allows flexibility in development and security, ensuring smooth delivery of videos to cellphones via an app or browser.