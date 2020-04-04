Python虚拟环境
====================
动态语言中Ruby、Python都有自己的虚拟环境，通过创建虚拟环境能够使不同的项目之间的运行环境保持独立性而相互不受影响。例如项目A依赖Django1.4，而项目B依赖Django1.5，这时它就能解决此类问题。Ruby有Vagrant，Python有virtualenv，本文讨论Python虚拟环境。[virtualenv](https://docs.python.org/zh-cn/3/tutorial/venv.html)可用于创建独立的Python环境，它会创建一个包含项目所必须要的执行文件。

#### install python3.7
##### 误删虚拟环境
find ~/.virtualenvs/my-virtual-env/ -type l -delete
virtualenv ~/.virtualenvs/my-virtual-env

##### openssl
wget http://www.openssl.org/source/openssl-1.1.1.tar.gz
tar -zxvf openssl-1.1.1.tar.gz
cd openssl-1.1.1
./config --prefix=$HOME/openssl shared zlib
make && make install
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/openssl/lib" >> $HOME/.bash_profile
source $HOME/.bash_profile

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/openssl/lib" >> $HOME/.bash_profile
source $HOME/.bash_profile

LD_LIBRARY_PATH环境变量主要用于指定查找共享库（动态链接库）时除了默认路径之外的其他路径。当执行函数动态链接.so时，如果此文件不在缺省目录下‘/lib' and ‘/usr/lib'，那么就需要指定环境变量LD_LIBRARY_PATH

---------------------------------------------------------------------------------
whereis python

yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel -y


#运行这个命令添加epel扩展源
yum -y install epel-release
#安装pip
yum install python-pip


wget wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
tar -zxvf Python-3.7.0.tgz
cd Python-3.7.6
#进入解压后的目录，依次执行下面命令进行手动编译
./configure prefix=/usr/local/python3
make && make install

#添加python3的软链接
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3.7
#添加 pip3 的软链接
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3.7
#测试是否安装成功了
python -V

- ignore 更改yum配置，因为其要用到python2才能执行，否则会导致yum不能正常使用（不管安装 python3的那个版本，都必须要做的）
vi /usr/bin/yum
把 #! /usr/bin/python 修改为 #! /usr/bin/python2
vi /usr/libexec/urlgrabber-ext-down
把 #! /usr/bin/python 修改为 #! /usr/bin/python2

####安装
    virtualenv ve -p $HOME/.localpython/bin/python2.7 or  virtualenv test-env -p /usr/local/python3/bin/python3.7
    source ve/bin/activate   
    $ python3 -m venv flask-env  # 在当前目录下建立一个名为flask-env的虚拟环境
    $ pip3 install virtualenv
    $ pip3 install virtualenvwrapper
    $ mkdir $HOME/.virtualenvs

####使用方法

    $ cd my_project_folder
    $ virtualenv venv
如，创建名为**ENV**的虚拟环境  

    $ virtualenv ENV
执行完命令后它会在当前目录下创建文件夹，这个文件夹包含一些Python执行文件，以及pip副本用于安装其他的packges。  

    .
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── activate_this.py
    │   ├── easy_install
    │   ├── easy_install-3.5
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.5
    │   ├── python -> python3
    │   ├── python3
    │   ├── python3.5 -> python3
    │   └── wheel
    ├── include
    │   └── python3.5m -> /Library/Frameworks/Python.framework/Versions/3.5/include/python3.5m
    └── lib
        └── python3.5

此外在创建env的时候可以选择Python解释器，例如：  

    $ virtualenv -p /usr/local/bin/python3 venv
默认情况下，虚拟环境会依赖系统环境中的site packages，就是说系统中已经安装好的第三方package也会安装在虚拟环境中，如果不想依赖这些package，那么可以加上参数 `--no-site-packages`建立虚拟环境  

    virtualenv --no-site-packages [虚拟环境名称]

####启动虚拟环境

    cd ENV
    source ./bin/activate

注意此时命令行会多一个`(ENV)`，ENV为虚拟环境名称，接下来所有模块都只会安装到这个虚拟的环境中去。

####退出虚拟环境  

    $ deactivate

如果想删除虚拟环境，那么直接运行`rm -rf venv/`命令即可。  

####在虚拟环境安装Python packages

Virtualenv 附带有pip安装工具，因此需要安装的packages可以直接运行：  

    pip install [套件名称]
如果没有启动虚拟环境，系统也安装了pip工具，那么packages将被安装在系统环境中，为了避免发生此事，可以在`~/.bashrc`文件中加上：  

    export PIP_REQUIRE_VIRTUALENV=true
如果在没开启虚拟环境时运行pip，就会提示错误：Could not find an activated virtualenv (required).  


####Virtualenvwrapper
Virtaulenvwrapper是virtualenv的扩展包，用于更方便管理虚拟环境，它可以做：  
1. 将所有虚拟环境整合在一个目录下  
2. 管理（新增，删除，复制）虚拟环境  
3. 切换虚拟环境  
4. ...  

#####安装（确保virtualenv已经安装）

    $ pip install virtualenvwrapper

此时还不能使用virtualenvwrapper，默认virtualenvwrapper安装在/usr/local/bin下面，实际上你需要运行virtualenvwrapper.sh文件才行，先别急，打开这个文件看看,里面有安装步骤，我们照着操作把环境设置好。  

1. 创建目录用来存放虚拟环境

        mkdir $HOME/Envs
2. 编辑~/.zshrc或~/.bashrc（根据你使用shell类型决定）

        export WORKON_HOME=$HOME/Envs
        source /usr/local/bin/virtualenvwrapper.sh
3. 运行：

        $ source    ~/.zshrc

此时virtualenvwrapper就可以使用了。virtualenvwrapper的基本使用方式：   

1. 列出虚拟环境列表  

        workon 或者 lsvirtualenv
2. 新建虚拟环境  

        mkvirtualenv [虚拟环境名称]

3. 启动/切换虚拟环境  

        workon [虚拟环境名称]

4. 删除虚拟环境  

        rmvirtualenv [虚拟环境名称]

5. 离开虚拟环境，和virutalenv一样的命令

        deactivate


参考：  
http://www.virtualenv.org/en/latest/  
http://stackoverflow.com/questions/11372221/virtualenvwrapper-not-found  
http://www.openfoundry.org/tw/tech-column/8516-pythons-virtual-environment-and-multi-version-programming-tools-virtualenv-and-pythonbrew  
http://virtualenvwrapper.readthedocs.org/en/latest/index.html  
