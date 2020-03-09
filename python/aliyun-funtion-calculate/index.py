# pip install interruptingcow==0.8
# pip install gevent==1.4.0
import logging

import requests

import gevent
from wand.image import Image
import os
from io import BytesIO
from interruptingcow import timeout
import oss2
import zipfile
import uuid
from oss2.exceptions import NoSuchKey
from image_exif import ExifData
from base import validate_event
from gevent import monkey
from exceptions import ValidationError

# 打补丁： 让gevent使用网络请求的耗时操作，让协程自动切换执行对应的下载任务
monkey.patch_all()

UPLOAD_IMAGE_SUPPORTED_EXTENSIONS = list(
    os.getenv('UPLOAD_SUPPORTED_EXTENSIONS', 'jpg,jpeg,png,JPG,JPEG,PNG').split(','))

UPLOAD_IMAGE_MAX_SIZE = int(os.getenv('UPLOAD_FILE_MAX_SIZE', 15 * 1024 * 1024))
UPLOAD_IMAGE_MIN_SIZE = int(os.getenv('UPLOAD_FILE_MAX_SIZE', 10 * 1024))
UPLOAD_IMAGE_MAX_WIGHT = int(os.getenv('UPLOAD_IMAGE_MAX_WIGHT', 6000))
UPLOAD_IMAGE_MIN_WIGHT = int(os.getenv('UPLOAD_IMAGE_MIN_WIGHT', 100))

decompression_expire_time = int(os.getenv('DECOMPRESSION_EXPIRE_TIME', 60))

oss_bucket_name = os.getenv('OSS_BUCKET', 'ecpro-uploads')
oss_endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')

protocol_type = os.getenv('protocol_type', "http")
callback_domain = os.getenv('OSS_BUCKET', '152.136.63.157:52000')
callback_path = os.getenv('OSS_ENDPOINT', '/storage/call-back/oss-unzip')

logger = logging.getLogger()


class PictureOperate:

    def __init__(
            self,
            bucket=None,
            file_path=None,
            entity_type=None,
            extension=None,
            base_file_path=None,
            package_file=None,
    ):
        self.image_without_exif = None
        self.entity_type = entity_type
        self.file_path = file_path
        self.storage_key = None

        self.bucket = bucket

        self.fmt = None
        self.width = None
        self.height = None

        self.file_name = None
        self.extension = extension
        self.base_file_path = base_file_path

        self.file_size = None
        self.package_file = package_file
        self.storage_key_list = list()

    def get_bytes_no_exif(self, file_path):

        # os.path.getsize(file_path) 本地路径处理

        file_content = self.package_file.read(file_path)
        file_info = self.package_file.getinfo(file_path)
        self.file_size = file_info.file_size

        with Image(file=BytesIO(file_content)) as img:
            fmt = img.format
            exProcessor = ExifData()
            try:
                if int(exProcessor.check_orientation(img)) in [6, 7]:
                    img.rotate(90)
                    img.metadata['exif:Orientation'] = '1'
                if int(exProcessor.check_orientation(img)) in [6, 8]:
                    img.rotate(-90)
                    img.metadata['exif:Orientation'] = '1'
                if int(exProcessor.check_orientation(img)) in [3, 4]:
                    img.rotate(180)
                    img.metadata['exif:Orientation'] = '1'
            except (KeyError, TypeError):
                pass
            width, height = img.size
            self.fmt = fmt
            self.width = width
            self.height = height

            data = img.make_blob()
            return BytesIO(data)

    def upload_original_picture_to_cos(self, data=None, count=None, file_path=None, error_message=None):

        guid = str(uuid.uuid4()).replace("-", '')

        logging.info("get image info")
        jpeg_bin = self.get_bytes_no_exif(file_path)

        validator_result = validator_image_standard(self.width, self.height, self.file_size, self.fmt)

        if validator_result is not None:
            error_message.update({
                get_original_unzip_name(file_path, is_last=True): validator_result
            })

        if len(error_message) == 0:
            storage_key = f'{self.base_file_path}/{guid}.{self.fmt.lower()}'
            logging.info(f'storage_key: {storage_key}')

            result = self.bucket.put_object(storage_key, jpeg_bin)
            logging.info(f'upload oss result: {result.etag}')

            if count is not None:
                if result.etag is not None:
                    data.update(
                        {
                            count: {
                                "key": storage_key,
                                "width": self.width,
                                "height": self.height,
                                "format": self.fmt,
                                "file_size": self.file_size,
                            }
                        }
                    )
                    self.storage_key_list.append(storage_key)
                else:
                    data.update({count: {"request_id": result.request_id}})

            return result
        else:
            # 删除刚开始创建的图片
            for key in self.storage_key_list:
                resp = self.bucket.delete_object(key=key)
                logger.info(f"delete info, {resp.resp}")

        # print(result.etag)
        # print(result.request_id)
        # print(result.resp)

    def get_extension_name(self, filename):
        # 获取文件后缀
        extension = os.path.splitext(filename)[1]
        file_name = os.path.splitext(filename)[-2].split('/')[-1]

        if extension.startswith('.'):
            extension = extension[1:]
        extension = extension.lower()
        self.file_name = file_name
        self.extension = extension
        return file_name, extension


def get_original_unzip_name(name, is_last=False):
    try:
        if is_last:
            name = name.rsplit("/", 1)[-1]
        name = name.encode('cp437').decode('utf-8')
    except Exception as e:
        print('change_name', e)
    return name


