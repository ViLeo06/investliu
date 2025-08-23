# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 老刘投资决策程序 - Claude Code Project Guide

## Project Overview
A stock investment decision support system based on "老刘" (Lao Liu)'s handwritten investment notes, delivered as a WeChat Mini Program focused on long-term value investing strategies.

## Essential Development Commands

### Data Processing Pipeline
```bash
# Generate latest stock recommendations (PRIMARY COMMAND)
cd data_processor && python3 main.py

# Install Python dependencies
pip install -r requirements.txt

# OCR processing for handwritten investment notes
python complete_ocr_processor.py  # Process 27 notebook images
python extract_quotes.py  # Extract investment quotes from OCR results

# Validate generated data files
ls -la *.json  # Check root directory JSON files
python -m json.tool summary.json  # Validate JSON format
python -m json.tool static_data/laoliu_quotes.json  # Validate quotes data
```

### WeChat Mini Program Development
```bash
# Open miniprogram directory in WeChat Developer Tools
# AppID: wx2aad9cd988058c1f
# Project Name: 老刘投资决策

# Build and test commands (via WeChat Developer Tools UI):
# - Click "Preview" → Scan QR code for device testing
# - Click "Upload" → Enter version number for release

# Local file validation
find miniprogram/pages -name "*.wxml" -o -name "*.wxss" -o -name "*.js"
```

### Deployment Workflow
```bash
# Complete data update and deployment
cd data_processor && python3 main.py  # Generate fresh data
git add *.json static_data/
git commit -m "update stock data and improvements"
git push origin master

# Verify GitHub Pages deployment
curl -I https://vileo06.github.io/investliu/summary.json
```

## High-Level Architecture

### Core Design Philosophy
- **Serverless Architecture**: Static JSON data hosted on GitHub Pages
- **Local Data Processing**: Python scripts generate investment recommendations
- **WeChat Mini Program**: Native development consuming static data
- **Cost Optimization**: Completely free technology stack

### Data Flow Architecture
```
Handwritten Notes → OCR Recognition → Rule Extraction → Python Analysis → JSON Output → GitHub Pages → Mini Program
```

### Key System Components

#### 1. Data Processing Layer (`data_processor/`)
- **`main.py`**: Primary orchestrator - runs all data generation workflows
- **`StockDataFetcher`**: Retrieves stock data (currently simulated API calls)
- **`StockAnalyzer`**: Four-dimensional scoring model (Valuation 25% + Growth 25% + Profitability 25% + Safety 25%)
- **`LaoLiuAnalyzer`**: Specialized analyzer implementing Lao Liu's investment philosophy
- **`RuleExtractor`**: Rule engine based on Lao Liu's investment experience
- **`DataGenerator`**: Coordinates all components to generate final JSON files

#### 2. OCR Processing Pipeline (Root directory scripts)
- **`complete_ocr_processor.py`**: Processes 27 investment note images, supports multiple OCR methods
- **`extract_quotes.py`**: Extracts curated investment quotes, categorized as Masters/Strategy/Philosophy
- **`structure_analyzer.py`**: Converts raw OCR text into structured investment rules

#### 3. Static Data Layer (Root directory JSON files)
- **`summary.json`**: Aggregated data and today's recommendations
- **`stocks_a.json/stocks_hk.json`**: A-share/H-share detailed recommendations
- **`market_timing.json`**: Market timing advice and sentiment analysis
- **`miniprogram_config.json`**: Mini program runtime configuration
- **`static_data/laoliu_quotes.json`**: Investment quotes data (17 curated quotes, 3 categories)

#### 4. Mini Program Frontend (`miniprogram/`)
- **`app.js`**: Global configuration with retry mechanism API wrapper and quotes version management
- **Core Pages**: Home (daily quotes), Stock Selection, Analysis, Portfolio, Settings
- **`components/quote-card/`**: Quote card component with sharing functionality
- **`utils/shareCard.js`**: Canvas-based share card generator
- **Caching Strategy**: 1-hour local cache with auto-refresh mechanism

