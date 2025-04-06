import boto3

S3_client = boto3.client('s3')
print(S3_client)

response = S3_client.create_bucket(
Bucket='goal-manifestation-app-sudeep',
CreateBucketConfiguration= {'LocationConstraint':'ap-south-1'}
)

print(response)