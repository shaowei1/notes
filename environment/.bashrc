# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
function dlogs() {
	docker logs -f "$1" --tail 100
}

function drestart() {
	docker restart "$1"
}

function dexec() {
	docker exec -it "$1"  /bin/bash
}

ZSH_THEME="robbyrussell"

plugins=(git)
source $ZSH/oh-my-zsh.sh


alias grep='grep --color=always'

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

function rm () {
  local path
  for path in "$@"; do
    # ignore any arguments
    if [[ "$path" = -* ]]; then :
    else
      local dst=${path##*/}
      # append the time if necessary
      while [ -e ~/.Trash/"$dst" ]; do
        dst="$dst "$(date +%H-%M-%S)
      done
      /bin/mv "$path" ~/.Trash/"$dst"
    fi
  done
}
