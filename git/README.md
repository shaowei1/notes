
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
