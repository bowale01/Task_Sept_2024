import json
import boto3
from boto3.dynamodb.conditions 
import Key
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Table names - fetched from environment variables or hard-coded
NOTES_TABLE_NAME = os.getenv('NOTES_TABLE_NAME', 'user-notes')
AUTH_TABLE_NAME = os.getenv('AUTH_TABLE_NAME', 'token-email-lookup')

# Max number of notes to return
MAX_NOTES = 10

def lambda_handler(event, context):
    # Get Authorization header
    auth_header = event['headers'].get('Authorization', '')
    
    # Check if Authorization header is valid
    if not auth_header.startswith('Bearer '):
        return response(400, {'message': 'Malformed or missing authentication header'})

    # Extract the token from the header
    token = auth_header.split(' ')[1]

    # If token is empty, return 403
    if not token:
        return response(403, {'message': 'Invalid token'})

    # Fetch the email associated with the token from the 'token-email-lookup' table
    email = get_email_from_token(token)
    
    # If token is invalid (i.e., no email found), return 403
    if not email:
        return response(403, {'message': 'Invalid token'})

    # Query the 'user-notes' table to get the notes of the authenticated user
    notes = get_user_notes(email)
    
    # Return the notes in a successful response
    return response(200, {'notes': notes})


def get_email_from_token(token):
    """
    Query DynamoDB to get the email associated with the provided token.
    Returns the email if token is valid, otherwise None.
    """
    auth_table = dynamodb.Table(AUTH_TABLE_NAME)
    
    try:
        # Query DynamoDB with token as the partition key
        result = auth_table.get_item(Key={'token': token})
        return result['Item']['email'] if 'Item' in result else None
    except Exception as e:
        print(f"Error fetching email for token {token}: {str(e)}")
        return None


def get_user_notes(email):
    """
    Query DynamoDB for notes belonging to the given email.
    Returns the notes sorted by 'create_date' in descending order, limited to MAX_NOTES.
    """
    notes_table = dynamodb.Table(NOTES_TABLE_NAME)
    
    try:
        # Query the table using the email as the partition key and limit to MAX_NOTES
        result = notes_table.query(
            KeyConditionExpression=Key('user').eq(email),
            ScanIndexForward=False,  # This will sort by create_date in descending order
            Limit=MAX_NOTES
        )
        # Return the list of notes
        return result.get('Items', [])
    except Exception as e:
        print(f"Error fetching notes for user {email}: {str(e)}")
        return []


def response(status_code, body):
    """
    Helper function to create a response compatible with API Gateway's expected format.
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
