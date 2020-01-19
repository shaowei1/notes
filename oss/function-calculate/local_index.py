import logging
import requests
import helper
from wand.image import Image
import os
from io import BytesIO
import oss2
import uuid
from image_exif import ExifData
from base import validate_event
from exceptions import ValidationError
import imagesize

logging.getLogger("oss2.api").setLevel(logging.ERROR)
logging.getLogger("oss2.auth").setLevel(logging.ERROR)

UPLOAD_IMAGE_SUPPORTED_EXTENSIONS = list(
    os.getenv('UPLOAD_SUPPORTED_EXTENSIONS', 'jpg,jpeg,png,JPG,JPEG,PNG').split(',')
)

UPLOAD_IMAGE_MAX_SIZE = int(os.getenv('UPLOAD_IMAGE_MAX_SIZE', 15 * 1024 * 1024))
UPLOAD_IMAGE_MIN_SIZE = int(os.getenv('UPLOAD_IMAGE_MIN_SIZE', 10 * 1024))
UPLOAD_IMAGE_MAX_WIGHT = int(os.getenv('UPLOAD_IMAGE_MAX_WIGHT', 6000))
UPLOAD_IMAGE_MIN_WIGHT = int(os.getenv('UPLOAD_IMAGE_MIN_WIGHT', 100))
DEBUG = os.getenv('DEBUG', True)

decompression_expire_time = int(os.getenv('DECOMPRESSION_EXPIRE_TIME', 60))

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
        print('file_content')
        file_info = self.package_file.getinfo(file_path)
        print('file_info')
        self.file_size = file_info.file_size
        print(self.file_size)
        width, height = imagesize.get(BytesIO(file_content))
        self.width = width
        self.height = height
        self.fmt = 'JPEG'
        if self.width > UPLOAD_IMAGE_MAX_WIGHT or self.height > UPLOAD_IMAGE_MAX_WIGHT:
            return None
        if self.width * self.height * 3 > UPLOAD_IMAGE_MAX_SIZE:
            self.file_size = self.width * self.height * 3
            return None

        with Image(file=BytesIO(file_content)) as img:
            fmt = img.format
            print(fmt)
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
            self.fmt = fmt
            data = img.make_blob()
            # file_content.close()
            return BytesIO(data)

    def upload_original_picture_to_cos(self, data=None, count=None, file_path=None, error_message=None):

        guid = str(uuid.uuid4()).replace("-", '')
        print('0', file_path)
        logging.info("get image info")
        jpeg_bin = self.get_bytes_no_exif(file_path)
        print('1', file_path)
        validator_result = validator_image_standard(self.width, self.height, self.file_size, self.fmt)
        print('2', file_path)

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
    format_judge = extension in UPLOAD_IMAGE_SUPPORTED_EXTENSIONS

    width_judge = UPLOAD_IMAGE_MIN_WIGHT <= width <= UPLOAD_IMAGE_MAX_WIGHT
    height_judge = UPLOAD_IMAGE_MIN_WIGHT <= height <= UPLOAD_IMAGE_MAX_WIGHT

    size_judge = UPLOAD_IMAGE_MIN_SIZE <= size <= UPLOAD_IMAGE_MAX_SIZE

    if format_judge and width_judge and size_judge and height_judge:
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
    # 单级目录，找不到父亲的情况
    if '/' not in tar_key:
        return data.get(list(data.keys())[0])
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
            if file.is_dir() is not True:
                # 如果文件夹只有一级
                root_node[root.rsplit("/", 1)[0] + '/'] = {}
            else:
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
            print("file_path", file_path)
            print("file_name", file_name)
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
    # all_task = []
    error_message = {}
    for count, value in pre_image_data.items():
        file_path = value.get("file_path")
        pic.upload_original_picture_to_cos(upload_image_result, count, file_path, error_message)
        # g_task = gevent.spawn(pic.upload_original_picture_to_cos, upload_image_result, count, file_path, error_message)
        # all_task.append(g_task)
    # gevent.joinall(all_task)
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


def response(body, content, oss_func_calculate_url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    logging.info(f"oss_func_calculate_url: {oss_func_calculate_url}")
    resp = requests.post(
        oss_func_calculate_url,
        json={
            "request_body": body,
            "result": content
        },
        # headers=headers
    )
    for count in range(10):
        if resp.status_code == 200:
            break

    return resp.content


def handler(
        event, context
):
    logging.info(f"original event: {event}")
    logging.info(f"original context: {context}")

    body = validate_event(event)
    if not body:
        return None

    oss_bucket_name = body.get("bucket_name")
    oss_region = body.get("region")
    oss_endpoint = f'oss-{oss_region}.aliyuncs.com'
    if DEBUG is None:
        creds = context.credentials
        auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    else:
        AccessKeyID = os.getenv('AccessKeyID', None)
        AccessKeySecret = os.getenv('AccessKeySecret', None)
        auth = oss2.Auth(AccessKeyID, AccessKeySecret)
    bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)

    logging.info('body initial', body)

    key = body.get("key")
    upload_task_id = body.get("upload_task_id")
    account_id = body.get("account_id")
    zip_name = body.get("zip_name")
    oss_func_calculate_url = body.get("oss_func_calculate_url")

    # decompression_expire_time = body.get("decompression_expire_time", 60)
    object_name = key
    lst = object_name.split("/")
    zip_name = lst[-1]
    PROCESSED_DIR = os.environ.get("PROCESSED_DIR", "")
    if PROCESSED_DIR and PROCESSED_DIR[-1] != "/":
        PROCESSED_DIR += "/"
    newKey = PROCESSED_DIR + zip_name
    zip_fp = helper.OssStreamFileLikeObject(bucket, object_name)

    newKey = newKey.replace(".zip", "/")

    base_file_path = f'intelligentArt/unzip/{account_id}/{upload_task_id}'

    with helper.zipfile_support_oss.ZipFile(zip_fp) as zip_file:
        logging.info("iter folder")
        root_node, pre_image_data = iter_package(zip_file)
        pic = PictureOperate(bucket=bucket, base_file_path=base_file_path, package_file=zip_file)
        try:
            data = upload_image_to_oss(pic, root_node, pre_image_data)
        except ValidationError as e:
            return response(body, {"error_message": e.message}, oss_func_calculate_url)

    # package_file.close()

    logging.info("all end")
    logging.info(f"data: {data}")
    logging.info(f"body: {body}")
    resp = response(body, data, oss_func_calculate_url)
    logging.info(f"resp: {resp}")
    return resp