export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --use-on-cd --shell zsh)"

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="fishy"
plugins=(git fzf z zsh-autosuggestions zsh-syntax-highlighting)
source "$ZSH/oh-my-zsh.sh"
