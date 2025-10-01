"""
Load — Upload final CSV to Amazon S3 (boto3)

Inputs:
    - Local file: project_Kayak/create_final_csv/hotels_weather_final.csv
    - Environment: AWS_KEY, AWS_SECRET_KEY (via .env)

Output:
    - S3 object: s3://flodussartprojectkayak/projectKayack/src/final_ter.csv

Notes:
    - Overwrites the object if the key already exists.
    - Re
"""
import os
from dotenv import load_dotenv
import boto3

print("Current working directory:", os.getcwd())
print("Listing current directory:", os.listdir())
load_dotenv()

session = boto3.Session(aws_access_key_id=os.environ["AWS_KEY"], 
                        aws_secret_access_key=os.environ["AWS_SECRET_KEY"])

s3 = session.resource("s3")

bucket = s3.Bucket("flodussartprojectkayak")

file_name = "../../Transform/data/hotels_weather_final.csv"

bucket.upload_file(file_name, "projectKayack/src/final_ter.csv")