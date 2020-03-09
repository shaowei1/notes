# pip install interruptingcow==0.8
# pip install gevent==1.4.0
import base64
import logging
import gevent
import json
from wand.image import Image
import os
from io import BytesIO
from interruptingcow import timeout
import oss2
import zipfile
import uuid
from oss2.exceptions import NoSuchKey
from image_exif import ExifData
from gevent import monkey

# 打补丁： 让gevent使用网络请求的耗时操作，让协程自动切换执行对应的下载任务
monkey.patch_all()

UPLOAD_IMAGE_SUPPORTED_EXTENSIONS = list(
    os.getenv('UPLOAD_SUPPORTED_EXTENSIONS', 'jpg,jpeg,png,JPG,JPEG,PNG').split(','))

UPLOAD_IMAGE_MAX_SIZE = int(os.getenv('UPLOAD_FILE_MAX_SIZE', 15 * 1024 * 1024))
UPLOAD_IMAGE_MIN_SIZE = int(os.getenv('UPLOAD_FILE_MAX_SIZE', 10 * 1024))
UPLOAD_IMAGE_MAX_WIGHT = int(os.getenv('UPLOAD_IMAGE_MAX_WIGHT', 6000))
UPLOAD_IMAGE_MIN_WIGHT = int(os.getenv('UPLOAD_IMAGE_MIN_WIGHT', 100))

oss_bucket_name = os.getenv('OSS_BUCKET', 'ecpro-uploads')
oss_endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')

logger = logging.getLogger()


