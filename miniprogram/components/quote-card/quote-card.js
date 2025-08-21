// 投资金句卡片组件
const ShareCardGenerator = require('../../utils/shareCard.js');

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    quote: {
      type: Object,
      value: {}
    },
    showShare: {
      type: Boolean,
      value: true
    },
    cardStyle: {
      type: String,
      value: 'default' // default, compact, detailed
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    gradients: {
      'masters': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      'strategy': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
      'philosophy': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    },
    showShareModal: false,
    shareImagePath: ''
  },

  /**
   * 组件的方法列表
   */
  methods: {
    // 分享金句
    onShareQuote() {
      const quote = this.data.quote;
      
      // 显示分享选项
      wx.showActionSheet({
        itemList: ['生成分享图片', '复制文字内容'],
        success: (res) => {
          if (res.tapIndex === 0) {
            this.generateShareImage();
          } else if (res.tapIndex === 1) {
            this.copyQuoteText();
          }
        }
      });
      
      // 触发分享事件
      this.triggerEvent('share', {
        quote: quote,
        type: 'button'
      });
    },

    // 生成分享图片
    generateShareImage() {
      const quote = this.data.quote;
      
      wx.showLoading({
        title: '生成分享图片...',
        mask: true
      });

      // 设置分享模态框显示，包含Canvas
      this.setData({
        showShareModal: true
      });

      // 等待DOM渲染完成后生成图片
      setTimeout(() => {
        const shareCard = new ShareCardGenerator();
        shareCard.generateQuoteCard(quote, (imagePath) => {
          wx.hideLoading();
          
          if (imagePath) {
            this.setData({
              shareImagePath: imagePath
            });
            
            // 预览分享图片
            wx.previewImage({
              urls: [imagePath],
              success: () => {
                // 用户可以长按保存或分享
                wx.showToast({
                  title: '长按图片保存或分享',
                  icon: 'none',
                  duration: 2000
                });
              }
            });
          } else {
            wx.showToast({
              title: '生成分享图片失败',
              icon: 'error'
            });
          }
          
          // 隐藏分享模态框
          this.setData({
            showShareModal: false
          });
        });
      }, 100);
    },

    // 复制文字内容
    copyQuoteText() {
      const quote = this.data.quote;
      const shareContent = `💎 ${quote.content}\n\n— ${quote.author}\n\n来自老刘投资笔记`;
      
      wx.setClipboardData({
        data: shareContent,
        success: () => {
          wx.showToast({
            title: '已复制到剪贴板',
            icon: 'success'
          });
        }
      });
    },

    // 点击卡片
    onCardTap() {
      this.triggerEvent('tap', {
        quote: this.data.quote
      });
      
      // 添加点击动画效果
      this.setData({
        clicking: true
      });
      
      setTimeout(() => {
        this.setData({
          clicking: false
        });
      }, 200);
    },

    // 关闭分享模态框
    closeShareModal() {
      this.setData({
        showShareModal: false
      });
    },

    // 获取分类图标
    getCategoryIcon(category) {
      const icons = {
        'masters': '🎯',
        'strategy': '📈', 
        'philosophy': '💭'
      };
      return icons[category] || '💡';
    },

    // 获取分类名称
    getCategoryName(category) {
      const names = {
        'masters': '投资大师',
        'strategy': '投资策略',
        'philosophy': '市场哲学'
      };
      return names[category] || '投资智慧';
    }
  },

  /**
   * 组件生命周期
   */
  lifetimes: {
    attached() {
      // 组件初始化
      console.log('Quote card attached:', this.data.quote.id);
    }
  }
});