def validator_image_standard(width, height, size, extension):
    format_ = extension in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS
    width = UPLOAD_IMAGE_MIN_WIGHT <= width <= UPLOAD_IMAGE_MAX_WIGHT
    size = UPLOAD_IMAGE_MIN_SIZE <= size <= UPLOAD_IMAGE_MAX_SIZE
    if format_ and width and size:
        return None
    return {
        "width": width,
        "height": height,
        "size": size,
        "extension": extension
    }


def get_node(tar_key, data):
    """

    :param tar_key: 稿定设计导出_354919/第二/1.jpg
    :param data: 稿定设计导出_354919/ or 稿定设计导出_354919/第二/
    :return:
    """
    for key in data.keys():
        if tar_key.endswith("/"):
            if tar_key.rsplit("/", 2)[0] + '/' == key:
                return data[key]
        else:
            if tar_key.rsplit("/", 1)[0] + '/' == key:
                return data[key]
    for value in data.values():
        if isinstance(value, dict):
            return get_node(tar_key, value)


def iter_package(package_file):
    # 遍历根目录
    root_node = {}
    pre_image_data = {}
    count = 0

    # print((file.file_size))
    # print(package_file.read(file.filename))

    for index, file in enumerate(package_file.infolist()):
        original_root = file.filename
        if '__MACOSX' in original_root:
            continue

        root = get_original_unzip_name(original_root)
        file_name = root.split("/")[-1]
        if file_name.startswith("..") or file_name.startswith("."):
            continue

        # 建立根节点目录
        if index == 0:
            root_node[root] = {}

        node = get_node(root, root_node)

        if file.is_dir():
            if index != 0:
                node.update({root: {}})
        else:
            extension = os.path.splitext(file_name)[-1].split(".")[-1]
            if extension not in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS:
                continue
            count += 1

            file_path = original_root
            print('root_node', root_node)
            print('file_name', file_name)
            print('root', root)
            node = get_node(root, root_node)
            try:
                node.update(
                    {
                        str(count): {
                            'file_path': file_path,
                            'file_name': file_name,
                        }
                    }
                )
                pre_image_data.update({count: node[str(count)]})
            except Exception:
                logging.info(f"what info {count}")

    return root_node, pre_image_data


def upload_image_to_oss(pic, root_node, pre_image_data):
    upload_image_result = dict()
    all_task = []
    error_message = {}
    for count, value in pre_image_data.items():
        file_path = value.get("file_path")
        g_task = gevent.spawn(pic.upload_original_picture_to_cos, upload_image_result, count, file_path, error_message)
        all_task.append(g_task)
    gevent.joinall(all_task)
    print('upload_image_result', upload_image_result)

    if len(error_message) > 0:
        # 用于前端显示的错误信息
        raise ValidationError(message=error_message)

    for count, value in pre_image_data.items():
        upload_status = upload_image_result.get(count)
        if upload_status is not None:
            value.update(upload_status)

            if 'file_path' in value:
                value.pop('file_path')

    print('root_node', root_node)
    return root_node


# memory profile
# if 'profile' not in dir():
#     def profile(func):
#         def inner(*args, **kwargs):
#             return func(*args, **kwargs)
#
#         return inner
#
# path = '/Users/root1/Github/ecpro-storage/snippets/unzip_test/shaowei'
#
#
# @profile

def response(body, content):
    resp = requests.post(f'{protocol_type}://{callback_domain}{callback_path}',
                         json={
                             "request_body": body,
                             "result": content
                         })
    for count in range(10):
        if resp.status_code == 200:
            break

    return resp.content


def api_gate_way_response(body, content):
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


def handler(
        event, context
):
    logging.info(f"original event: {event}")
    logging.info(f"original context: {context}")

    body = validate_event(event)
    if not body:
        return None

    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)

    logging.info('body initial', body)

    key = body.get("key")
    upload_task_id = body.get("upload_task_id")
    account_id = body.get("account_id")
    zip_name = body.get("zip_name")
    # decompression_expire_time = body.get("decompression_expire_time", 60)

    try:
        logging.info('bucket initial', key)
        pre_unzip_data = BytesIO(bucket.get_object(key).read())
        logging.info('download file')
    except NoSuchKey:
        return response(body, {"error_message": '文件获取失败'})

    base_file_path = f'intelligentArt/unzip/{account_id}/{upload_task_id}'

    try:
        with timeout(decompression_expire_time, exception=RuntimeError):
            logging.info("unzip start")
            package_file = zipfile.ZipFile(pre_unzip_data)
            logging.info("unzip end")
    except RuntimeError:
        return response(body, {"error_message": '文件解压超时错误'})
    except zipfile.BadZipFile:
        return response(body, {"error_message": '压缩包文件损坏'})

    logging.info("iter folder")
    root_node, pre_image_data = iter_package(package_file)
    pic = PictureOperate(bucket=bucket, base_file_path=base_file_path, package_file=package_file)
    try:
        data = upload_image_to_oss(pic, root_node, pre_image_data)
    except ValidationError as e:
        return response(body, {"error_message": e.message})

    package_file.close()

    logging.info("all end")
    logging.info(f"data: {data}")
    logging.info(f"body: {body}")
    resp = response(body, data)
    logging.info(f"resp: {resp}")
    return resp

# if __name__ == '__main__':
#     key = 'tmp/1/2d9cd430-43eb-4306-b7d6-1bbfe6e20605.zip'
#     zip_name = 'shaowei.zip'
#     unzip_task_func(
#         key=key,
#         upload_task_id=1,
#         account_id=1,
#         decompression_expire_time=60,
#         zip_name=zip_name
#     )
