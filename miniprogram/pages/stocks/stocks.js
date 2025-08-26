Page({
  data: {
    // 数据状态
    loading: false,
    refreshing: false,
    error: false,
    
    // 市场数据
    selectedMarket: 'a',  // 'a' 或 'hk'
    stockList: [],
    totalCount: 0,
    filteredCount: 0,
    
    // 搜索功能
    searchKeyword: '',
    
    // 筛选
    showFilters: false,
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
    
    // 筛选选项
    industryOptions: ['全部', '银行', '科技', '消费', '医药', '制造业', '房地产', '能源'],
    recommendationOptions: ['全部', '强烈买入', '买入', '持有', '卖出']
  },

  onLoad: function(options) {
    this.loadStockData()
    this.loadSearchHistory()
    this.loadSearchIndex()
  },

  // 搜索输入
  onSearchInput: function(e) {
    const keyword = e.detail.value.trim()
    this.setData({ searchKeyword: keyword })
    
    if (keyword.length > 0) {
      this.performLocalSearch(keyword)
    } else {
      // 恢复原始列表
      this.loadStockData()
    }
  },

  // 本地搜索
  performLocalSearch: function(keyword) {
    if (!this.data.stockList || this.data.stockList.length === 0) {
      return
    }
    
    const results = this.data.stockList.filter(stock => {
      const keywordLower = keyword.toLowerCase()
      return stock.code.toLowerCase().includes(keywordLower) ||
             stock.name.toLowerCase().includes(keywordLower) ||
             (stock.industry && stock.industry.toLowerCase().includes(keywordLower))
    })
    
    this.setData({
      stockList: results,
      filteredCount: results.length
    })
  },

  // 快速筛选
  quickFilter: function(e) {
    const type = e.currentTarget.dataset.type
    
    if (!this.data.stockList || this.data.stockList.length === 0) {
      wx.showToast({
        title: '请先导入股票数据',
        icon: 'none'
      })
      return
    }
    
    let filtered = [...this.data.stockList]
    let filterName = ''
    
    switch (type) {
      case 'high_roe':
        filtered = filtered.filter(stock => (stock.roe || 0) >= 15)
        filterName = '高ROE (≥15%)'
        break
      case 'low_pe':
        filtered = filtered.filter(stock => stock.pe_ratio && stock.pe_ratio > 0 && stock.pe_ratio <= 20)
        filterName = '低估值 (PE≤20)'
        break
      case 'strong_buy':
        filtered = filtered.filter(stock => stock.recommendation === 'strong_buy' || stock.recommendation === 'buy')
        filterName = '强推股票'
        break
      case 'high_score':
        filtered = filtered.filter(stock => (stock.laoliu_score || stock.total_score || 0) >= 80)
        filterName = '高分股票 (≥80分)'
        break
    }
    
    this.setData({
      stockList: filtered,
      filteredCount: filtered.length
    })
    
    wx.showToast({
      title: `已筛选：${filterName}`,
      icon: 'none',
      duration: 2000
    })
  },

  // 筛选输入事件
  onFilterInput: function(e) {
    const field = e.currentTarget.dataset.field
    const value = e.detail.value
    const filters = { ...this.data.filters }
    filters[field] = value
    this.setData({ filters })
  },

  onSearchConfirm: function(e) {
    const query = e.detail.value.trim()
    if (query.length > 0) {
      this.addToSearchHistory(query)
      this.performSearch(query)
    }
  },

  onSearchFocus: function() {
    this.setData({ showSearchHistory: this.data.searchHistory.length > 0 })
  },

  onSearchBlur: function() {
    // 延迟隐藏搜索历史，确保点击历史项目能正常触发
    setTimeout(() => {
      this.setData({ showSearchHistory: false })
    }, 200)
  },

  performSearch: function(query) {
    if (!this.data.searchIndex) {
      this.searchInCurrentData(query)
      return
    }

    const results = []
    const queryLower = query.toLowerCase()
    
    // 在搜索索引中查找
    Object.values(this.data.searchIndex.stocks).forEach(stock => {
      let score = 0
      
      // 精确匹配股票代码
      if (stock.code === query || stock.code === query.toUpperCase()) {
        score += 100
      }
      // 模糊匹配股票代码
      else if (stock.code.toLowerCase().includes(queryLower)) {
        score += 80
      }
      
      // 精确匹配股票名称
      if (stock.name === query) {
        score += 90
      }
      // 模糊匹配股票名称
      else if (stock.name.toLowerCase().includes(queryLower)) {
        score += 70
      }
      
      // 匹配行业
      if (stock.industry && stock.industry.toLowerCase().includes(queryLower)) {
        score += 30
      }
      
      // 匹配关键词
      if (stock.keywords) {
        stock.keywords.forEach(keyword => {
          if (keyword.toLowerCase().includes(queryLower)) {
            score += 20
          }
        })
      }
      
      if (score > 0) {
        results.push({ ...stock, searchScore: score })
      }
    })

    // 按匹配度排序
    results.sort((a, b) => b.searchScore - a.searchScore)
    
    this.setData({ 
      searchResults: results.slice(0, 10), // 限制显示前10个结果
      showSearchHistory: false 
    })
  },

  searchInCurrentData: function(query) {
    // 在当前股票数据中搜索（备用方案）
    const results = this.data.stockList.filter(stock => {
      const queryLower = query.toLowerCase()
      return stock.code.toLowerCase().includes(queryLower) ||
             stock.name.toLowerCase().includes(queryLower) ||
             (stock.industry && stock.industry.toLowerCase().includes(queryLower))
    })
    
    this.setData({ 
      searchResults: results.slice(0, 10),
      showSearchHistory: false 
    })
  },

  // 搜索历史管理
  addToSearchHistory: function(query) {
    let history = this.data.searchHistory.filter(item => item !== query)
    history.unshift(query)
    history = history.slice(0, 10) // 只保留最近10个搜索
    
    this.setData({ searchHistory: history })
    this.saveSearchHistory(history)
  },

  loadSearchHistory: function() {
    try {
      const history = wx.getStorageSync('stock_search_history') || []
      this.setData({ searchHistory: history })
    } catch (e) {
      console.error('加载搜索历史失败:', e)
    }
  },

  saveSearchHistory: function(history) {
    try {
      wx.setStorageSync('stock_search_history', history)
    } catch (e) {
      console.error('保存搜索历史失败:', e)
    }
  },

  onHistoryItemTap: function(e) {
    const query = e.currentTarget.dataset.query
    this.setData({
      searchQuery: query,
      showSearchHistory: false 
    })
    this.performSearch(query)
    this.addToSearchHistory(query)
  },

  clearSearchHistory: function() {
    wx.showModal({
      title: '清空搜索历史',
      content: '确定要清空所有搜索历史吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ searchHistory: [] })
          this.saveSearchHistory([])
        }
      }
    })
  },

  // 股票数据加载
  loadSearchIndex: function() {
    const app = getApp()
    app.request('/stock_search_index.json', 'stock_search').then(data => {
      if (data) {
        this.setData({ searchIndex: data })
        console.log('搜索索引加载成功:', Object.keys(data.stocks).length + '只股票')
      }
    }).catch(err => {
      console.warn('搜索索引加载失败:', err)
    })
  },

  loadStockData: function(selectedMarket) {
    this.setData({ loading: true, error: false })
    
    const app = getApp()
    const market = selectedMarket || this.data.selectedMarket
    const dataUrl = market === 'a' ? '/stocks_a.json' : '/stocks_hk.json'
    const cacheKey = market === 'a' ? 'stocks_a' : 'stocks_hk'
    
    app.request(dataUrl, cacheKey).then(data => {
      console.log('股票数据加载成功:', data)
      
      if (data && data.stocks) {
        const processedStocks = this.processStockData(data.stocks)
        const stocks = processedStocks.slice(0, 100) // 限制显示数量
        
        this.setData({
          stockList: stocks,
          totalCount: data.stocks.length,
          filteredCount: stocks.length,
          loading: false,
          currentPage: 1,
          hasMore: data.stocks.length > 100
        })
      } else {
        throw new Error('股票数据为空')
      }
    }).catch(err => {
      console.error('加载股票数据失败:', err)
      this.setData({
        loading: false,
        error: true,
        errorMessage: '数据加载失败，请点击一键导入获取最新数据'
      })
    })
  },

  // 处理股票数据，添加显示属性
  processStockData: function(stocks) {
    return stocks.map(stock => ({
      ...stock,
      displayPrice: this.formatPrice(stock.current_price),
      displayChange: this.formatNumber(stock.change_percent || 0, 2),
      displayScore: stock.laoliu_score || stock.total_score || 0,
      displayRecommendation: this.getRecommendationText(stock.recommendation),
      changeClass: this.getChangeClass(stock.change_percent || 0),
      scoreClass: this.getScoreClass(stock.laoliu_score || stock.total_score || 0),
      recommendationClass: this.getRecommendationClass(stock.recommendation)
    }))
  },

  // 格式化价格
  formatPrice: function(price) {
    if (!price || isNaN(price)) return '--'
    return Number(price).toFixed(2)
  },

  // 格式化数字
  formatNumber: function(num, decimals = 2) {
    if (num == null || isNaN(num)) return 0
    return Number(num).toFixed(decimals)
  },

  // 获取涨跌颜色类
  getChangeClass: function(change) {
    if (change > 0) return 'positive'
    if (change < 0) return 'negative'
    return 'neutral'
  },

  // 获取评分颜色类
  getScoreClass: function(score) {
    if (score >= 80) return 'score-high'
    if (score >= 60) return 'score-medium'
    return 'score-low'
  },

  // 获取推荐等级文本
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

  // 获取推荐等级样式类
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

  // 市场切换
  switchMarket: function(e) {
    const market = e.currentTarget.dataset.market
    if (market !== this.data.selectedMarket) {
      this.setData({
        selectedMarket: market,
        searchKeyword: '',
        stockList: [],
        totalCount: 0,
        filteredCount: 0
      })
      this.loadStockData(market)
    }
  },

  // 一键导入最新股票数据
  importLatestData: function() {
    wx.showModal({
      title: '导入股票数据',
      content: '将从服务器获取最新的股票数据，包括价格、财务指标和老刘评分。确定继续吗？',
      confirmText: '导入',
      cancelText: '取消',
      success: (res) => {
        if (res.confirm) {
          this.performDataImport()
        }
      }
    })
  },

  // 执行数据导入
  performDataImport: function() {
    wx.showLoading({
      title: '正在导入数据...',
      mask: true
    })

    const app = getApp()
    
    // 清除缓存，强制从网络获取最新数据
    const cacheKeys = ['stocks_a', 'stocks_hk', 'summary_data', 'market_timing']
    cacheKeys.forEach(key => {
      try {
        wx.removeStorageSync(key)
      } catch (e) {
        console.warn('清除缓存失败:', key, e)
      }
    })

    // 导入当前市场数据
    const market = this.data.selectedMarket
    const dataUrl = market === 'a' ? '/stocks_a.json' : '/stocks_hk.json'
    
    // 强制从网络请求，不使用缓存
    app._requestWithRetry({
      url: app.globalData.apiBaseUrl + dataUrl,
      method: 'GET',
      showLoading: false
    }, 3).then(data => {
      wx.hideLoading()
      
      if (data && data.stocks) {
        // 保存到本地缓存
        const cacheKey = market === 'a' ? 'stocks_a' : 'stocks_hk'
        app.setCache(cacheKey, data)
        
        // 处理并显示数据
        const processedStocks = this.processStockData(data.stocks)
        const stocks = processedStocks.slice(0, 100)
        
        this.setData({
          stockList: stocks,
          totalCount: data.stocks.length,
          filteredCount: stocks.length,
          loading: false,
          error: false
        })

        wx.showToast({
          title: `成功导入${data.stocks.length}只股票`,
          icon: 'success',
          duration: 2000
        })

        // 同时预加载另一个市场的数据
        this.preloadOtherMarketData()

      } else {
        throw new Error('导入的数据格式错误')
      }
    }).catch(err => {
      wx.hideLoading()
      console.error('数据导入失败:', err)
      
      wx.showModal({
        title: '导入失败',
        content: '无法获取最新数据，可能是网络问题或服务器暂时不可用。是否使用本地数据？',
        confirmText: '使用本地',
        cancelText: '重试',
        success: (res) => {
          if (res.confirm) {
            this.loadStockData()
          } else {
            // 用户选择重试
            setTimeout(() => this.performDataImport(), 1000)
          }
        }
      })
    })
  },

  // 预加载另一个市场的数据
  preloadOtherMarketData: function() {
    const app = getApp()
    const otherMarket = this.data.selectedMarket === 'a' ? 'hk' : 'a'
    const otherDataUrl = otherMarket === 'a' ? '/stocks_a.json' : '/stocks_hk.json'
    
    app._requestWithRetry({
      url: app.globalData.apiBaseUrl + otherDataUrl,
      method: 'GET',
      showLoading: false
    }, 1).then(data => {
      if (data && data.stocks) {
        const cacheKey = otherMarket === 'a' ? 'stocks_a' : 'stocks_hk'
        app.setCache(cacheKey, data)
        console.log(`预加载${otherMarket}股数据成功:`, data.stocks.length + '只')
      }
    }).catch(err => {
      console.log('预加载其他市场数据失败:', err)
    })
  },

  // 股票详情
  viewStockDetail: function(e) {
    const code = e.currentTarget.dataset.code
    const market = e.currentTarget.dataset.market || (this.data.currentTab === 0 ? 'A' : 'HK')
    
    // 跳转到分析页面
    wx.navigateTo({
      url: `/pages/analysis/analysis?code=${code}&market=${market}`
    })
  },

  // 搜索结果点击
  onSearchResultTap: function(e) {
    const stock = e.currentTarget.dataset.stock
    this.viewStockAnalysis(stock)
  },

  viewStockAnalysis: function(stock) {
    // 跳转到分析页面并分析该股票
    wx.navigateTo({
      url: `/pages/analysis/analysis?code=${stock.code}&market=${stock.market}`
    })
  },

  // 一键分析功能
  analyzeStock: function(e) {
    const code = e.currentTarget.dataset.code
    const market = e.currentTarget.dataset.market
    
    wx.showLoading({ title: '正在分析...' })
    
    // 模拟API调用进行实时分析
    setTimeout(() => {
      wx.hideLoading()
      wx.navigateTo({
        url: `/pages/analysis/analysis?code=${code}&market=${market}`
      })
    }, 2000)
  },

  // 筛选功能
  toggleFilters: function() {
    this.setData({ showFilters: !this.data.showFilters })
  },

  onFilterChange: function(e) {
    const { type, value } = e.currentTarget.dataset
    const filters = { ...this.data.filters }
    filters[type] = filters[type] === value ? '' : value
    
    this.setData({ filters })
    this.applyFilters()
  },

  applyFilters: function() {
    let filtered = this.data.stockList
    
    // 应用行业筛选
    if (this.data.filters.industry) {
      filtered = filtered.filter(stock => 
        stock.industry && stock.industry.includes(this.data.filters.industry)
      )
    }
    
    // 应用推荐等级筛选
    if (this.data.filters.recommendation) {
      filtered = filtered.filter(stock => 
        stock.recommendation === this.data.filters.recommendation
      )
    }
    
    // 应用价格筛选
    if (this.data.filters.minPrice) {
      const minPrice = parseFloat(this.data.filters.minPrice)
      filtered = filtered.filter(stock => 
        stock.current_price >= minPrice
      )
    }
    
    if (this.data.filters.maxPrice) {
      const maxPrice = parseFloat(this.data.filters.maxPrice)
      filtered = filtered.filter(stock => 
        stock.current_price <= maxPrice
      )
    }
    
    // 应用PE筛选
    if (this.data.filters.minPE) {
      const minPE = parseFloat(this.data.filters.minPE)
      filtered = filtered.filter(stock => 
        stock.pe_ratio && stock.pe_ratio >= minPE
      )
    }
    
    if (this.data.filters.maxPE) {
      const maxPE = parseFloat(this.data.filters.maxPE)
      filtered = filtered.filter(stock => 
        stock.pe_ratio && stock.pe_ratio <= maxPE
      )
    }
    
    // 应用ROE筛选
    if (this.data.filters.minROE) {
      const minROE = parseFloat(this.data.filters.minROE)
      filtered = filtered.filter(stock => 
        stock.roe && stock.roe >= minROE
      )
    }
    
    // 应用评分筛选
    if (this.data.filters.minScore) {
      const minScore = parseFloat(this.data.filters.minScore)
      filtered = filtered.filter(stock => 
        (stock.laoliu_score || stock.total_score || 0) >= minScore
      )
    }
    
    // 重新处理显示数据
    const processedFiltered = this.processStockData(filtered)
    
    this.setData({ 
      stockList: processedFiltered.slice(0, 100),
      filteredCount: filtered.length,
      showFilters: false
    })
  },

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
      }
    })
    
    // 重新加载原始数据
    this.loadStockData()
  },

  // 下拉刷新
  onPullDownRefresh: function() {
    this.loadStockData(this.data.selectedMarket)
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1500)
  },

  // 触底加载更多
  onReachBottom: function() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMoreStocks()
    }
  },

  loadMoreStocks: function() {
    // 模拟加载更多数据
    console.log('加载更多股票数据...')
    // 实际项目中这里需要实现分页加载逻辑
  }
})