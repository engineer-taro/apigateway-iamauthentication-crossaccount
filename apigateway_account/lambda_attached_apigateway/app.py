import json


def lambda_handler(event, context):
    print('excute')
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello from Lambda!'}),
        'headers': {},
    }
