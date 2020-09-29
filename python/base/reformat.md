### 并不修改文件
$ yapf <python file>

### 格式化前后对比
$ yapf -d <python file>

### 直接修改源文件
$ yapf -i <python file>

### 导出配置文件
$ yapf --style-help > style.cfg

### 自定义配置文件并使用
此例为将缩进由4个空格改为2个空格

$ yapf --style-help > my_style.cfg
$ sed -i "s/indent_width=4/indent_width=2/" my_style.cfg
$ yapf --style my_style.cfg loops.py

### 在代码中控制是否使用yapf
```
# yapf: disable
<code will not be formatted>
# yapf: enable

```

### 并发格式化多个文件，需要futures模块支持
$ yapf -pi *.py
