#!/bin/zsh
# 启动交互式控制
echo "停止后台 dataflow..."
dora destroy

echo "启动 dora coordinator..."
dora up &
sleep 2

echo "前台运行 dataflow (可以使用键盘控制)..."
echo "按 Ctrl+C 停止"
dora run dataflow.yml
