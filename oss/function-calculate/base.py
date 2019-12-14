#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Scenario:
    Custom rule template of Cloud Config allows you to quickly develop customized compliance rules.
Preparations:
    Step 1: Activate Log Service and authorize the Function Compute.
    Step 2: Activate Config (https://www.aliyun.com/product/config) and create a customer ConfigRule with this function's ARN.

"""
import os
import traceback
import logging
import json
import sys
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

    if 'account_id' not in evt:
        logger.error('account_id is empty.')
        return None

    if 'bucket_name' not in evt:
        logger.error('bucket_name is empty.')
        return None

    if 'upload_task_id' not in evt:
        logger.error('upload_task_id is empty.')
        return None

    return evt


# def parse_json(content):
#     """
#     Parse string to json object
#     :param content: json string content
#     :return: Json object
#     """
#     try:
#
#         content = json.loads(content)
#         for index, event in enumerate(content.get("events")):
#             if index == 0:
#                 region = event.get("region")
#                 oss_info = event.get("oss")
#
#                 bucket_name = oss_info.get("name")
#                 upload_object = oss_info.get("object")
#                 upload_object_size = upload_object.get("size")
#                 upload_object_key = upload_object.get("key")
#                 customize_vars = oss_info.get("xVars")
#                 account_id = customize_vars.get("x:account_id")
#                 filename = customize_vars.get("x:filename")
#                 upload_task_id = customize_vars.get("x:upload_task_id")
#
#                 # data = {
#                 #     "key": upload_object_key,
#                 #     "upload_task_id": int(json.loads(upload_task_id)),
#                 #     "account_id": int(account_id),
#                 #     "zip_name": filename,
#                 #     "file_size": int(upload_object_size),
#                 #     "bucket_name": bucket_name,
#                 #     "region": region,
#                 #
#                 # }
#                 data = {
#                     "key": upload_object_key,
#                     "upload_task_id": int(json.loads(upload_task_id)),
#                     "account_id": int(json.loads(account_id)),
#                     "zip_name": filename,
#                     "file_size": int(upload_object_size),
#                     "bucket_name": bucket_name,
#                     "region": region,
#
#                 }
#                 return data
#     except Exception as e:
#         logging.info("*" * 50)
#         logging.error({"error_args": str(e.args),
#                        "error_info": str(sys.exc_info()[0]),
#                        "error_point": str(traceback.format_exc())
#                        })
#         logger.error('Parse content:{}'.format(content))
#         return None
def parse_json(content):
    """
    Parse string to json object
    :param content: json string content
    {'events': [{'eventName': 'ObjectCreated:PostObject', 'eventSource': 'acs:oss', 'eventTime': '2019-12-05T14:03:04.000Z', 'eventVersion': '1.0',
                 'oss': {'bucket': {'arn': 'acs:oss:cn-beijing:1376573201505901:ecpro-uploads', 'name': 'ecpro-uploads', 'ownerIdentity': '1376573201505901', 'virtualBucket': ''},
                         'object': {'deltaSize': 0, 'eTag': 'EBF0126A0DC44D8B0FF6BE4C703978B2', 'key': 'tmp/1/e1c56c82-93d4-42d1-979b-f9405a0a5a19.zip', 'size': 5213787}, 'ossSchemaVersion': '1.0',
                         'ruleId': 'ecdce3120320d668045893fc85bc467860d4d3ad', 'xVars': {'x:customize': '{"mold": "tmp", "document_id": 0, "parent_file_id": 0, "account_id": 10016, "filename": "shaowei.zip", "upload_task_id": 11204}'}},
                 'region': 'cn-beijing', 'requestParameters': {'sourceIPAddress': '106.38.124.243'}, 'responseElements': {'requestId': '5DE90E143243A933348E40D9'}, 'userIdentity': {'principalId': '286847774614784161'}}]}
    :return: Json object
    """

    try:

        content = json.loads(content)
        logging.info(f"input content: {content}")
        for index, event in enumerate(content.get("events")):
            if index == 0:
                region = event.get("region")
                oss_info = event.get("oss")
                bucket_name = oss_info.get("bucket").get("name")

                upload_object = oss_info.get("object")
                upload_object_size = upload_object.get("size")
                upload_object_key = upload_object.get("key")

                customize_vars = json.loads(oss_info.get("xVars").get("x:customize"))

                account_id = customize_vars.get("account_id")
                period_id = customize_vars.get("period_id")
                filename = customize_vars.get("filename")
                upload_task_id = customize_vars.get("upload_task_id")
                storage_host = customize_vars.get("STORAGE_CALLBACK_HOST")

                logging.info(f"get storage_host: {storage_host}")

                oss_func_calculate_url = f"https://{storage_host}/storage-callback/aliyun-fc-callback/"
                logging.info(f"set oss_func_calculate_url: {oss_func_calculate_url}")

                # data = {
                #     "key": upload_object_key,
                #     "upload_task_id": int(json.loads(upload_task_id)),
                #     "account_id": int(account_id),
                #     "zip_name": filename,
                #     "file_size": int(upload_object_size),
                #     "bucket_name": bucket_name,
                #     "region": region,
                #
                # }
                data = {
                    "key": upload_object_key,
                    "upload_task_id": int(upload_task_id),
                    "account_id": int(account_id),
                    "file_size": int(upload_object_size),
                    "period_id": int(period_id),
                    "zip_name": filename,
                    "bucket_name": bucket_name,
                    "region": region,  # 'region': 'cn-shanghai',
                    "oss_func_calculate_url": oss_func_calculate_url,
                }
                return data
    except Exception as e:
        logging.info("*" * 50)
        logging.error({"error_args": str(e.args),
                       "error_info": str(sys.exc_info()[0]),
                       "error_point": str(traceback.format_exc())
                       })
        logger.error('Parse content:{}'.format(content))
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
