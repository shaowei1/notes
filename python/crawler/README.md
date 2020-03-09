```shell script
pip3 install you-get #安装You-Get
pip3 install --upgrade you-get #升级You-Get

you-get

you-get [url] #一般情况下用这一个命令就够了,使用最简单,而且下载的是最高质量

you-get -i [url]

you-get --format=hd3 #这是优酷的1080p
you-get --itag=137 #这是YouTube的1080p

you-get -o [new_path] [url]

you-get -f [url]

you-get [playlist_url]

"""Bilibili的弹幕文件是.xml格式,本地播放器可能无法加载,可以使用Danmu2Ass
将.xml格式转换为.ass格式
"""

you-get -x 127.0.0.1:1080 [url]


you-get "Video_Name"

brew install ffmpeg
brew info ffmpeg
brew upgrade ffmpeg
brew install tesseract-lang

ffmpeg -i 脱口秀.flv  -b:v  640k  脱口秀.mp4
# http://ffmpeg.org/

cat segment1_0_av.ts segment2_0_av.ts segment3_0_av.ts > all.ts
ffmpeg -i all.ts -bsf:a aac_adtstoasc -acodec copy -vcodec copy all.mp4

```
