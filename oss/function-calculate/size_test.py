from io import BytesIO

with open('/Users/root1/Downloads/大于6000px的图片/宽度 9000.jpg', 'rb') as f:
    data = f.read()

    length = len(data)
    bytesIO_data = BytesIO(data)



# try:
#     width, height = get_image_size.get_image_metadata_from_bytesio()
#     print(width, height)
# except get_image_size.UnknownImageFormat:
#     width, height = -1, -1
