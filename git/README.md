
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

[alias]
	co = checkout
	ci = commit
	br = branch
	st = status
	unstage = reset HEAD
	last = log -1
	lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```
