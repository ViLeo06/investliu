const RealtimeAnalyzer = require('./realtime_analyzer')

Page({
  data: {
    // 搜索和筛选
    searchQuery: '',
    showFilters: false,
    recommendationFilter: '',
    minScore: 0,
    
    // 数据状态
    loading: true,
    error: false,
    errorMessage: '',
    
    // 分析数据
    analysisList: [],
    filteredAnalysisList: [],
    
    // 详情弹窗
    showDetail: false,
    selectedStock: null,
    
    // 传参
    stockCode: '',
    market: 'a',
    
    // 实时分析
    showRealtimeSearch: false,
    realtimeSearchQuery: '',
    isAnalyzing: false,
    analysisHistory: []
  },

  onLoad: function (options) {
    // 如果有传参，说明是查看单个股票
    if (options.code && options.market) {
      this.setData({
        stockCode: options.code,
        market: options.market
      })
      // 直接分析指定股票
      this.analyzeSpecificStock(options.code, options.market)
    }
    
    this.loadAnalysisData()
    this.loadAnalysisHistory()
  },

  onShow: function() {
    // 页面显示时刷新数据
    this.loadAnalysisData()
  },

  loadAnalysisData: function() {
    this.setData({ loading: true, error: false })
    
    try {
      const app = getApp()
      
      // 优先加载分析样本数据
      app.request('/analysis_samples.json', 'analysis_samples').then(data => {
        console.log('分析样本数据加载成功:', data)
        
        if (data && data.analysis_results && data.analysis_results.length > 0) {
          this.setData({
            analysisList: data.analysis_results,
            filteredAnalysisList: data.analysis_results,
            loading: false
          })
          
          // 如果有指定股票，立即显示详情
          if (this.data.stockCode) {
            this.showStockDetail(this.data.stockCode)
          }
          
          wx.showToast({
            title: `加载${data.analysis_results.length}个分析`,
            icon: 'success'
          })
          
        } else {
          throw new Error('分析数据为空')
        }
        
      }).catch(err => {
        console.error('加载分析样本失败:', err)
        
        // 尝试加载本地存储的分析数据
        const localData = wx.getStorageSync('analysis_data')
        if (localData && localData.length > 0) {
          this.setData({
            analysisList: localData,
            filteredAnalysisList: localData,
            loading: false
          })
          
          // 如果有指定股票，立即显示详情
          if (this.data.stockCode) {
            this.showStockDetail(this.data.stockCode)
          }
          
          wx.showToast({
            title: '显示本地数据',
            icon: 'none'
          })
          
        } else {
          // 加载预设的分析数据
          this.loadMockAnalysisData()
        }
      })
      
    } catch (error) {
      console.error('加载分析数据失败:', error)
      this.setData({
        loading: false,
        error: true,
        errorMessage: '数据加载失败，请重试'
      })
    }
  },

  loadMockAnalysisData: function() {
    // 加载预设的模拟数据
    const mockAnalysisData = [
      {
        "basic_info": {
          "code": "600036",
          "name": "招商银行",
          "market_type": "A",
          "current_price": 43.12,
          "change_percent": 1.2,
          "volume": 2253764,
          "market_cap": 627191697.44,
          "industry": "银行",
          "update_time": "2025-08-24 13:48:36"
        },
        "valuation_metrics": {
          "pe_ratio": 6.1,
          "pb_ratio": 1.05,
          "ps_ratio": 0,
          "dividend_yield": 4.61
        },
        "financial_metrics": {
          "roe": 16.2,
          "roa": 11.3,
          "debt_ratio": 0.82,
          "current_ratio": 2.41,
          "gross_margin": 52.8,
          "net_margin": 9.72,
          "revenue_growth": 12.3,
          "profit_growth": 18.5,
          "report_date": "2024-09-30"
        },
        "laoliu_evaluation": {
          "laoliu_score": 65,
          "analysis_points": [
            "ROE荠16.2%，盈利能力强",
            "PE仅6.1倍，估值偏低",
            "PB仅1.05倍，账面价值安全",
            "银行行业符合老刘投资偏好"
          ],
          "risk_warnings": [
            "负债率82.0%，财务风险较高"
          ],
          "investment_advice": "谨慎推荐：基本面良好，可适当配置",
          "contrarian_opportunity": false
        },
        "technical_analysis": {
          "volume_price_signal": "量价关系正常",
          "volume_ratio": 1.13,
          "price_change": -0.48
        },
        "ai_insights": {
          "analysis_content": "【招商银行投资分析】\n\n综合评分：65分\n投资建议：谨慎推荐：基本面良好，可适当配置\n\n主要优势：\n• ROE荠16.2%，盈利能力强\n• PE仅6.1倍，估值偏低\n• PB仅1.05倍，账面价值安全\n\n风险提示：\n• 负债率82.0%，财务风险较高\n\n基于老刘投资理念，该股票符合价值投资标准，建议关注。",
          "key_points": [
            "ROE荠16.2%，盈利能力强",
            "PE仅6.1倍，估值偏低",
            "PB仅1.05倍，账面价值安全",
            "负债率82.0%，财务风险较高"
          ],
          "recommendation": "buy",
          "confidence_level": "中"
        },
        "investment_summary": {
          "comprehensive_score": 65,
          "recommendation": "buy",
          "target_price": 49.59,
          "stop_loss": 36.65,
          "position_suggestion": "可适度配置，建议1-3成"
        }
      },
      {
        "basic_info": {
          "code": "000858",
          "name": "五粮液",
          "market_type": "A",
          "current_price": 152.30,
          "change_percent": 2.1,
          "volume": 1580000,
          "market_cap": 987456000,
          "industry": "食品饮料",
          "update_time": "2025-08-24 13:48:36"
        },
        "valuation_metrics": {
          "pe_ratio": 18.5,
          "pb_ratio": 4.2,
          "ps_ratio": 5.8,
          "dividend_yield": 2.85
        },
        "financial_metrics": {
          "roe": 22.1,
          "roa": 15.8,
          "debt_ratio": 0.35,
          "current_ratio": 2.85,
          "gross_margin": 78.5,
          "net_margin": 13.3,
          "revenue_growth": 18.2,
          "profit_growth": 25.3,
          "report_date": "2024-09-30"
        },
        "laoliu_evaluation": {
          "laoliu_score": 82,
          "analysis_points": [
            "ROE荠22.1%，盈利能力优秀",
            "毛利率78.5%，品牌优势明显",
            "食品饮料行业符合老刘投资偏好",
            "财务安全，负债率35%"
          ],
          "risk_warnings": [
            "PE18.5倍估值偏高",
            "PB4.2倍需要关注"
          ],
          "investment_advice": "推荐：基本面优秀，符合老刘投资理念",
          "contrarian_opportunity": false
        },
        "technical_analysis": {
          "volume_price_signal": "量价配合良好",
          "volume_ratio": 1.45,
          "price_change": 2.1
        },
        "ai_insights": {
          "analysis_content": "【五粮液投资分析】\n\n综合评分：82分\n投资建议：推荐\n\n主要优势：\n• ROE22.1%，盈利能力优秀\n• 毛利率78.5%，品牌优势明显\n• 食品饮料行业符合老刘投资偏好\n\n风险提示：\n• PE18.5倍估值偏高，需要谨慎\n\n基于老刘投资理念，该股票优质，建议重点关注。",
          "key_points": [
            "ROE22.1%，盈利能力优秀",
            "毛利率78.5%，品牌优势明显",
            "财务安全，负债率35%",
            "PE18.5倍估值偏高"
          ],
          "recommendation": "strong_buy",
          "confidence_level": "高"
        },
        "investment_summary": {
          "comprehensive_score": 82,
          "recommendation": "strong_buy",
          "target_price": 190.38,
          "stop_loss": 129.46,
          "position_suggestion": "可适当加大仓位，建议3-5成"
        }
      }
    ]
    
    // 保存到本地存储
    try {
      wx.setStorageSync('analysis_data', mockAnalysisData)
    } catch (error) {
      console.error('保存分析数据失败:', error)
    }
    
    this.setData({
      analysisList: mockAnalysisData,
      filteredAnalysisList: mockAnalysisData,
      loading: false
    })
    
    // 如果有指定股票，立即显示详情
    if (this.data.stockCode) {
      this.showStockDetail(this.data.stockCode)
    }
  },

  // 搜索功能
  onSearchInput: function(e) {
    const query = e.detail.value
    this.setData({ searchQuery: query })
    this.performFilter()
  },

  // 切换筛选面板
  toggleFilters: function() {
    this.setData({ showFilters: !this.data.showFilters })
  },

  // 推荐等级筛选
  onRecommendationFilter: function(e) {
    const value = e.currentTarget.dataset.value
    this.setData({ recommendationFilter: value })
    this.performFilter()
  },

  // 评分筛选
  onMinScoreChange: function(e) {
    const minScore = e.detail.value
    this.setData({ minScore: minScore })
    this.performFilter()
  },

  // 执行筛选
  performFilter: function() {
    let filtered = this.data.analysisList.filter(item => {
      // 搜索筛选
      if (this.data.searchQuery) {
        const query = this.data.searchQuery.toLowerCase()
        const matchName = item.basic_info.name.toLowerCase().includes(query)
        const matchCode = item.basic_info.code.toLowerCase().includes(query)
        const matchIndustry = item.basic_info.industry.toLowerCase().includes(query)
        if (!matchName && !matchCode && !matchIndustry) {
          return false
        }
      }
      
      // 推荐等级筛选
      if (this.data.recommendationFilter && 
          item.investment_summary && 
          item.investment_summary.recommendation !== this.data.recommendationFilter) {
        return false
      }
      
      // 评分筛选
      if (item.laoliu_evaluation && 
          item.laoliu_evaluation.laoliu_score < this.data.minScore) {
        return false
      }
      
      return true
    })
    
    this.setData({ filteredAnalysisList: filtered })
  },

  // 查看详情
  viewDetail: function(e) {
    const code = e.currentTarget.dataset.code
    this.showStockDetail(code)
  },

  showStockDetail: function(code) {
    const stock = this.data.analysisList.find(item => item.basic_info.code === code)
    if (stock) {
      this.setData({
        selectedStock: stock,
        showDetail: true
      })
    }
  },

  // 关闭详情
  closeDetail: function() {
    this.setData({ showDetail: false, selectedStock: null })
  },

  // 导出数据
  exportData: function() {
    const data = this.data.filteredAnalysisList
    const exportContent = data.map(item => ({
      股票代码: item.basic_info.code,
      股票名称: item.basic_info.name,
      行业: item.basic_info.industry,
      当前价格: item.basic_info.current_price,
      老刘评分: item.laoliu_evaluation ? item.laoliu_evaluation.laoliu_score : 'N/A',
      投资建议: item.laoliu_evaluation ? item.laoliu_evaluation.investment_advice : 'N/A',
      推荐等级: item.investment_summary ? item.investment_summary.recommendation : 'N/A',
      目标价格: item.investment_summary ? item.investment_summary.target_price : 'N/A',
      止损价格: item.investment_summary ? item.investment_summary.stop_loss : 'N/A'
    }))
    
    // 保存到剄贴板
    wx.setClipboardData({
      data: JSON.stringify(exportContent, null, 2),
      success: () => {
        wx.showToast({
          title: '数据已复制到剄贴板',
          icon: 'success'
        })
      }
    })
  },

  // 刷新数据
  refreshData: function() {
    // 清除缓存
    try {
      wx.removeStorageSync('analysis_data')
    } catch (error) {
      console.error('清除缓存失败:', error)
    }
    
    // 重新加载数据
    this.loadAnalysisData()
    
    wx.showToast({
      title: '数据已刷新',
      icon: 'success'
    })
  },

  // 实时股票分析功能
  showRealtimeAnalysis: function() {
    this.setData({ showRealtimeSearch: true })
  },

  hideRealtimeAnalysis: function() {
    this.setData({ 
      showRealtimeSearch: false,
      realtimeSearchQuery: ''
    })
  },

  onRealtimeSearchInput: function(e) {
    this.setData({ realtimeSearchQuery: e.detail.value })
  },

  // 分析指定股票
  async analyzeSpecificStock(code, market) {
    this.setData({ isAnalyzing: true })
    
    try {
      const result = await RealtimeAnalyzer.analyzeStock(code, market.toUpperCase())
      
      if (result.success) {
        // 添加到分析列表顶部
        const newAnalysis = result.data
        const analysisList = [newAnalysis, ...this.data.analysisList]
        
        this.setData({
          analysisList,
          filteredAnalysisList: analysisList,
          isAnalyzing: false
        })
        
        // 保存分析结果
        RealtimeAnalyzer.saveAnalysisToLocal(newAnalysis, code)
        
        // 自动显示详情
        this.showStockDetail(code)
        
        wx.showToast({
          title: '分析完成',
          icon: 'success'
        })
      } else {
        throw new Error(result.error)
      }
      
    } catch (error) {
      console.error('分析失败:', error)
      this.setData({ isAnalyzing: false })
      
      wx.showModal({
        title: '分析失败',
        content: error.message || '无法分析该股票，请检查股票代码或网络连接',
        showCancel: false
      })
    }
  },

  // 搜索并分析股票
  async searchAndAnalyzeStock() {
    const query = this.data.realtimeSearchQuery.trim()
    if (!query) {
      wx.showToast({
        title: '请输入股票代码或名称',
        icon: 'none'
      })
      return
    }

    this.setData({ isAnalyzing: true })

    try {
      const result = await RealtimeAnalyzer.searchAndAnalyze(query, 'A')
      
      if (result.success) {
        // 添加分析结果
        const newAnalysis = result.analysis
        const analysisList = [newAnalysis, ...this.data.analysisList]
        
        this.setData({
          analysisList,
          filteredAnalysisList: analysisList,
          isAnalyzing: false,
          showRealtimeSearch: false,
          realtimeSearchQuery: ''
        })
        
        // 保存分析结果
        RealtimeAnalyzer.saveAnalysisToLocal(newAnalysis, result.targetStock.code)
        
        // 显示分析结果
        this.showStockDetail(result.targetStock.code)
        
        wx.showToast({
          title: `${result.targetStock.name} 分析完成`,
          icon: 'success'
        })
      } else {
        throw new Error(result.error)
      }
      
    } catch (error) {
      console.error('搜索分析失败:', error)
      this.setData({ isAnalyzing: false })
      
      wx.showModal({
        title: '搜索失败',
        content: error.message || '未找到相关股票或分析失败',
        showCancel: false
      })
    }
  },

  // 加载分析历史
  loadAnalysisHistory: function() {
    const history = RealtimeAnalyzer.getAnalysisHistory()
    this.setData({ analysisHistory: history })
  },

  // 查看历史分析
  viewHistoryAnalysis: function(e) {
    const key = e.currentTarget.dataset.key
    try {
      const analysis = wx.getStorageSync(key)
      if (analysis) {
        this.setData({
          selectedStock: analysis,
          showDetail: true
        })
      }
    } catch (error) {
      console.error('读取历史分析失败:', error)
      wx.showToast({
        title: '读取失败',
        icon: 'none'
      })
    }
  },

  // 删除历史分析
  deleteHistoryAnalysis: function(e) {
    const key = e.currentTarget.dataset.key
    const code = e.currentTarget.dataset.code
    
    wx.showModal({
      title: '删除确认',
      content: `确定删除 ${code} 的分析记录吗？`,
      success: (res) => {
        if (res.confirm) {
          const success = RealtimeAnalyzer.deleteAnalysis(key)
          if (success) {
            this.loadAnalysisHistory()
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
          } else {
            wx.showToast({
              title: '删除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  }
})