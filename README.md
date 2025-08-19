# 老刘投资决策程序

> 基于个人投资者老刘多年投资笔记的股票投资决策辅助系统

## 📋 项目简介

本项目旨在将个人投资者老刘10万字的手写投资笔记数字化，提炼出投资决策规则，开发一个专注于中长线投资的股票分析程序，最终通过微信小程序为用户提供选股、择时和仓位管理建议。

## 🎯 核心功能

- **智能选股**: 基于价值投资理念筛选A股和港股
- **择时建议**: 结合技术指标和市场情绪给出买卖时机
- **仓位管理**: 提供风险控制和资金配置建议
- **投资记录**: 追踪决策过程和投资逻辑

## 🏗️ 技术架构

### 系统架构
```
手写笔记 → OCR识别 → 规则提取 → 本地脚本 → 静态JSON → 微信小程序
```

### 技术栈
- **数据处理**: Python + pandas
- **OCR识别**: 百度OCR API / 腾讯OCR API  
- **数据存储**: 静态JSON文件
- **文件托管**: GitHub Pages (免费)
- **前端展示**: 微信小程序原生开发
- **股票数据**: 免费API (新浪财经/东方财富)

## 📁 项目结构

```
investliu/
├── data_processor/          # 本地数据处理脚本
│   ├── ocr_processor.py     # OCR识别处理
│   ├── rule_extractor.py    # 投资规则提取
│   ├── stock_analyzer.py    # 股票分析脚本
│   └── data_generator.py    # JSON数据生成
├── static_data/             # 静态数据文件
│   ├── stocks_a.json        # A股推荐数据
│   ├── stocks_hk.json       # 港股推荐数据
│   ├── timing.json          # 择时建议
│   └── rules.json           # 投资规则库
├── miniprogram/             # 微信小程序代码
│   ├── pages/               # 页面文件
│   ├── components/          # 组件文件
│   └── utils/               # 工具函数
├── notes/                   # 原始笔记文件
└── docs/                    # 项目文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 微信开发者工具
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/ViLeo06/investliu.git
cd investliu
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **配置API密钥**
```bash
cp config.example.py config.py
# 编辑config.py添加OCR和股票API密钥
```

4. **运行数据处理脚本**
```bash
python data_processor/main.py
```

5. **部署静态文件**
```bash
# 将static_data/目录上传到GitHub Pages
git add static_data/
git commit -m "update stock data"
git push
```

## 📱 小程序功能

### 主要页面
- **首页**: 今日推荐股票和大盘状态
- **选股**: A股和港股推荐列表
- **分析**: 个股详细分析页面  
- **设置**: 风险偏好和通知设置

### 核心特性
- 📊 实时股票数据展示
- 🎯 基于老刘经验的选股建议
- ⏰ 买卖时机提醒
- 📈 投资组合追踪
- 💡 决策逻辑透明化

## 🔄 数据更新流程

1. **每日数据更新**: 运行本地Python脚本
2. **自动生成**: 创建最新的JSON数据文件
3. **文件上传**: 推送到GitHub Pages
4. **小程序刷新**: 自动获取最新推荐数据

## 📊 投资策略

### 选股标准 (基于老刘笔记)
- 估值指标: PE、PB、PEG
- 财务指标: ROE、负债率、现金流
- 成长性: 营收增长、利润增长
- 行业地位: 市场份额、竞争优势

### 择时信号
- 技术指标: 均线、MACD、RSI
- 市场情绪: 成交量、涨跌比例
- 宏观环境: 政策导向、经济数据

### 风险控制
- 分散投资: 行业配置、个股权重
- 止损策略: 动态止损、定期检查
- 仓位管理: 根据市场环境调整

## 🛠️ 开发计划

- [x] 需求分析和技术方案设计
- [ ] 笔记OCR识别和内容整理
- [ ] 投资规则提取和数字化
- [ ] 本地数据处理脚本开发
- [ ] 股票分析算法实现
- [ ] 静态文件托管配置
- [ ] 微信小程序界面开发
- [ ] 功能测试和优化
- [ ] 上线部署和维护

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests 来改进这个项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱: [your-email@example.com]
- 微信: [your-wechat-id]

---

**免责声明**: 本系统仅供投资参考，不构成投资建议。投资有风险，入市需谨慎。