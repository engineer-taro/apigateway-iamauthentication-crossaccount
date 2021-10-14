import requests
import os
import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth


REGION_NAME = 'ap-northeast-1'
api_string = os.environ['API_STRING']
api_path = os.environ['API_PATH']


def lambda_handler(event, context):
    aws_host = f'{api_string}.execute-api.{REGION_NAME}.amazonaws.com'  # noqa: E501
    url = f'https://{aws_host}/{api_path}'

    credentials = get_credentials()
    auth = AWSRequestsAuth(
        aws_access_key=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_host=aws_host,
        aws_region=REGION_NAME,
        aws_service='execute-api'
    )
    headers = {'x-amz-security-token': credentials['SessionToken']}

    response = requests.post(
        url, json={"foo": "bar"}, auth=auth, headers=headers)

    response_body = response.json()
    print(response_body)

    return {
        'statusCode': response.status_code,
        'body': response_body.get('message')
    }


def get_credentials():
    client = boto3.client('sts')
    IAM_ROLE_ARN = os.environ['IAM_ROLE_ARN']
    IAM_ROLE_SESSION_NAME = 'other_account_session'
    response = client.assume_role(
        RoleArn=IAM_ROLE_ARN,
        RoleSessionName=IAM_ROLE_SESSION_NAME
    )
    return response['Credentials']
