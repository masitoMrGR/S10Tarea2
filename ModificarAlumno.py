import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression='SET alumno_datos = :datos',
            ConditionExpression='attribute_exists(alumno_id)',
            ExpressionAttributeValues={
                ':datos': alumno_datos
            },
            ReturnValues='ALL_NEW'
        )
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'mensaje': 'Alumno no encontrado'
        }
    # Salida (json)
    return {
        'statusCode': 200,
        'alumno': response['Attributes']
    }
