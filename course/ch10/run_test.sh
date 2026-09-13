#!/bin/zsh
# 激活 conda 环境并运行 test_so101.py
eval "$(/opt/homebrew/Caskroom/miniforge/base/bin/conda shell.zsh hook)"
python test_so101.py
