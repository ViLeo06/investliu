# GitHub Pages 部署指南

## 快速部署步骤

### 1. 创建 GitHub 仓库
```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始提交: 老刘投资决策系统"

# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/your-username/investliu.git

# 推送到 GitHub
git push -u origin main
```

### 2. 启用 GitHub Pages
1. 访问你的 GitHub 仓库页面
2. 点击 "Settings" 选项卡
3. 滚动到 "Pages" 部分
4. 在 "Source" 下选择 "Deploy from a branch"
5. 选择 "main" 分支，文件夹选择 "/ (root)"
6. 点击 "Save"

### 3. 配置 GitHub Actions 自动部署
创建 `.github/workflows/deploy.yml` 文件实现自动部署：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  schedule:
    # 每天北京时间9点运行（UTC时间1点）
    - cron: '0 1 * * *'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run data update
      env:
        BAIDU_OCR_APP_ID: ${{ secrets.BAIDU_OCR_APP_ID }}
        BAIDU_OCR_API_KEY: ${{ secrets.BAIDU_OCR_API_KEY }}
        BAIDU_OCR_SECRET_KEY: ${{ secrets.BAIDU_OCR_SECRET_KEY }}
      run: |
        python update_data.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./static_data
        publish_branch: gh-pages
```

### 4. 设置 GitHub Secrets
在 GitHub 仓库设置中添加以下 Secrets：
- `BAIDU_OCR_APP_ID`
- `BAIDU_OCR_API_KEY` 
- `BAIDU_OCR_SECRET_KEY`

### 5. 访问你的网站
部署完成后，你的数据将在以下地址可用：
```
https://your-username.github.io/investliu/
```

## 数据 API 端点

部署后，小程序可以通过以下端点获取数据：

```
# 汇总数据
https://your-username.github.io/investliu/summary.json

# 市场择时
https://your-username.github.io/investliu/market_timing.json

# A股推荐
https://your-username.github.io/investliu/stocks_a_recommendations.json

# 港股推荐
https://your-username.github.io/investliu/stocks_hk_recommendations.json

# 投资组合建议
https://your-username.github.io/investliu/portfolio_suggestion.json

# 小程序配置
https://your-username.github.io/investliu/miniprogram_config.json
```

## 自定义域名（可选）

如果你有自己的域名，可以在仓库根目录创建 `CNAME` 文件：
```
yourdomain.com
```

然后在域名提供商那里设置 CNAME 记录指向 `your-username.github.io`。

## 注意事项

1. **API 限制**: 免费 API 有调用频率限制，避免过于频繁的更新
2. **数据大小**: GitHub Pages 有 1GB 的存储限制
3. **HTTPS**: GitHub Pages 默认支持 HTTPS
4. **缓存**: 可以设置适当的缓存策略提高访问速度

## 本地测试

在部署前，可以本地测试数据生成：
```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp config.example.py config.py
# 编辑 config.py 文件

# 生成数据
python update_data.py

# 检查 static_data 目录
ls static_data/
```