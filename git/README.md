
# show branch graph
git log --graph --pretty=oneline --abbrev-commit

git push origin master
git pull
git status

# many commit branch merge
git rebase

# git config file
touch ~/.gitconfig
```

[user]
	email = shaowei@infimind.com
	name = shaowei

[alias]
	co = checkout
	ci = commit
	br = branch
	st = status
	unstage = reset HEAD
	last = log -1
	lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

# ssh-keygen
使用过程中不要自己定义文件名，不然git 识别不到，需要修改.gitconfig

# .gitignore不生效问题
原因是git ignore只会对不在git仓库中的文件进行忽略，如果这些文件已经在git仓库中，则不会忽略。所以如果需要忽略的文件已经提交到本地仓库，则需要从本地仓库中删除掉，
如果已经提交到远端仓库，则需要从远端仓库中删除

git rm ignored_file -rf
