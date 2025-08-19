// 首页逻辑
const app = getApp()

Page({
  data: {
    loading: true,
    error: '',
    currentTab: 0,
    summary: {
      market_status: {},
      recommendations_count: {
        a_stocks: 0,
        hk_stocks: 0,
        total: 0
      },
      top_picks: {
        a_stocks: [],
        hk_stocks: []
      },
      portfolio_risk: 'medium',
      investment_suggestions: []
    },
    marketData: {
      sentiment: 'neutral',
      position: '5',
      signals: [],
      update_time: ''
    }
  },

  onLoad: function(options) {
    console.log('首页加载')
    this.loadData()
  },

  onShow: function() {
    // 检查是否需要刷新数据
    const lastUpdate = wx.getStorageSync('last_data_update')
    const now = Date.now()
    
    // 如果超过1小时，重新加载数据
    if (!lastUpdate || (now - lastUpdate) > 3600000) {
      this.loadData()
    }
  },

  onPullDownRefresh: function() {
    console.log('下拉刷新')
    this.loadData().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 加载数据
  loadData: function() {
    this.setData({ 
      loading: true, 
      error: '' 
    })

    return Promise.all([
      this.loadSummaryData(),
      this.loadMarketTiming()
    ]).then(() => {
      this.setData({ loading: false })
      // 记录更新时间
      wx.setStorageSync('last_data_update', Date.now())
    }).catch(err => {
      console.error('加载数据失败:', err)
      this.setData({ 
        loading: false,
        error: '数据加载失败，请检查网络连接'
      })
    })
  },

  // 加载汇总数据
  loadSummaryData: function() {
    // 先尝试从缓存加载
    const cachedData = app.getCache('summary_data')
    if (cachedData) {
      this.setData({ summary: cachedData })
    }

    return app.request({
      url: '/summary.json',
      showLoading: false
    }).then(data => {
      if (data) {
        this.setData({ summary: data })
        // 缓存数据
        app.setCache('summary_data', data)
      }
    })
  },

  // 加载市场择时数据
  loadMarketTiming: function() {
    // 先尝试从缓存加载
    const cachedData = app.getCache('market_timing')
    if (cachedData) {
      this.updateMarketData(cachedData)
    }

    return app.request({
      url: '/market_timing.json',
      showLoading: false
    }).then(data => {
      if (data) {
        this.updateMarketData(data)
        // 缓存数据
        app.setCache('market_timing', data)
      }
    })
  },

  // 更新市场数据
  updateMarketData: function(data) {
    const position = Math.round((data.recommended_position || 0.5) * 10)
    
    this.setData({
      marketData: {
        sentiment: data.market_sentiment || 'neutral',
        position: position.toString(),
        signals: data.signals || [],
        update_time: data.analysis_time || ''
      }
    })
  },

  // 切换标签
  switchTab: function(e) {
    const tab = parseInt(e.currentTarget.dataset.tab)
    this.setData({ currentTab: tab })
  },

  // 查看股票详情
  viewStock: function(e) {
    const stock = e.currentTarget.dataset.stock
    if (!stock) return

    wx.navigateTo({
      url: `/pages/analysis/analysis?code=${stock.code}&name=${stock.name}`
    })
  },

  // 查看更多股票
  viewMoreStocks: function() {
    wx.switchTab({
      url: '/pages/stocks/stocks'
    })
  },

  // 获取推荐等级的样式类
  getRecommendationClass: function(recommendation) {
    const classMap = {
      'strong_buy': 'rec-strong-buy',
      'buy': 'rec-buy', 
      'hold': 'rec-hold',
      'sell': 'rec-sell',
      'strong_sell': 'rec-strong-sell'
    }
    return classMap[recommendation] || 'rec-hold'
  },

  // 获取推荐等级的文本
  getRecommendationText: function(recommendation) {
    const textMap = {
      'strong_buy': '强烈买入',
      'buy': '买入',
      'hold': '持有',
      'sell': '卖出', 
      'strong_sell': '强烈卖出'
    }
    return textMap[recommendation] || '持有'
  },

  // 分享功能
  onShareAppMessage: function() {
    return {
      title: '老刘投资决策 - 今日股票推荐',
      path: '/pages/index/index',
      imageUrl: '' // 可以设置分享图片
    }
  }
})