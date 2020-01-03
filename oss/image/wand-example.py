# brew install freetype imagemagick

from wand.image import Image


def my_handler(event, context):
    # 旋转180度
    with Image(blob=event) as img:
        print(img.size)
        with img.clone() as i:
            i.rotate(180)
            return i.make_blob()


with open('1.png', 'rb') as f:
    x = my_handler(f.read(), None)
    with open('test.png', 'wb') as result:
        result.write(x)
