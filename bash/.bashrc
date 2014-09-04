# .bashrc

# User specific aliases and functions

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

export EDITOR='gvim -f'
alias grep='grep --color=auto'
alias gg='git grep -n'

# Add default keys
ssh-add -l >/dev/null 2>&1
error=$?
if [[ $error -eq 2 && -r $SSH_AGENT_FILE ]]; then
  . $SSH_AGENT_FILE
  ssh-add -l >/dev/null 2>&1
  error=$?
fi
if [ $error -eq 1 ]; then
  ssh-add
fi
unset error

function gp() {
  SGR0="\[$(tput sgr0)\]"
  GREEN="\[$(tput setaf 2)\]"
  CYAN="\[$(tput setaf 6)\]"
  export PS1="$CYAN[\u@\h$SGR0\$(git branch 2> /dev/null | grep -e '\* ' | sed 's/^..\(.*\)/ $GREEN\1$SGR0/') $CYAN\w]$SGR0 "
}

function ugp() {
  SGR0="\[$(tput sgr0)\]"
  CYAN="\[$(tput setaf 6)\]"
  export PS1="$CYAN[\u@\h \w]$SGR0 "
}

function d() {
  dirs -v
  echo -n 'Which dir: '
  read i
  [ -n "$i" ] && pushd +$i
}

function dn() {
  pushd +1
}

function dp() {
  pushd -0
}