### Investment Analysis Algorithm Core
```python
# Four-dimensional scoring model (implemented in stock_analyzer.py)
total_score = (valuation_score * 0.25 + 
               growth_score * 0.25 + 
               profitability_score * 0.25 + 
               safety_score * 0.25) * industry_weight
```

Based on financial metrics: PE, PB, ROE, debt ratio, combined with industry comparison and market environment adjustments.

## Technology Stack
- **Data Processing**: Python 3.8+ (pandas, requests, akshare, baidu-aip, tencentcloud-sdk-python)
- **Data Storage**: Static JSON files hosted on GitHub Pages
- **Frontend**: WeChat Mini Program native development
- **API Data Sources**: Free stock APIs (currently using mock data)

## 关键开发模式

### UI设计系统（2025年8月更新）
项目采用现代化金融主题设计，重点特性：
```css
/* 核心配色方案 */
主渐变: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
成功色: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)
警告色: linear-gradient(135deg, #f39c12 0%, #e67e22 100%)
危险色: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)

/* 关键样式类 */
.card - 玻璃拟态卡片，带backdrop-filter效果
.btn-primary/.btn-secondary/.btn-ghost - 现代化按钮系统
.tag-success/.tag-warning/.tag-danger - 彩色标签系统
.fade-in/.slide-up/.bounce - 动画效果类
.stock-item - 股票卡片（包含头像、评分、推荐等级）

/* TabBar现代化设计 */
- 选中时字体变大(22rpx→26rpx)、加粗、缩放(scale 1.08)
- 底部渐变指示器，带动画效果
- 毛玻璃背景效果，半透明白色
- 品牌蓝紫色(#667eea)选中状态
```

### 小程序页面结构
- `pages/index/` - 首页，欢迎横幅+市场概况+今日推荐
- `pages/stocks/` - 选股页面，筛选面板完全隐藏/展开切换
- UI特色：渐变背景、emoji图标、动效、现代化卡片、玻璃拟态
- 关键组件：market-dashboard、recommend-tabs、stock-avatar、filters-panel

### TabBar交互增强
- 选中状态：字体加粗、颜色变蓝紫、轻微放大、底部指示线
- 动画过渡：0.25s缓动，指示器从0宽度展开
- 视觉层次：选中项带品牌色阴影

### 数据更新工作流
1. 运行 `cd data_processor && python3 main.py` 生成最新数据
2. JSON文件同时输出到 `static_data/` 和项目根目录
3. 提交并推送到GitHub，触发Pages自动部署
4. 小程序下次启动时自动获取最新数据

### OCR处理工作流（处理手写笔记）
1. 将手写笔记图片放入 `investnotebook/` 目录（支持68-94序号命名）
2. 运行 `python complete_ocr_processor.py` 进行完整OCR处理
3. 使用多种OCR方法验证：qwen-vl-max, qwen-vl-ocr, optimized-prompt
4. 运行 `python extract_quotes.py` 提取投资金句并生成JSON数据
5. 金句数据自动更新到 `static_data/laoliu_quotes.json`

### 投资金句功能架构
- **数据结构**: 17条精选金句，分为3大类别（投资大师🎯/投资策略📈/市场哲学💭）
- **每日轮换**: 基于日期的算法自动轮换首页展示金句
- **分享功能**: Canvas生成精美分享卡片，包含渐变背景和品牌标识
- **版本管理**: 支持金句数据版本检查和自动更新

### 小程序错误处理机制
- 网络请求包含自动重试（默认2次）
- 本地缓存策略（1小时过期）
- 降级显示和用户友好的错误提示
- 请求超时和网络异常的分类处理

### API接口配置
```javascript
// miniprogram/app.js
apiBaseUrl: 'https://vileo06.github.io/investliu'
// 所有API请求自动添加此前缀
```

## 关键配置信息

### 小程序配置
- **AppID**: wx2aad9cd988058c1f
- **项目名称**: 老刘投资决策
- **API基地址**: https://vileo06.github.io/investliu/

### GitHub Pages配置
- **仓库**: ViLeo06/investliu
- **部署分支**: master
- **访问地址**: https://vileo06.github.io/investliu/

