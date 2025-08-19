# 配置文件示例
# 复制此文件为 config.py 并填入你的API密钥

# 百度OCR API配置
BAIDU_OCR_APP_ID = "your_app_id"
BAIDU_OCR_API_KEY = "your_api_key" 
BAIDU_OCR_SECRET_KEY = "your_secret_key"

# 腾讯OCR API配置（可选）
TENCENT_SECRET_ID = "your_secret_id"
TENCENT_SECRET_KEY = "your_secret_key"
TENCENT_REGION = "ap-beijing"

# 股票数据API配置
SINA_API_BASE = "https://hq.sinajs.cn/list="
EASTMONEY_API_BASE = "https://push2.eastmoney.com/api/qt/clist/get"

# GitHub Pages配置
GITHUB_USERNAME = "your_username"
GITHUB_REPO = "investliu"
GITHUB_TOKEN = "your_token"  # 用于自动提交

# 数据更新配置
UPDATE_INTERVAL = 24  # 小时
MAX_RECOMMEND_STOCKS = 10  # 每次推荐股票数量

# 投资参数配置
MIN_MARKET_CAP = 50  # 最小市值（亿元）
MAX_PE_RATIO = 30    # 最大市盈率
MIN_ROE = 0.1        # 最小净资产收益率
MAX_DEBT_RATIO = 0.6 # 最大负债率