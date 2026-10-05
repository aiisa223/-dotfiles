# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs

# Added by Toolbox App
export PATH="$PATH:/home/ali/.local/share/JetBrains/Toolbox/scripts"

eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
