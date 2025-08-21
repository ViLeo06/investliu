#!/bin/bash

# 老刘投资决策小程序部署验证脚本

echo "=========================================="
echo "老刘投资决策小程序部署验证"
echo "=========================================="

# 1. 检查数据文件
echo "1. 检查数据文件..."
files=("summary.json" "stocks_a.json" "stocks_hk.json" "market_timing.json" "miniprogram_config.json" "laoliu_quotes.json")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
        # 检查文件大小
        size=$(wc -c < "$file")
        if [ $size -gt 100 ]; then
            echo "   文件大小: ${size} bytes"
        else
            echo "❌ $file 文件过小，可能有问题"
        fi
    else
        echo "❌ $file 不存在"
    fi
done

# 2. 检查小程序配置
echo -e "\n2. 检查小程序配置..."
if [ -f "miniprogram/app.js" ]; then
    echo "✅ 小程序入口文件存在"
    # 检查API地址配置
    if grep -q "vileo06.github.io" miniprogram/app.js; then
        echo "✅ API地址配置正确"
    else
        echo "❌ API地址配置可能有问题"
    fi
else
    echo "❌ 小程序入口文件不存在"
fi

if [ -f "miniprogram/app.json" ]; then
    echo "✅ 小程序配置文件存在"
    # 检查页面配置
    if grep -q "pages/index/index" miniprogram/app.json; then
        echo "✅ 页面配置正确"
    else
        echo "❌ 页面配置可能有问题"
    fi
else
    echo "❌ 小程序配置文件不存在"
fi

# 3. 检查页面文件
echo -e "\n3. 检查页面文件..."
pages=("index" "stocks" "analysis" "portfolio" "settings")
for page in "${pages[@]}"; do
    dir="miniprogram/pages/$page"
    if [ -d "$dir" ]; then
        echo "✅ $page 页面目录存在"
        # 检查必需文件
        files=("$page.js" "$page.json" "$page.wxml" "$page.wxss")
        for file in "${files[@]}"; do
            if [ -f "$dir/$file" ]; then
                echo "   ✅ $file"
            else
                echo "   ❌ $file 缺失"
            fi
        done
    else
        echo "❌ $page 页面目录不存在"
    fi
done

# 4. 检查数据生成器
echo -e "\n4. 检查数据生成器..."
if [ -f "data_processor/main.py" ]; then
    echo "✅ 数据生成器存在"
    
    # 尝试运行数据生成器
    echo "尝试运行数据生成器..."
    cd data_processor
    if python3 main.py > /dev/null 2>&1; then
        echo "✅ 数据生成器运行成功"
    else
        echo "❌ 数据生成器运行失败，可能缺少依赖"
    fi
    cd ..
else
    echo "❌ 数据生成器不存在"
fi

# 5. 检查GitHub Pages文件
echo -e "\n5. 检查GitHub Pages文件..."
if [ -f "index.html" ]; then
    echo "✅ GitHub Pages入口文件存在"
else
    echo "❌ GitHub Pages入口文件不存在"
fi

# 6. 检查文档
echo -e "\n6. 检查文档..."
docs=("README.md" "CLAUDE.md" "docs/release_checklist.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✅ $doc 存在"
    else
        echo "❌ $doc 不存在"
    fi
done

# 7. 生成部署报告
echo -e "\n=========================================="
echo "部署验证完成"
echo "=========================================="

# 统计结果
total_checks=0
passed_checks=0

# 这里可以添加更详细的统计逻辑

echo "建议下一步操作："
echo "1. 在微信开发者工具中打开 miniprogram 目录"
echo "2. 配置小程序AppID: wx2aad9cd988058c1f"
echo "3. 预览测试所有功能"
echo "4. 上传代码并提交审核"
echo ""
echo "数据更新命令："
echo "cd data_processor && python3 main.py"
echo ""
echo "GitHub Pages访问地址："
echo "https://vileo06.github.io/investliu/"