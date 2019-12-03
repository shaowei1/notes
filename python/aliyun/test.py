#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Scenario:
    Custom rule template of Cloud Config allows you to quickly develop customized compliance rules.
Preparations:
    Step 1: Activate Log Service and authorize the Function Compute.
    Step 2: Activate Config (https://www.aliyun.com/product/config) and create a customer ConfigRule with this function's ARN.

"""
result = {'events': [
    {
        'eventName': 'ObjectCreated:PostObject', 'eventSource': 'acs:oss', 'eventTime': '2019-11-30T12:57:09.000Z',
        'eventVersion': '1.0',
        'oss': {
            'bucket': {'arn': 'acs:oss:cn-beijing:1376573201505901:ecpro-uploads', 'name': 'ecpro-uploads',
                       'ownerIdentity': '1376573201505901', 'virtualBucket': ''},
            'object': {'deltaSize': 5213787, 'eTag': 'EBF0126A0DC44D8B0FF6BE4C703978B2',
                       'key': 'tmp/1/e1c56c82-93d4-42d1-979b-f9405a0a5a19.zip', 'size': 5213787},
            'ossSchemaVersion': '1.0',
            'ruleId': 'ecdce3120320d668045893fc85bc467860d4d3ad',
            'xVars': {'x:account_id': '1', 'x:filename': 'shaowei.zip', 'x:upload_task_id': '11175'}
        },
        'region': 'cn-beijing',
        'requestParameters': {'sourceIPAddress': '106.38.124.243'},
        'responseElements': {'requestId': '5DE26723CE658933359A1DBD'},
        'userIdentity': {'principalId': '286847774614784161'}}]
}

import logging
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.request import CommonRequest

logger = logging.getLogger()

# Matched resource types
MATCH_RESOURCE_TYPES = '{{ resourceTypes }}'

# AccessKey/SecretKey, need AliyunConfigFullAccess policy
AK = '{{ ak }}'
SK = '{{ sk }}'

# Valid compliace type
COMPLIACE_TYPE_COMPLIANT = 'COMPLIANT'
COMPLIACE_TYPE_NON_COMPLIANT = 'NON_COMPLIANT'
COMPLIACE_TYPE_NOT_APPLICABLE = 'NOT_APPLICABLE'
COMPLIACE_TYPE_INSUFFICIENT_DATA = 'INSUFFICIENT_DATA'


def response(body, content):
    rep = {
        "isBase64Encoded": "false",
        "statusCode": "200",
        "headers": {
            "x-custom-header": "no"
        },
        "body": {
            "request_callback": body,
            "result": dict(content)
            # "result": {}
        }
    }
    return rep


def handler(event, context):
    """
    FC handler
    :param event: Event
    :param context: Context
    :return: Result
    """
    # Validate event
    evt = validate_event(event)
    if not evt:
        return None

    rule_parameters = evt.get('ruleParameters')
    result_token = evt.get('resultToken')
    invoking_event = evt.get('invokingEvent')

    # Initilize
    compliance_type = COMPLIACE_TYPE_NOT_APPLICABLE
    annotation = None

    # Get configuration item
    configuration_item = invoking_event.get('configurationItem')
    if not configuration_item:
        logger.error('Configuration item is empty.')
        return None

    ordering_timestamp = configuration_item.get('captureTime')
    resource_id = configuration_item.get('resourceId')
    resource_type = configuration_item.get('resourceType')

    # Get compliace result
    compliance_type, annotation = evaluate_configuration_item(
        rule_parameters, configuration_item)

    # Compliance result
    evaluations = [
        {
            'complianceResourceId': resource_id,
            'complianceResourceType': resource_type,
            'orderingTimestamp': ordering_timestamp,
            'complianceType': compliance_type,
            'annotation': annotation
        }
    ]

    # Put evaluation result by invoking open api
    put_evaluations(context, result_token, evaluations)

    return evaluations


def evaluate_configuration_item(rule_parameters, configuration_item):
    """
    评估逻辑
    :param rule_parameters: 规则参数
    :param configuration_item: 配置项
    :return: 评估类型，注解
    """
    # Initilize
    compliance_type = COMPLIACE_TYPE_NOT_APPLICABLE
    annotation = None

    # Get resource type and configuration
    resource_type = configuration_item['resourceType']
    full_configuration = configuration_item['configuration']

    # Check resource type
    if MATCH_RESOURCE_TYPES and resource_type not in MATCH_RESOURCE_TYPES.split(','):
        annotation = 'Resource type is {}, not in {}.'.format(
            resource_type, MATCH_RESOURCE_TYPES)
        return compliance_type, annotation

    # Check configuration
    if not full_configuration:
        annotation = 'Configuration is empty.'
        return compliance_type, annotation

    # Parse to json object
    configuration = parse_json(full_configuration)
    if not configuration:
        annotation = 'Configuration:{} in invald.'.format(full_configuration)
        return compliance_type, annotation

    # =========== Customer code start =========== #

    # =========== Customer code end =========== #

    return compliance_type, annotation


def validate_event(event):
    """
    Validate event
    :param event: Event
    :return: Event json object
    """
    if not event:
        logger.error('Event is empty.')

    evt = parse_json(event)
    logger.info('Loading event: %s .' % evt)

    if 'resultToken' not in evt:
        logger.error('ResultToken is empty.')
        return None

    if 'ruleParameters' not in evt:
        logger.error('RuleParameters is empty.')
        return None

    if 'invokingEvent' not in evt:
        logger.error('InvokingEvent is empty.')
        return None

    return evt


def parse_json(content):
    """
    Parse string to json object
    :param content: json string content
    :return: Json object
    """
    try:
        return json.loads(content)
    except Exception as e:
        logger.error('Parse content:{} to json error:{}.'.format(content, e))
        return None


def put_evaluations(context, result_token, evaluations):
    """
    Put evaluation result by invoking open api
    :param context: Context
    :param result_token: Invoke token
    :param evaluations: Evaluation result
    :return: None
    """
    # ak/sk, need AliyunConfigFullAccess policy
    client = AcsClient(AK, SK, 'cn-shanghai', )

    # Open api request
    request = CommonRequest()
    request.set_domain('config.cn-shanghai.aliyuncs.com')
    request.set_version('2018-12-24')
    request.set_action_name('PutEvaluations')
    request.add_body_params('ResultToken', result_token)
    request.add_body_params('Evaluations', evaluations)
    request.set_method('POST')

    try:
        response = client.do_action_with_exception(request)
        logger.info('PutEvaluations with request: {}, response: {}.'.format(request, response))
    except Exception as e:
        logger.error('PutEvaluations error: %s' % e)
