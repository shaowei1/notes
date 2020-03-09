import os
import re

import requests


def get_number(data):
    length = len(str(data))
    return (3 - length) * "0" + str(data)


if __name__ == '__main__':
    for i in range(226):
        number = get_number(i)
        m3u8 = f'https://hd1.o0omvo0o.com/dm/EBCAFAFB/SD/out{number}.ts'
        try:
            r = requests.get(m3u8)

            if r.status_code == 200:
                text = r.text
                # m3u8_rel = m3u8.replace('index.m3u8', '') + re.split('n', text)[-1]
                ffmpeg = "ffmpeg"
                output = '/Users/root1/Movies/aa.mp4'
                cmd = ffmpeg + " -i " + text + " -vcodec copy -acodec copy " + output
                os.system(cmd)
        except Exception as e:
            continue