class PictureOperate:

    def __init__(self,
                 bucket=None,
                 file_path=None,
                 entity_type=None,
                 extension=None,
                 base_file_path=None
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

    def remove_rotate_info(self, image_bytes):
        if isinstance(image_bytes, str):
            self.file_size = os.path.getsize(image_bytes)
        with Image(filename=image_bytes) as img:
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
            self.image_without_exif = img
            self.fmt = fmt
            self.width = width
            self.height = height
            return width, height, fmt, self.file_size

    def get_bytes_no_exif(self, file_path):
        if isinstance(file_path, str):
            self.file_size = os.path.getsize(file_path)
        with Image(filename=file_path) as img:
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

    def upload_original_picture_to_cos(self, data=None, count=None, file_path=None):
        guid = str(uuid.uuid4()).replace("-", '')

        logging.info("get image info")
        jpeg_bin = self.get_bytes_no_exif(file_path)

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
            else:
                data.update({count: {"request_id": result.request_id}})
        return result

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


def get_original_unzip_name(name):
    try:
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


def validator_iter_files(rootDir):
    # 遍历根目录
    error_message = {}
    pic = PictureOperate()
    for root, dirs, files in os.walk(rootDir):
        if '__MACOSX' in root:
            continue
        print(root, dirs, files)

        for file_name in files:
            if file_name.startswith('.'):
                continue
            extension = os.path.splitext(file_name)[-1].split(".")[-1]
            if extension not in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS:
                continue
            print('extension', extension)
            file_path = os.path.join(root, file_name)
            print('file_name', file_name)
            chinese_file_name = file_name.encode('cp437').decode('utf-8')
            print('chinese_file_name', chinese_file_name)
            width, height, fmt, file_size = pic.remove_rotate_info(file_path)

            validator_result = validator_image_standard(width, height, file_size, extension)

            if validator_result is not None:
                error_message.update({
                    file_name: validator_result
                })
    if error_message:
        return error_message


def get_node(tar_key, data):
    tar_key = tar_key.rsplit("/", 1)[-1]
    tar_key = get_original_unzip_name(tar_key)
    for key in data.keys():
        if tar_key == key:
            return data[key]
    for value in data.values():
        if isinstance(value, dict):
            return get_node(tar_key, value)


def iter_files(rootDir):
    # 遍历根目录
    data = {}
    pic = PictureOperate()
    for root, dirs, files in os.walk(rootDir):
        if '__MACOSX' in root:
            continue
        print(root, dirs, files)
        root_name = root.split('/')[-1]
        data[root_name] = {}

        for file_name in files:
            if file_name.startswith('.'):
                continue
            extension = os.path.splitext(file_name)[-1].split(".")[-1]
            if extension not in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS:
                continue
            file_path = os.path.join(root, file_name)
            print('file_name', file_name.encode('cp437').decode('utf-8'))
            chinese_file_name = file_name.encode('cp437').decode('utf-8')
            data[root_name].update({chinese_file_name: chinese_file_name})
    return data


# 遍历文件夹
def only_iter_files(rootDir):
    # 遍历根目录
    root_node = {}
    pre_image_data = {}
    count = 0
    for index, (root, dirs, files) in enumerate(os.walk(rootDir)):
        if '__MACOSX' in root:
            continue
        original_root = root
        print(root, dirs, files)

        root = root.split('/')[-1]

        node = get_node(root, root_node)
        if node is None:
            root_node[root] = {}
            node = get_node(root, root_node)

        for dir_name in dirs:
            if '__MACOSX' in dir_name:
                continue
            node.update({get_original_unzip_name(dir_name): {}})

        for file_name in files:
            if file_name.startswith('.'):
                continue
            extension = os.path.splitext(file_name)[-1].split(".")[-1]
            if extension not in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS:
                continue
            count += 1
            file_path = os.path.join(original_root, file_name)

            print('root_node', root_node)
            print('file_name', file_name)
            print('root', root)
            node = get_node(root, root_node)
            node.update(
                {
                    str(count): {
                        'file_path': file_path,
                        'file_name': get_original_unzip_name(file_name),
                    }
                }
            )
            pre_image_data.update({count: node[str(count)]})

    return root_node, pre_image_data


def upload_image_to_oss(pic, root_node, pre_image_data):
    upload_image_result = dict()
    all_task = []
    for count, value in pre_image_data.items():
        file_path = value.get("file_path")
        g_task = gevent.spawn(pic.upload_original_picture_to_cos, upload_image_result, count, file_path)
        all_task.append(g_task)
    gevent.joinall(all_task)
    print('upload_image_result', upload_image_result)

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
    event = json.loads(event)
    content = {
        'path': event['path'],
        'method': event['httpMethod'],
        'headers': event['headers'],
        'queryParameters': event['queryParameters'],
        'pathParameters': event['pathParameters'],
        'body': event['body']
    }

    creds = context.credentials
    # auth = oss2.StsAuth(creds.accessKeyId, creds.accessKeySecret, creds.securityToken)
    # auth = oss2.Auth(creds.accessKeyId, creds.accessKeySecret)
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)
    body = json.loads(base64.b64decode(content.get("body")))

    logging.info('body initial', body)

    key = body.get("key")
    upload_task_id = body.get("upload_task_id")
    account_id = body.get("account_id")
    zip_name = body.get("zip_name")
    decompression_expire_time = body.get("decompression_expire_time", 60)

    if zip_name.endswith(".zip"):
        zip_name = zip_name.rsplit(".", 1)[-2]

    # tmpdir = f'/tmp/{key}.zip'
    tmpdir = f'/tmp/{zip_name}.zip'

    os.system("rm -rf /tmp/*")
    target_path = f'/tmp/{zip_name}'
    try:
        logging.info('bucket initial', key)
        resp = bucket.get_object_to_file(key, tmpdir)
        logging.info('download file')
    except NoSuchKey:
        return response(body, {"error_message": '文件获取失败'})

    base_file_path = f'intelligentArt/unzip/{account_id}/{upload_task_id}'

    try:
        with timeout(decompression_expire_time, exception=RuntimeError):
            logging.info("unzip start")
            package_file = zipfile.ZipFile(tmpdir)
            package_file.extractall(target_path)
            os.system(f'rm -rf {tmpdir}')
            logging.info("unzip end")
    except RuntimeError:
        return response(body, {"error_message": '文件解压超时错误'})

    validator_result = validator_iter_files(target_path)
    logging.info("validator end")
    if validator_result is not None:
        return response(body, {"error_message": validator_result})

    logging.info("iter folder")
    root_node, pre_image_data = only_iter_files(target_path)
    pic = PictureOperate(bucket=bucket, base_file_path=base_file_path)
    data = upload_image_to_oss(pic, root_node, pre_image_data)
    logging.info("all end")
    logging.info(data)

    logging.info(body)
    xx = response(body, data)
    logging.info(json.dumps(xx))
    return xx

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
