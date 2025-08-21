# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 老刘投资决策程序 - Claude Code 项目记录

## 项目概述
基于个人投资者老刘多年投资笔记的股票决策辅助程序，以微信小程序形式呈现，专注中长线价值投资策略。

## 核心开发命令

### 数据处理命令
```bash
# 生成最新股票推荐数据（核心命令）
cd data_processor && python3 main.py

# 安装Python依赖
pip install -r requirements.txt

# 配置API密钥（首次运行需要）
cp config.example.py config.py
# 编辑config.py添加OCR和股票API密钥

# 验证生成的数据文件
ls -la *.json  # 检查根目录JSON文件
cat summary.json | head -20  # 验证数据格式
```

### 微信小程序开发
```bash
# 在微信开发者工具中打开miniprogram目录
# AppID: wx2aad9cd988058c1f
# 项目名称: 老刘投资决策

# 预览测试（在微信开发者工具中）
# 点击"预览" → 扫码真机测试

# 上传代码（在微信开发者工具中）
# 点击"上传" → 填写版本号

# 检查小程序页面样式
# 主要检查首页WXML/WXSS的现代化UI效果
```

### 部署命令
```bash
# 完整数据更新和部署流程
cd data_processor && python3 main.py  # 生成数据
cp static_data/*.json .  # 复制到根目录（如需要）
git add *.json static_data/
git commit -m "update stock data and UI improvements"
git push origin master

# 验证GitHub Pages部署
curl -I https://vileo06.github.io/investliu/summary.json
```

## 项目架构

### 核心设计理念
- **零服务器架构**: 使用GitHub Pages托管静态JSON数据
- **本地数据处理**: Python脚本生成投资建议
- **微信小程序**: 原生开发，直接读取静态数据
- **成本优化**: 完全免费的技术栈

### 高层架构概述

#### 数据流架构
```
手写笔记 → OCR识别 → 规则提取 → Python分析引擎 → JSON输出 → GitHub Pages → 微信小程序
```

#### 核心组件交互
1. **数据处理层** (`data_processor/`): 
   - `StockDataFetcher`: 获取股票基础数据（模拟API调用）
   - `StockAnalyzer`: 四维分析模型（估值25% + 成长25% + 盈利25% + 安全25%）
   - `RuleExtractor`: 基于老刘投资经验的规则引擎
   - `DataGenerator`: 协调所有组件生成最终JSON文件

2. **静态数据层** (根目录JSON文件):
   - `summary.json`: 汇总数据和今日推荐
   - `stocks_a.json/stocks_hk.json`: A股/港股详细推荐
   - `market_timing.json`: 择时建议和市场情绪
   - `miniprogram_config.json`: 小程序运行时配置

3. **小程序前端** (`miniprogram/`):
   - `app.js`: 全局配置，包含重试机制的API请求封装
   - 5个核心页面：首页、选股、分析、组合、设置
   - 缓存策略：1小时本地缓存，自动刷新机制

#### 投资分析算法核心
```python
# 四维评分模型（stock_analyzer.py中实现）
total_score = (valuation_score * 0.25 + 
               growth_score * 0.25 + 
               profitability_score * 0.25 + 
               safety_score * 0.25) * industry_weight
```

基于财务指标: PE、PB、ROE、负债率，结合行业比较和市场环境调整。

### 技术栈
- **数据处理**: Python 3.8+ (pandas, requests, akshare, baidu-aip, tencentcloud-sdk-python)
- **数据存储**: 静态JSON文件托管在GitHub Pages
- **前端**: 微信小程序原生开发
- **API数据源**: 免费股票API (当前使用模拟数据)

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
- **UI样式异常**: 检查`app.wxss`和页面级wxss中的渐变和动画CSS
- **TabBar样式不生效**: 确认`app.json`中tabBar配置和`app.wxss`中wx-tab-bar覆盖样式
- **筛选面板显示问题**: 验证`filters-panel.show`类的opacity/visibility/padding组合
- **数据加载失败**: 验证网络请求重试机制在`app.js`中正确配置
- **股票评分显示错误**: 确认`stock_analyzer.py`中的评分算法逻辑
- **页面动画不生效**: 检查CSS动画keyframes和animation类是否正确应用
- **按钮文字不显示**: 确认WXML中使用`<view>`而非`<text>`作为按钮容器

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
- 微信小程序完整UI（现代化设计）
- GitHub Pages静态托管
- 错误处理和重试机制
- 全面UI美化（渐变、动画、emoji图标）
- TabBar现代化交互（选中放大、指示器、毛玻璃效果）
- 筛选面板完美隐藏/展开机制
- 按钮和推荐标签显示优化

### 🔄 技术债务
- 当前使用模拟数据，待集成真实股票API
- 需要微信小程序金融类资质认证
- 可考虑添加更多技术指标

### 📋 发布准备
- 核心功能完整，可直接发布
- UI设计现代化，用户体验优秀
- 使用`docs/release_checklist.md`验证发布条件
- TabBar和页面交互效果已完善