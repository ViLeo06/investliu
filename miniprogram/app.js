// 小程序入口文件
App({
  globalData: {
    // 全局数据
    userInfo: null,
    apiBaseUrl: 'https://vileo06.github.io/investliu',
    updateTime: '',
    cacheTime: 3600000, // 缓存1小时
    systemInfo: null
  },

  onLaunch: function() {
    console.log('老刘投资决策小程序启动')
    
    // 获取系统信息
    this.getSystemInfo()
    
    // 检查小程序更新
    this.checkUpdate()
    
    // 初始化配置
    this.initConfig()
  },

  onShow: function() {
    console.log('小程序显示')
  },

  onHide: function() {
    console.log('小程序隐藏')
  },

  onError: function(msg) {
    console.error('小程序错误:', msg)
  },

  // 获取系统信息
  getSystemInfo: function() {
    const self = this
    wx.getSystemInfo({
      success: function(res) {
        self.globalData.systemInfo = res
        console.log('系统信息:', res)
      }
    })
  },

  // 检查小程序更新
  checkUpdate: function() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      updateManager.onCheckForUpdate(function(res) {
        if (res.hasUpdate) {
          console.log('发现新版本')
        }
      })

      updateManager.onUpdateReady(function() {
        wx.showModal({
          title: '更新提示',
          content: '新版本已经准备好，是否重启应用？',
          success: function(res) {
            if (res.confirm) {
              updateManager.applyUpdate()
            }
          }
        })
      })

      updateManager.onUpdateFailed(function() {
        console.log('新版本下载失败')
      })
    }
  },

  // 初始化配置
  initConfig: function() {
    const self = this
    
    // 从缓存读取配置
    const config = wx.getStorageSync('app_config')
    if (config) {
      self.globalData.apiBaseUrl = config.baseUrl || self.globalData.apiBaseUrl
      console.log('加载本地配置:', config)
    }

    // 获取最新配置
    this.fetchConfig()
  },

  // 获取远程配置
  fetchConfig: function() {
    const self = this
    
    wx.request({
      url: self.globalData.apiBaseUrl + '/miniprogram_config.json',
      method: 'GET',
      success: function(res) {
        if (res.statusCode === 200 && res.data) {
          console.log('获取远程配置成功:', res.data)
          
          // 更新全局配置
          if (res.data.baseUrl) {
            self.globalData.apiBaseUrl = res.data.baseUrl
          }
          
          self.globalData.updateTime = res.data.updateTime || ''
          
          // 缓存配置
          wx.setStorageSync('app_config', res.data)
        }
      },
      fail: function(err) {
        console.error('获取远程配置失败:', err)
      }
    })
  },

  // 通用API请求方法
  request: function(options) {
    const self = this
    const defaultOptions = {
      method: 'GET',
      timeout: 10000,
      header: {
        'Content-Type': 'application/json'
      }
    }

    // 合并选项
    const requestOptions = Object.assign({}, defaultOptions, options)
    
    // 添加base URL
    if (requestOptions.url && !requestOptions.url.startsWith('http')) {
      requestOptions.url = self.globalData.apiBaseUrl + requestOptions.url
    }

    // 显示加载
    if (requestOptions.showLoading !== false) {
      wx.showLoading({
        title: '加载中...',
        mask: true
      })
    }

    return new Promise((resolve, reject) => {
      wx.request({
        ...requestOptions,
        success: function(res) {
          wx.hideLoading()
          
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            console.error('请求失败:', res)
            reject(new Error(`请求失败: ${res.statusCode}`))
          }
        },
        fail: function(err) {
          wx.hideLoading()
          console.error('网络请求失败:', err)
          
          wx.showToast({
            title: '网络请求失败',
            icon: 'none',
            duration: 2000
          })
          
          reject(err)
        }
      })
    })
  },

  // 格式化数字
  formatNumber: function(num, decimals = 2) {
    if (num == null || isNaN(num)) return '--'
    return Number(num).toFixed(decimals)
  },

  // 格式化百分比
  formatPercent: function(num, decimals = 2) {
    if (num == null || isNaN(num)) return '--'
    const percent = Number(num * 100).toFixed(decimals)
    return (num >= 0 ? '+' : '') + percent + '%'
  },

  // 获取涨跌颜色
  getChangeColor: function(change) {
    if (change > 0) return '#f5222d' // 红色
    if (change < 0) return '#52c41a' // 绿色
    return '#666666' // 灰色
  },

  // 缓存管理
  setCache: function(key, data, expireTime = null) {
    const cacheData = {
      data: data,
      timestamp: Date.now(),
      expireTime: expireTime || (Date.now() + this.globalData.cacheTime)
    }
    wx.setStorageSync(key, cacheData)
  },

  getCache: function(key) {
    try {
      const cacheData = wx.getStorageSync(key)
      if (cacheData && Date.now() < cacheData.expireTime) {
        return cacheData.data
      }
      return null
    } catch (e) {
      return null
    }
  },

  // 清理过期缓存
  clearExpiredCache: function() {
    try {
      const info = wx.getStorageInfoSync()
      const now = Date.now()
      
      info.keys.forEach(key => {
        const data = wx.getStorageSync(key)
        if (data && data.expireTime && now >= data.expireTime) {
          wx.removeStorageSync(key)
        }
      })
    } catch (e) {
      console.error('清理缓存失败:', e)
    }
  }
})