SRX-DGNMZ-3C
# add exec file
```
<!-- .bashrc -->
export PATH=${PATH}:/Users/root1/Downloads/command
可执行文件放在command 目录下
```
easy_install brew

# zsh install document
https://medium.com/@Clovis_app/configuration-of-a-beautiful-efficient-terminal-and-prompt-on-osx-in-7-minutes-827c29391961

# install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew cask install iterm2

# zsh
brew install zsh

sh -c "$(curl -fsSL
https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
# brew
```
cd "$(brew --repo)" && git remote set-url origin https://git.coding.net/homebrew/homebrew.git

cd $home && brew update
```


# mac install

```
# python -m pip install --user virtualenv # 废弃
# -m python2 use virtualenv, python3 use venv

brew install python3
easy_install pip

https://support.apple.com/en-us/HT204323
pip install --upgrade setuptools

pip install -r requirements.txt  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install --upgrade requests

brew update
```



```
pip install virtualenv
sudo pip install tld --ignore-installed six
sudo pip install virtualenvwrapper
which virtualenvwrapper.sh
cat virtualenvwrapper.sh# see operate documents

lssitepackages # show package recently installed
```



# pip set aliyuan

```
$HOME/.config/pip/pip.conf
cat $HOME/.config/pip/pip.conf
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```



# Switch Omega settingß
https://wall-guide.readthedocs.io/zh/latest/SwitchyOmega%E4%BB%A3%E7%90%86%E8%AE%BE%E7%BD%AE.html



# terminal

```
# open file
man open
# open with a certain application
open -a "QuickTime Player" ~/Desktop/filename.mp4

# install tldr
brew tap tldr-pages/tldr && brew install tldr
```

# set startapp

```
system prefercene --> user and group --> login items
```

# sound
```
sudo killall coreaudiod
and then restart coreaudiod like this:

sudo -u _coreaudiod /usr/sbin/coreaudiod &
This will kill the Core Audio daemon (which is a system-level process, so escalating your privileges to super-user levels using sudo is necessary)
```

# ssh setting

vi /root/.ssh/config
ServerAliveInterval 60
ssh client will auto detect connection with server about some time, will not be broken for a long time
sudo launchctl stop com.openssh.sshd
