Page({
  data: {
    stockList: [],
    filteredStockList: [], // 筛选后的股票列表
    allStocks: [], // 所有股票数据
    selectedMarket: 'a', // 'a' for A股, 'hk' for 港股
    loading: false,
    refreshing: false,
    searchKeyword: '', // 搜索关键词
    filters: {
      minPrice: '',
      maxPrice: '', 
      minPE: '',
      maxPE: '',
      minROE: '',
      industry: '',
      recommendation: '', // 推荐等级筛选
      minScore: '' // 最低评分
    },
    showFilters: false,
    industries: [], // 行业列表
    industryOptions: ['全部'], // 行业选择器选项
    recommendationOptions: ['全部', 'strong_buy', '推荐', '持有', '卖出'], // 推荐等级选项
    totalCount: 0, // 总股票数
    filteredCount: 0 // 筛选后数量
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
      
      // 预处理数据，添加显示所需的字段
      const processedStocks = (data.stocks || []).map(stock => {
        return {
          ...stock,
          displayPrice: stock.current_price,
          displayChange: stock.change_percent,
          displayScore: Math.round((stock.total_score || stock.laoliu_score / 100) * 100),
          displayRecommendation: self.getRecommendationText(stock.recommendation),
          recommendationClass: self.getRecommendationClass(stock.recommendation),
          scoreClass: self.getScoreClass(Math.round((stock.total_score || stock.laoliu_score / 100) * 100)),
          changeClass: stock.change_percent >= 0 ? 'text-red' : 'text-green'
        }
      })
      
      // 提取行业列表
      const industries = [...new Set(processedStocks.map(stock => stock.industry).filter(Boolean))]
      const industryOptions = ['全部', ...industries]
      
      self.setData({
        allStocks: processedStocks,
        stockList: processedStocks.slice(0, 50), // 初始显示前50只
        filteredStockList: processedStocks,
        industries: industries,
        industryOptions: industryOptions,
        totalCount: processedStocks.length,
        filteredCount: processedStocks.length,
        loading: false
      })
      
      // 缓存数据
      app.setCache(`stocks_${self.data.selectedMarket}`, processedStocks)
      wx.setStorageSync('stocks_last_update', Date.now())
      
    }).catch(err => {
      console.error('加载股票数据失败:', err)
      
      // 尝试加载缓存数据
      const cachedData = app.getCache(`stocks_${self.data.selectedMarket}`)
      if (cachedData) {
        const industries = [...new Set(cachedData.map(stock => stock.industry).filter(Boolean))]
        const industryOptions = ['全部', ...industries]
        self.setData({
          allStocks: cachedData,
          stockList: cachedData.slice(0, 50),
          filteredStockList: cachedData,
          industries: industries,
          industryOptions: industryOptions,
          totalCount: cachedData.length,
          filteredCount: cachedData.length,
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
    const currentList = this.data.stockList
    const filteredList = this.data.filteredStockList
    const nextBatch = filteredList.slice(currentList.length, currentList.length + 30)
    
    if (nextBatch.length > 0) {
      this.setData({
        stockList: [...currentList, ...nextBatch]
      })
      console.log(`加载更多股票，当前显示: ${this.data.stockList.length}/${filteredList.length}`)
    }
  },

  // 搜索股票
  onSearchInput: function(e) {
    const keyword = e.detail.value.trim()
    this.setData({
      searchKeyword: keyword
    })
    
    // 延迟搜索避免频繁触发
    clearTimeout(this.searchTimer)
    this.searchTimer = setTimeout(() => {
      this.performSearch()
    }, 300)
  },

  // 执行搜索
  performSearch: function() {
    const { searchKeyword, allStocks, filters } = this.data
    let filtered = [...allStocks]
    
    // 搜索过滤
    if (searchKeyword) {
      filtered = filtered.filter(stock => 
        stock.name.includes(searchKeyword) || 
        stock.code.includes(searchKeyword) ||
        (stock.industry && stock.industry.includes(searchKeyword))
      )
    }
    
    // 应用其他筛选条件
    filtered = this.applyFiltersToList(filtered, filters)
    
    this.setData({
      filteredStockList: filtered,
      stockList: filtered.slice(0, 50), // 重新显示前50只
      filteredCount: filtered.length
    })
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
    
    // 处理picker选择
    if (field === 'industry') {
      const selectedIndustry = this.data.industryOptions[value]
      const actualValue = selectedIndustry === '全部' ? '' : selectedIndustry
      this.setData({
        [`filters.${field}`]: actualValue
      })
    } else if (field === 'recommendation') {
      const selectedRecommendation = this.data.recommendationOptions[value] 
      const actualValue = selectedRecommendation === '全部' ? '' : selectedRecommendation
      this.setData({
        [`filters.${field}`]: actualValue
      })
    } else {
      // 处理普通input
      this.setData({
        [`filters.${field}`]: value
      })
    }
  },

  // 应用筛选
  applyFilters: function() {
    const { filters, allStocks, searchKeyword } = this.data
    let filtered = [...allStocks]
    
    // 先应用搜索
    if (searchKeyword) {
      filtered = filtered.filter(stock => 
        stock.name.includes(searchKeyword) || 
        stock.code.includes(searchKeyword) ||
        (stock.industry && stock.industry.includes(searchKeyword))
      )
    }
    
    // 应用筛选条件
    filtered = this.applyFiltersToList(filtered, filters)
    
    this.setData({
      filteredStockList: filtered,
      stockList: filtered.slice(0, 50),
      filteredCount: filtered.length,
      showFilters: false
    })
    
    console.log('筛选完成:', {
      原始数量: allStocks.length,
      筛选后: filtered.length,
      筛选条件: filters
    })
  },

  // 对股票列表应用筛选条件
  applyFiltersToList: function(stockList, filters) {
    return stockList.filter(stock => {
      // 价格筛选
      if (filters.minPrice && stock.current_price < parseFloat(filters.minPrice)) return false
      if (filters.maxPrice && stock.current_price > parseFloat(filters.maxPrice)) return false
      
      // PE筛选
      if (filters.minPE && stock.pe_ratio < parseFloat(filters.minPE)) return false
      if (filters.maxPE && stock.pe_ratio > parseFloat(filters.maxPE)) return false
      
      // ROE筛选
      if (filters.minROE && stock.roe < parseFloat(filters.minROE)) return false
      
      // 行业筛选
      if (filters.industry && stock.industry !== filters.industry) return false
      
      // 推荐等级筛选
      if (filters.recommendation && stock.recommendation !== filters.recommendation) return false
      
      // 评分筛选
      if (filters.minScore) {
        const score = stock.total_score ? Math.round(stock.total_score * 100) : stock.laoliu_score
        if (score < parseFloat(filters.minScore)) return false
      }
      
      return true
    })
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
        industry: '',
        recommendation: '',
        minScore: ''
      },
      searchKeyword: ''
    })
    
    // 重置为显示所有股票
    this.setData({
      filteredStockList: this.data.allStocks,
      stockList: this.data.allStocks.slice(0, 50),
      filteredCount: this.data.allStocks.length
    })
  },

  // 快速筛选
  quickFilter: function(e) {
    const type = e.currentTarget.dataset.type
    const { allStocks } = this.data
    let filtered = []
    
    switch(type) {
      case 'high_roe':
        filtered = allStocks.filter(stock => stock.roe >= 15)
        break
      case 'low_pe':
        filtered = allStocks.filter(stock => stock.pe_ratio <= 20)
        break
      case 'strong_buy':
        filtered = allStocks.filter(stock => stock.recommendation === 'strong_buy')
        break
      case 'high_score':
        filtered = allStocks.filter(stock => {
          const score = stock.total_score ? Math.round(stock.total_score * 100) : stock.laoliu_score
          return score >= 80
        })
        break
      default:
        filtered = allStocks
    }
    
    this.setData({
      filteredStockList: filtered,
      stockList: filtered.slice(0, 50),
      filteredCount: filtered.length
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
      case 'strong_buy': 
      case '强烈推荐': return 'rec-strong-buy'
      case 'buy':
      case '推荐': return 'rec-buy' 
      case 'hold':
      case '持有': return 'rec-hold'
      case 'sell':
      case '卖出': return 'rec-sell'
      case 'strong_sell':
      case '强烈卖出': return 'rec-strong-sell'
      default: return 'rec-hold'
    }
  },

  // 获取推荐文本
  getRecommendationText: function(level) {
    switch(level) {
      case 'strong_buy': return '强烈推荐'
      case 'buy': return '推荐'
      case 'hold': return '持有'
      case 'sell': return '卖出'
      case 'strong_sell': return '强烈卖出'
      default: return level || '持有'
    }
  },

  // 获取评分样式
  getScoreClass: function(score) {
    if (score >= 80) return 'score-high'
    if (score >= 60) return 'score-medium'
    return 'score-low'
  }
})