#!/bin/bash

# 自动推送代码到GitHub

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}GitHub 自动推送脚本${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# 添加所有更改
echo -e "${GREEN}[1/3]${NC} 添加文件到暂存区..."
git add .

# 检查是否有更改
if git diff --cached --quiet; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
    exit 0
fi

# 显示更改状态
echo -e "${GREEN}[2/3]${NC} 提交更改..."
git status --short

# 提交
read -p "请输入提交信息 (默认: update): " commit_msg
commit_msg=${commit_msg:-update}

git commit -m "$commit_msg"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 提交成功${NC}"
else
    echo -e "${RED}✗ 提交失败${NC}"
    exit 1
fi

# 推送到远程仓库
echo -e "${GREEN}[3/3]${NC} 推送到远程仓库..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ 推送成功!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ 推送失败${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
