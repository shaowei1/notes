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
	docker logs -f "$1" --tail 100
}

function dbuild() {
       docker rm "$1" -f
       docker build -t "$1" -f /root/"$1"/Dockerfile-debug /root/"$1"
       docker run  -t -i --env-file /root/"$1"/.env.example -v /root/"$1"/app/:/app -p "$2":80 --name "$1" --network some-network "$1":latest
}

function dexec() {
	docker exec -it "$1"  /bin/bash
}

function drm() {
	docker rm "$1" -f
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


export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6
source /usr/local/bin/virtualenvwrapper.sh
