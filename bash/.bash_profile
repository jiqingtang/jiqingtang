# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

shopt -s checkwinsize

export PATH
unset USERNAME

# Start ssh-agent if necessary
ssh-add -l >/dev/null 2>&1
if [ $? -eq 2 ]; then
  export SSH_AGENT_FILE=$HOME/.ssh/agent.$HOSTNAME
  if [ -r $SSH_AGENT_FILE ]; then
    . $SSH_AGENT_FILE
    ssh-add -l >/dev/null 2>&1
  else
    (exit 2)
  fi
  if [ $? -eq 2 ]; then
    ssh-agent | grep -v ^echo > $SSH_AGENT_FILE
    . $SSH_AGENT_FILE
  fi
fi
