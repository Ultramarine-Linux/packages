
# Ultramarine ZSH config
# initialize starship
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

# [Ctrl] + Alt + <Arrows/Home/End> to select text, Backspace/Delete remove the selection
# Copying or pasting over selected text doesn't currently work
# Uses Alt instead of Shift because Konsole already binds Shift+Arrows by default
_shift_select() {
  if (( ! REGION_ACTIVE )); then
    MARK=$CURSOR REGION_ACTIVE=1
    _shift_selecting=1
  fi
  zle ${WIDGET#select-}
}
for widget in backward-char forward-char backward-word forward-word beginning-of-line end-of-line; do
  zle -N select-$widget _shift_select
done
unset widget

_shift_select_clear() {
  if (( _shift_selecting )) && [[ $LASTWIDGET != select-* ]]; then
    REGION_ACTIVE=0 _shift_selecting=0
    _zsh_highlight
  fi
}
autoload -Uz add-zle-hook-widget
add-zle-hook-widget line-pre-redraw _shift_select_clear

_shift_select_delete() {
  if (( REGION_ACTIVE )); then
    zle kill-region
  else
    zle ${WIDGET#shift-select-}
  fi
}
zle -N shift-select-backward-delete-char _shift_select_delete
zle -N shift-select-delete-char _shift_select_delete
bindkey '^?' shift-select-backward-delete-char
bindkey '^[[3~' shift-select-delete-char

bindkey '^[[1;3D' select-backward-char
bindkey '^[[1;3C' select-forward-char
bindkey '^[[1;7D' select-backward-word
bindkey '^[[1;7C' select-forward-word
bindkey '^[[1;3H' select-beginning-of-line
bindkey '^[[1;3F' select-end-of-line

zle_highlight=(region:bg=blue)
