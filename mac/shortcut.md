# sublime
## json
OS X: cmd+ctrl+j

# Text Mate
## json reformate
control + shift + h
## markdown preview
control + option + command + p
## Searching
Edit → Find → Find Next (⌘G)
Edit → Find → Find Previous (⇧⌘G)
Edit → Find → Show History (⌃⌥⌘F)
Edit → Find → Use Selection for Find (⌘E)


# Atom
## shortcuts
- markdown preview
ctrl + shift + m
- Searching
cmd + t
- show file tree
cmd + \
- copy current row
cmd + shift + d
- open file
cmd + o
- move focus to tree
control + 0 # a，m，delete
- git
option + ->
- jump into row
ctrl - g
- jump with function
cmd - r
- 移动行，单词
ctrl + a/e/b/f
ctrl + p/n/f/b

## setting
- hide some file
file > setting > package > tree-view, Hide igorned Names
- set china resource
apm config set registry http://registry.npm.taobao.org

## package
platformio-ide-terminal:在当前编辑窗口开启cmd终端
markdown-toc
npm install --save markdown-toc


## customizing keybindings
https://flight-manual.atom.io/using-atom/sections/basic-customization/#customizing-keybindings

vi .atom/config.cson

## install package
apm install formatter
or
apm install formatter-json

'atom-text-editor':
  'shift-cmd-j': 'pretty-json:prettify'


brew install npm

npm config get proxy
npm config get https-proxy

npm config set proxy null
npm config set https-proxy null

npm config set proxy http://domain:8080
npm config delete proxy

npm config set registry http://registry.cnpmjs.org/

.npmrc
registry = http://registry.cnpmjs.org

# System shortcuts
```
command + M : minimize

Command + o : open file

Option + command + esc: force quit a app

control + command + f: Full screen

shift + command + 5: screenshot

shift + command + N: create a new folder in the Finder

Command + ,: open the preferences

control + command + D: translate a word of selected
```

# pycharm
- 折叠代码块
cmd + shift + -
