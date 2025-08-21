// 分享卡片工具类
class ShareCardGenerator {
  
  constructor() {
    this.canvas = null;
    this.ctx = null;
  }

  // 生成分享卡片
  generateQuoteCard(quote, callback) {
    const that = this;
    
    // 创建Canvas查询
    const query = wx.createSelectorQuery();
    query.select('#shareCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        if (res[0]) {
          const canvas = res[0].node;
          const ctx = canvas.getContext('2d');
          
          that.canvas = canvas;
          that.ctx = ctx;
          
          // 设置Canvas尺寸
          const dpr = wx.getSystemInfoSync().pixelRatio;
          canvas.width = 750 * dpr;
          canvas.height = 1000 * dpr;
          ctx.scale(dpr, dpr);
          
          // 绘制卡片
          that.drawQuoteCard(quote, callback);
        }
      });
  }

  // 绘制金句卡片
  drawQuoteCard(quote, callback) {
    const ctx = this.ctx;
    const canvas = this.canvas;
    
    // 背景渐变
    const gradient = ctx.createLinearGradient(0, 0, 750, 1000);
    const gradientColors = this.getGradientColors(quote.category);
    gradient.addColorStop(0, gradientColors.start);
    gradient.addColorStop(1, gradientColors.end);
    
    // 绘制背景
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 750, 1000);
    
    // 绘制装饰图案
    this.drawDecorations(ctx);
    
    // 绘制内容
    this.drawContent(ctx, quote);
    
    // 绘制底部信息
    this.drawFooter(ctx);
    
    // 生成图片
    setTimeout(() => {
      wx.canvasToTempFilePath({
        canvas: canvas,
        success: (res) => {
          console.log('分享卡片生成成功:', res.tempFilePath);
          callback && callback(res.tempFilePath);
        },
        fail: (err) => {
          console.error('分享卡片生成失败:', err);
          callback && callback(null);
        }
      });
    }, 500);
  }

  // 获取渐变色
  getGradientColors(category) {
    const colorMap = {
      'masters': { start: '#667eea', end: '#764ba2' },
      'strategy': { start: '#f093fb', end: '#f5576c' },
      'philosophy': { start: '#4facfe', end: '#00f2fe' }
    };
    return colorMap[category] || colorMap.masters;
  }

  // 绘制装饰
  drawDecorations(ctx) {
    // 设置透明度
    ctx.globalAlpha = 0.1;
    
    // 绘制圆形装饰
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(650, 100, 80, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(100, 850, 60, 0, Math.PI * 2);
    ctx.fill();
    
    // 绘制线条装饰
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, 950);
    ctx.lineTo(750, 950);
    ctx.stroke();
    
    // 恢复透明度
    ctx.globalAlpha = 1;
  }

  // 绘制内容
  drawContent(ctx, quote) {
    // 分类标签
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    
    const categoryText = this.getCategoryText(quote.category);
    ctx.fillText(categoryText, 375, 150);
    
    // 金句内容
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 36px sans-serif';
    ctx.textAlign = 'center';
    
    // 文字换行处理
    const maxWidth = 650;
    const lines = this.wrapText(ctx, quote.content, maxWidth);
    const lineHeight = 60;
    const startY = 300;
    
    lines.forEach((line, index) => {
      ctx.fillText(line, 375, startY + (index * lineHeight));
    });
    
    // 作者
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = '28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`— ${quote.author}`, 375, startY + (lines.length * lineHeight) + 80);
  }

  // 绘制底部信息
  drawFooter(ctx) {
    // 来源信息
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = '24px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('来自老刘投资笔记', 375, 900);
    
    // 小程序码位置（如果有的话）
    // 这里可以绘制小程序码
  }

  // 文字换行
  wrapText(ctx, text, maxWidth) {
    const words = text.split('');
    const lines = [];
    let currentLine = '';

    for (let i = 0; i < words.length; i++) {
      const testLine = currentLine + words[i];
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;
      
      if (testWidth > maxWidth && i > 0) {
        lines.push(currentLine);
        currentLine = words[i];
      } else {
        currentLine = testLine;
      }
    }
    lines.push(currentLine);
    return lines;
  }

  // 获取分类文本
  getCategoryText(category) {
    const textMap = {
      'masters': '🎯 投资大师',
      'strategy': '📈 投资策略',
      'philosophy': '💭 市场哲学'
    };
    return textMap[category] || '💡 投资智慧';
  }
}

// 导出工具类
module.exports = ShareCardGenerator;