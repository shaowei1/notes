"""
阿里云存储OSS中设置上传文件ContentType



如果你使用浏览器上传文件，则浏览器会自动在header中设置正确地content type，然后对文件的访问会得到正确地回应。



如果采用编程的方式，处理文件上传，保持到 aliyun OSS中，则需要正确设置content type，否则，缺省的content type都为application/octet-stream。



如果类型是application/octst-stream，则在访问文件时，会导致下载操作。在浏览器中，会弹出下载保存的对话框。

"""
files = {
    'file1': ('foo.gif', open('foo.gif', 'rb'), 'image/gif'),
    'file2': ('bar.png', open('bar.png', 'rb'), 'image/png'),
}
response = requests.post(url, files=files)
