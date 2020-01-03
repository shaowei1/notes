import gevent
import urllib.request  # 网络请求模块
from gevent import monkey

# 打补丁： 让gevent使用网络请求的耗时操作，让协程自动切换执行对应的下载任务
monkey.patch_all()


# 根据图片地址下载对应的图片
def download_img(img_url, img_name):
    try:
        print(img_url)
        # 根据图片地址打开网络资源数据
        response = urllib.request.urlopen(img_url)
        # 创建文件把数据写入到指定文件里面
        with open(img_name, "wb") as img_file:
            while True:
                # 读取网络图片数据
                img_data = response.read(1024)
                if img_data:
                    # 把数据写入到指定文件里面
                    img_file.write(img_data)
                else:
                    break
    except Exception as e:
        print("图片下载异常:", e)
    else:
        print("图片下载成功: %s" % img_name)


if __name__ == '__main__':
    # 准备图片地址
    img_url1 = "https://ecpro-upload-public-1258059231.picbj.myqcloud.com/upload/10016/p/40b25a97/5582/420d/40b25a97-5582-420d-8a26-74bbb54de6bc.png.jpg"
    img_url2 = "https://ecpro-upload-public-1258059231.picbj.myqcloud.com/upload/10016/p/40b25a97/5582/420d/40b25a97-5582-420d-8a26-74bbb54de6bc.png.jpg"
    img_url3 = "https://ecpro-upload-public-1258059231.picbj.myqcloud.com/upload/10016/p/40b25a97/5582/420d/40b25a97-5582-420d-8a26-74bbb54de6bc.png.jpg"

    # 创建协程指派对应的任务
    g1 = gevent.spawn(download_img, img_url1, "1.jpg")
    g2 = gevent.spawn(download_img, img_url2, "2.jpg")
    g3 = gevent.spawn(download_img, img_url3, "3.jpg")

    # 主线程等待所有的协程执行完成以后程序再退出
    gevent.joinall([g1, g2, g3])
