// 实时股票分析器
const stockSearchAPI = require('../../utils/stockSearchAPI')

const RealtimeAnalyzer = {
  /**
   * 分析指定股票
   * @param {string} code - 股票代码
   * @param {string} market - 市场 'A' | 'HK'
   * @returns {Promise<Object>} 分析结果
   */
  async analyzeStock(code, market = 'A') {
    try {
      wx.showLoading({ title: '正在分析股票...' })
      
      // 获取股票详细信息
      const stockDetail = await stockSearchAPI.getStockDetail(code, market)
      if (!stockDetail) {
        throw new Error('获取股票信息失败')
      }

      // 进行分析
      const analysis = await stockSearchAPI.analyzeStock(code, market)
      
      wx.hideLoading()
      return {
        success: true,
        data: analysis
      }
      
    } catch (error) {
      wx.hideLoading()
      console.error('股票分析失败:', error)
      
      // 返回错误信息
      return {
        success: false,
        error: error.message || '分析失败'
      }
    }
  },

  /**
   * 搜索并分析股票
   * @param {string} query - 搜索关键词
   * @param {string} market - 市场类型
   * @returns {Promise<Object>} 搜索和分析结果
   */
  async searchAndAnalyze(query, market = 'A') {
    try {
      wx.showLoading({ title: '搜索股票中...' })
      
      // 首先搜索股票
      const searchResults = await stockSearchAPI.searchStocks(query, market)
      
      if (searchResults.length === 0) {
        wx.hideLoading()
        return {
          success: false,
          error: '未找到相关股票'
        }
      }

      // 取第一个搜索结果进行分析
      const targetStock = searchResults[0]
      
      wx.showLoading({ title: `分析 ${targetStock.name}...` })
      
      const analysis = await this.analyzeStock(targetStock.code, targetStock.market)
      
      return {
        success: true,
        searchResults,
        analysis: analysis.data,
        targetStock
      }
      
    } catch (error) {
      wx.hideLoading()
      console.error('搜索分析失败:', error)
      return {
        success: false,
        error: error.message || '搜索分析失败'
      }
    }
  },

  /**
   * 批量分析多只股票
   * @param {Array} codes - 股票代码数组
   * @param {string} market - 市场类型
   * @returns {Promise<Array>} 分析结果数组
   */
  async batchAnalyze(codes, market = 'A') {
    const results = []
    
    for (let i = 0; i < codes.length; i++) {
      const code = codes[i]
      
      try {
        wx.showLoading({ title: `分析 ${code} (${i + 1}/${codes.length})` })
        
        const analysis = await this.analyzeStock(code, market)
        results.push({
          code,
          success: analysis.success,
          data: analysis.success ? analysis.data : null,
          error: analysis.success ? null : analysis.error
        })
        
        // 避免请求过快
        await this.delay(1000)
        
      } catch (error) {
        results.push({
          code,
          success: false,
          data: null,
          error: error.message
        })
      }
    }
    
    wx.hideLoading()
    return results
  },

  /**
   * 获取实时股票数据
   * @param {string} code - 股票代码
   * @param {string} market - 市场类型
   * @returns {Promise<Object>} 实时数据
   */
  async getRealTimeData(code, market = 'A') {
    try {
      const data = await stockSearchAPI.getStockDetail(code, market)
      return {
        success: true,
        data
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      }
    }
  },

  /**
   * 保存分析结果到本地
   * @param {Object} analysis - 分析结果
   * @param {string} code - 股票代码
   */
  saveAnalysisToLocal(analysis, code) {
    try {
      const key = `analysis_${code}_${Date.now()}`
      const data = {
        ...analysis,
        saveTime: new Date().toISOString(),
        code
      }
      
      wx.setStorageSync(key, data)
      
      // 更新分析历史索引
      let analysisHistory = wx.getStorageSync('analysis_history') || []
      analysisHistory.unshift({
        code,
        name: analysis.basic_info?.name || code,
        score: analysis.laoliu_evaluation?.laoliu_score || 0,
        time: data.saveTime,
        key
      })
      
      // 只保留最近50个分析
      analysisHistory = analysisHistory.slice(0, 50)
      wx.setStorageSync('analysis_history', analysisHistory)
      
    } catch (error) {
      console.error('保存分析结果失败:', error)
    }
  },

  /**
   * 获取分析历史
   * @returns {Array} 历史分析列表
   */
  getAnalysisHistory() {
    try {
      return wx.getStorageSync('analysis_history') || []
    } catch (error) {
      console.error('获取分析历史失败:', error)
      return []
    }
  },

  /**
   * 删除分析历史
   * @param {string} key - 分析记录key
   */
  deleteAnalysis(key) {
    try {
      wx.removeStorageSync(key)
      
      let history = this.getAnalysisHistory()
      history = history.filter(item => item.key !== key)
      wx.setStorageSync('analysis_history', history)
      
      return true
    } catch (error) {
      console.error('删除分析记录失败:', error)
      return false
    }
  },

  /**
   * 工具方法：延迟
   * @param {number} ms - 延迟毫秒数
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  },

  /**
   * 验证股票代码格式
   * @param {string} code - 股票代码
   * @param {string} market - 市场类型
   * @returns {boolean} 是否有效
   */
  validateStockCode(code, market = 'A') {
    if (!code || typeof code !== 'string') {
      return false
    }

    code = code.trim().toUpperCase()

    if (market === 'A') {
      // A股：6位数字
      return /^\d{6}$/.test(code)
    } else if (market === 'HK') {
      // 港股：5位数字，可能有前导0
      return /^\d{5}$/.test(code)
    }

    return false
  },

  /**
   * 格式化股票代码
   * @param {string} code - 股票代码
   * @param {string} market - 市场类型
   * @returns {string} 格式化后的代码
   */
  formatStockCode(code, market = 'A') {
    if (!code) return ''
    
    code = code.trim().replace(/[^\d]/g, '')
    
    if (market === 'A' && code.length <= 6) {
      return code.padStart(6, '0')
    } else if (market === 'HK' && code.length <= 5) {
      return code.padStart(5, '0')
    }
    
    return code
  }
}

module.exports = RealtimeAnalyzer
