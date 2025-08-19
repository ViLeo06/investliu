Page({
  data: {
    stockList: [],
    selectedMarket: 'a', // 'a' for A股, 'hk' for 港股
    loading: false,
    refreshing: false,
    filters: {
      minPrice: '',
      maxPrice: '', 
      minPE: '',
      maxPE: '',
      minROE: '',
      industry: ''
    },
    showFilters: false
  },

  onLoad: function (options) {
    console.log('选股页面加载')
    this.loadStockData()
  },

  onShow: function () {
    // 页面显示时检查是否需要刷新数据
    const lastUpdate = wx.getStorageSync('stocks_last_update')
    const now = Date.now()
    if (!lastUpdate || now - lastUpdate > 300000) { // 5分钟
      this.loadStockData()
    }
  },

  onPullDownRefresh: function () {
    this.refreshData()
  },

  onReachBottom: function () {
    // 加载更多数据
    this.loadMoreData()
  },

  // 切换市场
  switchMarket: function(e) {
    const market = e.currentTarget.dataset.market
    if (market === this.data.selectedMarket) return
    
    this.setData({
      selectedMarket: market,
      stockList: []
    })
    this.loadStockData()
  },

  // 加载股票数据
  loadStockData: function() {
    const self = this
    self.setData({ loading: true })

    const app = getApp()
    const url = self.data.selectedMarket === 'a' ? '/stocks_a.json' : '/stocks_hk.json'
    
    app.request({
      url: url,
      showLoading: false
    }).then(data => {
      console.log('股票数据加载成功:', data)
      
      self.setData({
        stockList: data.stocks || [],
        loading: false
      })
      
      // 缓存数据
      app.setCache(`stocks_${self.data.selectedMarket}`, data.stocks || [])
      wx.setStorageSync('stocks_last_update', Date.now())
      
    }).catch(err => {
      console.error('加载股票数据失败:', err)
      
      // 尝试加载缓存数据
      const cachedData = app.getCache(`stocks_${self.data.selectedMarket}`)
      if (cachedData) {
        self.setData({
          stockList: cachedData,
          loading: false
        })
        wx.showToast({
          title: '显示缓存数据',
          icon: 'none'
        })
      } else {
        self.setData({ loading: false })
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        })
      }
    })
  },

  // 刷新数据
  refreshData: function() {
    this.setData({ refreshing: true })
    this.loadStockData()
    
    setTimeout(() => {
      this.setData({ refreshing: false })
      wx.stopPullDownRefresh()
    }, 1000)
  },

  // 加载更多数据
  loadMoreData: function() {
    // 如果需要分页加载，在这里实现
    console.log('加载更多数据')
  },

  // 显示/隐藏筛选条件
  toggleFilters: function() {
    this.setData({
      showFilters: !this.data.showFilters
    })
  },

  // 筛选输入
  onFilterInput: function(e) {
    const field = e.currentTarget.dataset.field
    const value = e.detail.value
    const filters = this.data.filters
    filters[field] = value
    
    this.setData({
      [`filters.${field}`]: value
    })
  },

  // 应用筛选
  applyFilters: function() {
    // 实现筛选逻辑
    console.log('应用筛选条件:', this.data.filters)
    this.setData({
      showFilters: false
    })
    // 这里可以添加筛选逻辑
  },

  // 清空筛选
  clearFilters: function() {
    this.setData({
      filters: {
        minPrice: '',
        maxPrice: '', 
        minPE: '',
        maxPE: '',
        minROE: '',
        industry: ''
      }
    })
  },

  // 查看股票详情
  viewStockDetail: function(e) {
    const stock = e.currentTarget.dataset.stock
    wx.navigateTo({
      url: `/pages/analysis/analysis?code=${stock.code}&market=${this.data.selectedMarket}`
    })
  },

  // 获取推荐等级样式
  getRecommendationClass: function(level) {
    switch(level) {
      case '强烈推荐': return 'rec-strong-buy'
      case '推荐': return 'rec-buy' 
      case '持有': return 'rec-hold'
      case '卖出': return 'rec-sell'
      case '强烈卖出': return 'rec-strong-sell'
      default: return 'rec-hold'
    }
  },

  // 获取评分样式
  getScoreClass: function(score) {
    if (score >= 80) return 'score-high'
    if (score >= 60) return 'score-medium'
    return 'score-low'
  }
})