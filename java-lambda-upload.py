import boto3
import json

def main():
    access_key_id = '**'
    secret_access_key = '**'
    region = '**'
    s3_bucket_name = '**'
    s3_object_name = '**'
    lambda_function_name = '**'
    
    jar_path = '**'
    lambda_payload = {
        'key1': 'val1'
    }

    s3 = boto3.resource('s3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    s3.Object(s3_bucket_name, s3_object_name).upload_file(jar_path)
    print("JAR '" + s3_object_name + "' successfully uploaded to S3:/" + s3_bucket_name)

    lambda_client = boto3.client('lambda',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region
    )
    lambda_update_response = lambda_client.update_function_code(
        FunctionName=lambda_function_name,
        S3Bucket=s3_bucket_name,
        S3Key=s3_object_name,

    )
    print("Lambda update response:")
    print(json.dumps(lambda_update_response, indent=4))

    print("Invoking '" + lambda_function_name + "'...")
    lambda_invoke_response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        Payload=json.dumps(lambda_payload)
    )
    print("Lamdba invoke response:")
    print(lambda_invoke_response["Payload"].read())


if __name__ == "__main__": main()