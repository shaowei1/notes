from wand.image import Image


# create class for get exif data from image
class ExifData:
    key_exif = ['date:create',
                'date:modify',
                'exif:ApertureValue',
                'exif:BrightnessValue',
                'exif:ColorSpace',
                'exif:ComponentsConfiguration',
                'exif:Compression',
                'exif:DateTime',
                'exif:DateTimeDigitized',
                'exif:DateTimeOriginal',
                'exif:ExifImageLength',
                'exif:ExifImageWidth',
                'exif:ExifOffset',
                'exif:ExifVersion',
                'exif:ExposureMode',
                'exif:ExposureProgram',
                'exif:ExposureTime',
                'exif:Flash',
                'exif:FlashPixVersion',
                'exif:FNumber',
                'exif:FocalLength',
                'exif:FocalLengthIn35mmFilm',
                'exif:ISOSpeedRatings',
                'exif:JPEGInterchangeFormat',
                'exif:JPEGInterchangeFormatLength',
                'exif:Make',
                'exif:MeteringMode',
                'exif:Model',
                'exif:Orientation',
                'exif:ResolutionUnit',
                'exif:SceneCaptureType',
                'exif:SceneType',
                'exif:SensingMethod',
                'exif:ShutterSpeedValue',
                'exif:Software',
                'exif:SubjectArea',
                'exif:SubSecTimeDigitized',
                'exif:SubSecTimeOriginal',
                'exif:WhiteBalance',
                'exif:XResolution',
                'exif:YCbCrPositioning',
                'exif:YResolution',
                'jpeg:colorspace',
                'jpeg:sampling-factor']

    exif_orientation_column = [{"top": [6, 5]}, {"bottom": [7, 8]}, {"left": [1, 4]}, {"right": [2, 3]}]
    exif_orientation_row = [{"top": [1, 3]}, {"bottom": [3, 4]}, {"left": [5, 8]}, {"right": [6, 7]}]

    exif_data = {}

    def __init__(self):
        return None

    def get_exif_data(self, img_path):
        # read image
        img = Image(filename=img_path)
        img_exif = img.metadata
        for key in self.key_exif:
            self.exif_data[key] = img_exif[key]

        return self.exif_data

    def check_orientation(self, img):
        exif = img.metadata
        # print exif['exif:Orientation']
        return exif['exif:Orientation']


class ImageResizer:
    # predefine image size
    # square size
    square_150x150 = '150x150^'
    square_320x320 = '320x320^'
    square_500x500 = '500x500^'
    square_640x640 = '640x640^'

    square_150x150_size = [150, 150]
    square_320x320_size = [320, 320]
    square_500x500_size = [500, 500]
    square_640x640_size = [640, 640]

    square_150x150_name = 'square_150x150'
    square_320x320_name = 'square_320x320'
    square_500x500_name = 'square_500x500'
    square_640x640_name = 'square_640x640'

    # non_square_size
    small_240x180 = '240x180^'
    small_320x240 = '320x240^'
    medium_640x480 = '640x480^'
    medium_800x600 = '800x600^'
    large_1024x768 = '1024x768^'
    large_1600x1200 = '1600x1200^'

    small_240x180_size = [240, 180]
    small_320x240_size = [320, 240]
    medium_640x480_size = [640, 480]
    medium_800x600_size = [800, 600]
    large_1024x768_size = [1024, 768]
    large_1600x1200_size = [1600, 1200]

    small_240x180_name = 'small_240x180'
    small_320x240_name = 'small_320x240'
    medium_640x480_name = 'medium_640x480'
    medium_800x600_name = 'medium_800x600'
    large_1024x768_name = 'large_1024x768'
    large_1600x1200_name = 'large_1600x1200'

    def __init__(self):
        return None

    def generate_square_img(self, img_path, size_config, size_img, size_name, dest_path):
        # open_image
        img = Image(filename=img_path)
        # transform with resize scale config
        img.transform(resize=size_config)
        # try to crop, calculate width crop first
        target_size = size_img[1]  # use one because its square
        width, height = img.size
        # print "width, height ", width, height
        crop_start, crop_end = [0, 0]  # add new size params
        # calculate
        crop_start = (width - target_size) / 2
        crop_end = crop_start + target_size

        # print crop_start, crop_end, target_size, (crop_end - crop_start)
        '''
        exProcessor = ExifData()
        #rotate image if necessary
        if exProcessor.check_orientation(img) in [6, 7]:
            img.rotate(90)
            img.metadata['exif:Orientation'] = 1
        if exProcessor.check_orientation(img) in [6, 8]:
            img.rotate(-90)
            img.metadata['exif:Orientation'] = 1
        if exProcessor.check_orientation(img) in [3, 4]:
            img.rotate(180) 
            img.metadata['exif:Orientation'] = 1
        '''

        # do cropping
        with img[crop_start:crop_end, :] as square_image:
            # save
            square_image.save(filename=''.join([dest_path, size_name, '.jpg']))

    def resize_image(self, img_path, size_config, size_name, dest_path):
        # open image
        img = Image(filename=img_path)
        # transform using resize config
        img.transform(resize=size_config)
        '''
        exProcessor = ExifData()
        #rotate image if necessary
        if exProcessor.check_orientation(img) in [6, 7]:
            img.rotate(90)
            img.metadata['exif:Orientation'] = 1
        if exProcessor.check_orientation(img) in [6, 8]:
            img.rotate(-90)
            img.metadata['exif:Orientation'] = 1
        if exProcessor.check_orientation(img) in [3, 4]:
            img.rotate(180) 
            img.metadata['exif:Orientation'] = 1
        '''
        # save img
        img.save(filename=''.join([dest_path, size_name, '.jpg']))

    def generate_all_image(self, image_path, dest_path):
        # generate square image
        self.generate_square_img(image_path, self.square_150x150, self.square_150x150_size, self.square_150x150_name,
                                 dest_path)
        self.generate_square_img(image_path, self.square_320x320, self.square_320x320_size, self.square_320x320_name,
                                 dest_path)
        self.generate_square_img(image_path, self.square_500x500, self.square_500x500_size, self.square_500x500_name,
                                 dest_path)
        self.generate_square_img(image_path, self.square_640x640, self.square_640x640_size, self.square_640x640_name,
                                 dest_path)

        # generate non square image
        self.resize_image(image_path, self.small_240x180, self.small_240x180_name, dest_path)
        self.resize_image(image_path, self.small_320x240, self.small_320x240_name, dest_path)
        self.resize_image(image_path, self.medium_640x480, self.medium_640x480_name, dest_path)
        self.resize_image(image_path, self.medium_800x600, self.medium_800x600_name, dest_path)
        self.resize_image(image_path, self.large_1024x768, self.large_1024x768_name, dest_path)
        self.resize_image(image_path, self.large_1600x1200, self.large_1600x1200_name, dest_path)

        return None
