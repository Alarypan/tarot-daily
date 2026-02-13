#!/bin/bash
# 塔罗牌每日运势 - 双击运行

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

clear

echo ""
echo "========================================================"
echo "  🔮  正在启动「塔罗牌每日运势」..."
echo "========================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "  ❌  未找到Python3，请先安装Python"
    echo ""
    read -p "按回车键关闭..."
    exit 1
fi

# 运行主程序
python3 "$SCRIPT_DIR/main.py"
