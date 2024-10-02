import json
import boto3
from typing import List
from datetime import datetime

s3_client = boto3.client("s3")
batch_client = boto3.client("batch")

input_bucket_name = "noaa-gfs-bdp-pds"
output_bucket_name = "outputbucket-604815197344-test"
job_queue = "BatchJobQueue"
job_definition = "BatchEC2JobDefinition"


def filter_s3_files(bucket: str, date: str) -> List[str]:
    """Filter S3 files based on the specified path format."""
    prefix = f"gfs.{date}/06/atmos/gfs.t06z.pgrb2.0p25.f"
    filtered_files = []

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if "Contents" in page:
                for item in page["Contents"]:
                    if not (x := item["Key"]).endswith(".idx"):
                        i_ = int(x[-3:])
                        if i_ % 3 == 0:
                            filtered_files.append(item["Key"])

    except Exception as e:
        print(f"Error retrieving files from bucket {bucket}: {e}")

    return filtered_files


def submit_jobs(files):
    for file_key in files:
        job_name = f"Process-{file_key[-3:]}"
        response = batch_client.submit_job(
            jobName=job_name,
            jobQueue=job_queue,
            jobDefinition=job_definition,
            containerOverrides={
                "environment": [
                    {
                        "name": "INPUT_FILE",
                        "value": f"s3://{input_bucket_name}/{file_key}",
                    },
                    {
                        "name": "OUTPUT_BUCKET",
                        "value": output_bucket_name,
                    },
                ]
            },
        )
        print(f'Submitted job: {response["jobId"]} for file: {file_key}')


def lambda_handler(event, context):
    date_ = datetime.now().strftime("%Y%m%d")
    date = "20241002"
    print(f"hardcoded date: {date} vs", date_)

    files_to_process = filter_s3_files(input_bucket_name, date)
    print(f"Found {len(files_to_process)} files to process")
    files_to_process = files_to_process[:10]

    submit_jobs(files_to_process)

    return {
        "statusCode": 200,
        "body": json.dumps(
            f"Jobs submitted successfully for {len(files_to_process)} files"
        ),
    }
