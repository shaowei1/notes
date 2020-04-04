1. brew install imagemagick

2. brew upgrade imagemagick

3. 进入terminal, cd 到图片文件夹, 在内部创建一个文件夹 resized

4. 运行如下命令

   ```bash
   ls *.png | xargs -n1 sh -c 'magick $0 -geometry 750x -quality 100 -format jpg resized/$0.jpg'
   ```

> 所有png文件
> 转换为宽度为750的
> 格式为 jpg
> 图片质量为95
> 并且以相同文件名放置在resized文件夹下

https://imagemagick.org/script/command-line-tools.php
