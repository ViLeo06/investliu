#!/bin/bash

# 老刘投资决策系统 - 项目测试脚本

echo "========================================"
echo "老刘投资决策系统 - 集成测试"
echo "========================================"

# 检查Python环境
echo "1. 检查Python环境..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python未安装或不在PATH中"
    exit 1
fi

# 检查依赖包
echo "2. 检查Python依赖包..."
python -c "
import requests
import pandas
import numpy
print('✅ 核心依赖包检查通过')
"

if [ $? -ne 0 ]; then
    echo "❌ 依赖包缺失，请运行: pip install -r requirements.txt"
    exit 1
fi

# 检查项目结构
echo "3. 检查项目结构..."
required_dirs=("data_processor" "miniprogram" "static_data" "notes" ".github/workflows")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir 目录存在"
    else
        echo "❌ $dir 目录不存在"
        exit 1
    fi
done

# 检查关键文件
echo "4. 检查关键文件..."
required_files=(
    "data_processor/ocr_processor.py"
    "data_processor/rule_extractor.py" 
    "data_processor/stock_data_fetcher.py"
    "data_processor/stock_analyzer.py"
    "data_processor/data_generator.py"
    "update_data.py"
    "requirements.txt"
    "miniprogram/app.js"
    "miniprogram/app.json"
    ".github/workflows/deploy.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        exit 1
    fi
done

# 测试数据模块
echo "5. 测试数据处理模块..."
python -c "
import sys
sys.path.append('.')
from data_processor import StockDataFetcher, StockAnalyzer

# 测试股票数据获取
fetcher = StockDataFetcher()
print('✅ 股票数据获取模块导入成功')

# 测试股票分析
analyzer = StockAnalyzer()
print('✅ 股票分析模块导入成功')

print('✅ 数据处理模块测试通过')
"

if [ $? -ne 0 ]; then
    echo "❌ 数据处理模块测试失败"
    exit 1
fi

# 创建测试配置
echo "6. 创建测试配置..."
cat > test_config.py << EOF
# 测试配置文件
SINA_API_BASE = "https://hq.sinajs.cn/list="
EASTMONEY_API_BASE = "https://push2.eastmoney.com/api/qt/clist/get"
UPDATE_INTERVAL = 24
MAX_RECOMMEND_STOCKS = 5
MIN_MARKET_CAP = 50
MAX_PE_RATIO = 30
MIN_ROE = 0.1
MAX_DEBT_RATIO = 0.6
EOF

# 测试数据生成
echo "7. 测试数据生成（简化版）..."
python -c "
import sys
import os
sys.path.append('.')

# 导入配置
sys.path.append('.')
import test_config as config

from data_processor.stock_data_fetcher import StockDataFetcher
from data_processor.stock_analyzer import StockAnalyzer

# 测试获取少量数据
fetcher = StockDataFetcher()
print('正在获取测试数据...')

# 获取市场指数
indices = fetcher.get_market_index()
if indices:
    print(f'✅ 获取到 {len(indices)} 个市场指数')
else:
    print('⚠️  未获取到市场指数数据')

# 获取少量股票数据
a_stocks = fetcher.get_stock_list_a(page=1, size=5)
if a_stocks:
    print(f'✅ 获取到 {len(a_stocks)} 只A股数据')
else:
    print('⚠️  未获取到A股数据')

print('✅ 数据获取测试完成')
"

if [ $? -ne 0 ]; then
    echo "❌ 数据生成测试失败"
    exit 1
fi

# 检查小程序文件
echo "8. 检查小程序文件..."
miniprogram_files=(
    "miniprogram/app.js"
    "miniprogram/app.json"
    "miniprogram/app.wxss"
    "miniprogram/pages/index/index.js"
    "miniprogram/pages/index/index.wxml"
    "miniprogram/pages/index/index.wxss"
    "miniprogram/pages/index/index.json"
)

for file in "${miniprogram_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        exit 1
    fi
done

# 检查JSON文件格式
echo "9. 检查小程序配置文件格式..."
python -c "
import json

# 检查app.json格式
with open('miniprogram/app.json', 'r', encoding='utf-8') as f:
    json.load(f)
print('✅ app.json 格式正确')

# 检查project.config.json格式  
with open('miniprogram/project.config.json', 'r', encoding='utf-8') as f:
    json.load(f)
print('✅ project.config.json 格式正确')
"

if [ $? -ne 0 ]; then
    echo "❌ 小程序配置文件格式错误"
    exit 1
fi

# 清理测试文件
rm -f test_config.py

echo ""
echo "========================================"
echo "✅ 所有测试通过！"
echo "========================================"
echo ""
echo "🚀 项目已准备就绪，可以进行以下操作："
echo ""
echo "1. 配置API密钥:"
echo "   cp config.example.py config.py"
echo "   # 编辑config.py添加你的API密钥"
echo ""
echo "2. 生成数据:"
echo "   python update_data.py"
echo ""
echo "3. 部署到GitHub Pages:"
echo "   git add ."
echo "   git commit -m '部署老刘投资决策系统'"
echo "   git push origin main"
echo ""
echo "4. 开发小程序:"
echo "   # 用微信开发者工具打开 miniprogram 目录"
echo ""
echo "📊 项目特点:"
echo "   ✓ 零服务器成本"
echo "   ✓ 自动数据更新"  
echo "   ✓ 智能股票推荐"
echo "   ✓ 完整小程序界面"
echo ""
echo "⚠️  注意事项:"
echo "   - 投资有风险，仅供参考"
echo "   - 需要申请相关API密钥"
echo "   - 小程序需要相应资质"
echo ""