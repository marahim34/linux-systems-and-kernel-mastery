12. The Modern CLI — zsh, fzf, ripgrep & Friends
zsh + a framework
sudo apt install zsh
chsh -s $(which zsh)
sh -c "$(curl -fsSL
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# ~/.zshrc
plugins=(git z sudo docker)

1. zsh: bash-compatible with superior completion (menu-select, typo correction, mid-word matching).