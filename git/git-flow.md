> Shift + Ctrl + M

# merge

develop --> master
1. git pull --all --rebase   拉取远程所有更新并且不生成merge信息
2. 在develop上 git merge release ，并处理冲突
3. git checkout release
4. git merge —no-ff -m “Merge branch develop into release” develop
5. git push

# conflict
```
git reset --hard origin/master
git fetch
git rebase -i origin/master # Usually if I have to check which are the commits that differ from the master I do
git pull -s recursive -X theirs
```



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
# rebase

> 只要你的分支上需要 `rebase` 的所有 `commits` 历史还没有被 `push` 过，就可以安全地使用 `git-rebase`来操作。

### 合并多次体积记录

1. 我们来合并最近的 4 次提交纪录，执行：

```bash
git rebase -i HEAD~4
```

2. 这时候，会自动进入 vi 编辑模式：

```
s cacc52da add: qrcode
s f072ef48 update: indexeddb hack
s 4e84901a feat: add indexedDB floder
s 8f33126c feat: add test2.js

# Rebase 5f2452b2..8f33126c onto 5f2452b2 (4 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
```

3. 如果保存的时候，你碰到了这个错误：

```
error: cannot 'squash' without a previous commit
```

注意不要合并先前提交的东西，也就是已经提交远程分支的纪录。

4. 如果你异常退出了 `vi` 窗口，不要紧张：

```
git rebase --edit-todo
```



这时候会一直处在这个编辑的模式里，我们可以回去继续编辑，修改完保存一下：

```
git rebase --continue
```



5. 查看结果

```
git log
```

### 分支合并

首先，`git` 会把 `feature1` 分支里面的每个 `commit` 取消掉；
其次，把上面的操作临时保存成 `patch` 文件，存在 `.git/rebase` 目录下；
然后，把 `feature1` 分支更新到最新的 `master` 分支；
最后，把上面保存的 `patch` 文件应用到 `feature1` 分支上；

1. git checkout experiment
   git rebase master

![](./imgs/basic-rebase-3.png)

2. git checkout master
   git merge experiment

![](./imgs/basic-rebase-4.png)

3. 在 `rebase` 的过程中，也许会出现冲突 `conflict`。在这种情况，`git` 会停止 `rebase` 并会让你去解决冲突。在解决完冲突后，用 `git add` 命令去更新这些内容。

注意，你无需执行 git-commit，只要执行 continue

```
git rebase --continue
```

这样 `git` 会继续应用余下的 `patch` 补丁文件。

4. 在任何时候，我们都可以用 `--abort` 参数来终止 `rebase` 的行动，并且分支会回到 `rebase` 开始前的状态。

```
git rebase —abort
```

[reference]: http://jartto.wang/2018/12/11/git-rebase/



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

# branch
git branch -d xxx
