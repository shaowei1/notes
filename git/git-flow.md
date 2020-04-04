# merge

develop --> master
1. git pull --all --rebase   拉取远程所有更新并且不生成merge信息
2. 在develop上 git merge release ，并处理冲突
3. git checkout release
4. git merge —no-ff -m “Merge branch develop into release” develop
5. git push

# commint info format
```
<type>(<scope>): <subject> <BLANK LINE> <body>
<BLANK LINE>
<footer>

 type: 必填
➤ feat:新功能
➤ fix:修复bug
➤ docs:文档变动
➤ style:格式调整，对代码实际运行没有改动，例如添加空行、格式化等
➤ refactor:重构
➤ perf:提升性能的改动
➤ test:添加或修正测试代码
➤ chore:构建过程或辅助工具和库(如文档生成)的更改
subject:必填， 具体的修改描述信息
scope:修改范围，选填。主要是这次修改涉及到的部分，简单概括，例如 login、train-order
```
git commit --amend 指令追加改动

# stash
切换正在修改的分支
git checkout release  # error
git stash
git checkout release  # right

git checkout develop  # return
git stash list
git stash pop  # recover

# log
git log —pretty=oneline
git reflog

# checkout
➤ 创建新分支并推送到远程分支
git checkout -b hotfix-xxx
git push --set-upstream origin hotfix-xxx

➤ 更新远程分支的本地列表
git remote update origin --prune

# tag
git tag

git tag  release-v1.0.10

git tag -d  release-v1.0.10

git push origin --tags

# remove
-  仅仅删除暂存区里的文件
git rm --cache 文件名

- 删除暂存区和工作区的文件
git rm -f 文件名

- 删除错误提交的commit
//仅仅只是撤销已提交的版本库，不会修改暂存区和工作区
git reset --soft 版本库ID


//仅仅只是撤销已提交的版本库和暂存区，不会修改工作区
git reset --mixed 版本库ID


//彻底将工作区、暂存区和版本库记录恢复到指定的版本库
git reset --hard 版本库ID
