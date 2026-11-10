# ========================================
# Default Ultramarine zsh Config
# ========================================

# Initialize Starship
eval "$(starship init zsh)"

source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

source /usr/share/fzf/shell/key-bindings.zsh

# Ctrl + Arrow keybindings
bindkey "^[[1;5D" backward-word
bindkey "^[[1;5C" forward-word

# Ctrl + Backspace/Delete Kebindings
bindkey '^H' backward-kill-word
bindkey '^[[3;5~' kill-word

# Alt + Backspace/Delete Keybinds
bindkey "^[[3~" delete-char
bindkey -M emacs '^[[3;3~' kill-word

# Home/End Keybinds
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt appendhistory
setopt SHARE_HISTORY
setopt autocd

# Allow Bash-style globbing
unsetopt nomatch

# Bind Home/End
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[1~' beginning-of-line
bindkey '^[[4~' end-of-line

# Search history using current input as a prefix
autoload -Uz up-line-or-beginning-search down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search
bindkey '^[[A' up-line-or-beginning-search
bindkey '^[OA' up-line-or-beginning-search
bindkey '^[[B' down-line-or-beginning-search
bindkey '^[OB' down-line-or-beginning-search

# Ctrl+Z to undo
bindkey '^Z' undo
# Alt+Z to redo
bindkey '^[z' redo

# Case-insensitive completion
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# Colored completion lists
zstyle ':completion:*' list-colors "${(@s.:.)LS_COLORS}"

# Ctrl+Arrows/Backspace/Delete stop at punctuation like Bash
autoload -U select-word-style
select-word-style bash

# ========================================
# End of Default Config
# ========================================