## 重要开发注意事项

### 数据结构依赖
- 修改数据结构时需同步更新小程序页面逻辑
- JSON数据字段变更需检查所有页面的数据绑定
- 新增API接口需更新 `miniprogram_config.json` 配置

### 投资分析算法调整
- 估值标准在 `stock_analyzer.py` 中的 `valuation_criteria` 配置
- 行业权重可通过 `industry_weights` 调整
- 推荐等级映射: strong_buy/buy/hold/sell/strong_sell

### 调试和故障排除
```bash
# 检查Python数据生成
cd data_processor && python3 -c "import main; print('模块导入成功')"

# 验证JSON数据格式
python3 -m json.tool summary.json > /dev/null && echo "JSON格式正确"

# 检查小程序文件结构
find miniprogram/pages -name "*.wxml" -o -name "*.wxss" -o -name "*.js"

# GitHub Pages数据可访问性测试
curl -f https://vileo06.github.io/investliu/summary.json || echo "数据访问失败"
```

### 常见问题解决
- **OCR处理失败**: 检查阿里云API密钥配置，确保qwen-vl模型调用权限正常
- **金句数据不显示**: 验证`static_data/laoliu_quotes.json`文件格式，检查版本管理逻辑
- **UI样式异常**: 检查`app.wxss`和页面级wxss中的渐变和动画CSS
- **TabBar样式不生效**: 确认`app.json`中tabBar配置和`app.wxss`中wx-tab-bar覆盖样式
- **筛选面板显示问题**: 验证`filters-panel.show`类的opacity/visibility/padding组合
- **数据加载失败**: 验证网络请求重试机制在`app.js`中正确配置
- **股票评分显示错误**: 确认`stock_analyzer.py`中的评分算法逻辑
- **页面动画不生效**: 检查CSS动画keyframes和animation类是否正确应用
- **按钮文字不显示**: 确认WXML中使用`<view>`而非`<text>`作为按钮容器
- **Canvas分享卡片生成失败**: 检查`utils/shareCard.js`中Canvas API调用和图片绘制权限

### 部署验证
- 发布前必须验证所有JSON文件格式正确性
- 使用 `docs/release_checklist.md` 进行发布前检查
- 运行验证脚本确保所有组件就位

### 小程序开发规范
- 遵循微信小程序原生开发规范
- 错误处理统一使用app.js中的request方法
- UI组件使用统一的样式系统（app.wxss）

## 成本控制模式
- **GitHub Pages**: 免费托管
- **微信小程序**: 免费开发（认证费300元/年）
- **股票数据**: 当前使用模拟数据，实际部署需免费API
- **总运维成本**: ≈300元/年

## 金融合规要求
1. 微信小程序金融类需要相应资质认证
2. 投资建议必须包含免责声明
3. 数据准确性和时效性要求较高
4. 用户隐私保护符合相关法规

## 项目当前状态（2025年8月）
### ✅ 已完成功能
- Python数据处理管道和四维分析模型
- 完整OCR处理管道（27张投资笔记图片，多方法验证）
- 投资金句功能完整实现（17条精选金句，3大分类，分享功能）
- 微信小程序完整UI（现代化设计）
- quote-card组件和Canvas分享卡片生成器
- GitHub Pages静态托管
- 错误处理和重试机制
- 全面UI美化（渐变、动画、emoji图标）
- TabBar现代化交互（选中放大、指示器、毛玻璃效果）
- 筛选面板完美隐藏/展开机制
- 按钮和推荐标签显示优化
- 每日金句轮换和版本管理系统

### 🔄 技术债务
- 当前使用模拟数据，待集成真实股票API
- OCR密钥管理需要环境变量化（目前硬编码在脚本中）
- 需要微信小程序金融类资质认证
- 可考虑添加更多技术指标
- Canvas分享功能在部分设备上性能待优化

### 📋 发布准备
- 核心功能完整，可直接发布
- UI设计现代化，用户体验优秀
- 使用`docs/release_checklist.md`验证发布条件
- TabBar和页面交互效果已完善