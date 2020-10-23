# 复印无效
# 公示专用

from PIL import Image, ImageDraw, ImageFont


def add_num(img):
    draw = ImageDraw.Draw(img)
    myfont = ImageFont.truetype('./resource/fonts/Alibaba-PuHuiTi-Bold.ttf', size=200)
    fillcolor = "#D3D3D3"
    width, height, = img.size
    start_width = 0
    start_height = 0
    while True:
        draw.text((start_width, start_width), '复印无效    公示专用', font=myfont, fill=fillcolor)
        if start_width > width and start_height > height:
            break
        start_width += 400
        start_height += 400
    img.save('result.jpg', 'jpeg')

    return 0


def transparent(im):
    image = im.convert("RGBA")
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    font = ImageFont.truetype('./resource/fonts/Alibaba-PuHuiTi-Bold.ttf', size=200)
    d = ImageDraw.Draw(txt)
    d.text((0, 0), "复印无效    公示专用", fill=(0, 0, 0, 15), font=font)
    d.text((400, 200), "复印无效    公示专用", fill=(0, 0, 0, 15), font=font)
    d.text((1700, 600), "复印无效    公示专用", fill=(0, 0, 0, 15), font=font)
    d.text((800, 1700), "复印无效    公示专用", fill=(0, 0, 0, 15), font=font)
    combined = Image.alpha_composite(image, txt)

    combined.save("result.png")
    combined.show()


if __name__ == '__main__':
    image = Image.open('resource/demo.jpg')
    transparent(image)


def add_image(im, mark):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (im.size[0] - 150, im.size[1] - 150))
    out = Image.composite(layer, im, layer)
    out.save('result.jpg', 'jpeg')
    out.show()


def copyright_apply(input_image_path,
                    output_image_path,
                    text):
    photo = Image.open(input_image_path)

    # Store image width and height
    w, h = photo.size

    # make the image editable
    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype("RobotoBlack.ttf", 68)

    # get text width and height
    text = "© " + text + "   "
    text_w, text_h = drawing.textsize(text, font)

    pos = w - text_w, (h - text_h) - 50

    c_text = Image.new('RGB', (text_w, (text_h)), color='#000000')
    drawing = ImageDraw.Draw(c_text)

    drawing.text((0, 0), text, fill="#ffffff", font=font)
    c_text.putalpha(100)

    photo.paste(c_text, pos, c_text)
    photo.save(output_image_path)
