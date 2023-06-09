
import os
import boto3
import logging
import traceback


logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def get_ssm_parameter(parameter_name):
    log = logging.getLogger('ssm')
    value = ''
    response = None
    try:
        ssm_client = boto3.client('ssm', region_name='us-east-1')
        log.info(ssm_client)

        response = ssm_client.get_parameter(
            Name=parameter_name, WithDecryption=True)

        value = response['Parameter']['Value']
    except Exception as e:
        log.error('Failed to retrieve parameter {}. Result was {}. Exception was {}'.format(
            parameter_name, response, e))
        log.error(traceback.format_exc())
        value = os.getenv(parameter_name, value)
    return value
