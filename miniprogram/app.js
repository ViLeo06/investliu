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

  // 通用API请求方法（带重试）
  request: function(options) {
    const self = this
    const defaultOptions = {
      method: 'GET',
      timeout: 10000,
      header: {
        'Content-Type': 'application/json'
      },
      retry: 2 // 默认重试2次
    }

    // 合并选项
    const requestOptions = Object.assign({}, defaultOptions, options)
    
    // 添加base URL
    if (requestOptions.url && !requestOptions.url.startsWith('http')) {
      requestOptions.url = self.globalData.apiBaseUrl + requestOptions.url
    }

    return this._requestWithRetry(requestOptions, requestOptions.retry || 0)
  },

  // 带重试的请求方法
  _requestWithRetry: function(options, retryCount) {
    const self = this
    
    // 显示加载
    if (options.showLoading !== false) {
      wx.showLoading({
        title: '加载中...',
        mask: true
      })
    }

    return new Promise((resolve, reject) => {
      wx.request({
        ...options,
        success: function(res) {
          wx.hideLoading()
          
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            console.error('请求失败:', res)
            
            // 如果是服务器错误且还有重试次数，则重试
            if (res.statusCode >= 500 && retryCount > 0) {
              console.log(`请求失败，${retryCount}秒后重试...`)
              setTimeout(() => {
                self._requestWithRetry(options, retryCount - 1)
                  .then(resolve)
                  .catch(reject)
              }, 1000)
              return
            }
            
            reject(new Error(`请求失败: ${res.statusCode}`))
          }
        },
        fail: function(err) {
          wx.hideLoading()
          console.error('网络请求失败:', err)
          
          // 如果还有重试次数，则重试
          if (retryCount > 0) {
            console.log(`网络请求失败，${retryCount}秒后重试...`)
            setTimeout(() => {
              self._requestWithRetry(options, retryCount - 1)
                .then(resolve)
                .catch(reject)
            }, 1000)
            return
          }
          
          // 根据错误类型显示不同提示
          let errorMsg = '网络请求失败'
          if (err.errMsg) {
            if (err.errMsg.includes('timeout')) {
              errorMsg = '请求超时，请检查网络'
            } else if (err.errMsg.includes('fail')) {
              errorMsg = '网络连接异常'
            }
          }
          
          wx.showToast({
            title: errorMsg,
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

  // 金句版本管理
  checkQuotesVersion: function() {
    const self = this;
    
    return new Promise((resolve) => {
      // 获取本地缓存的版本信息
      const localVersion = wx.getStorageSync('quotes_version') || '0.0.0';
      
      // 请求远程版本信息
      self.request({
        url: '/laoliu_quotes.json',
        showLoading: false
      }).then(data => {
        const remoteVersion = data.version || '1.0.0';
        
        if (self.compareVersions(remoteVersion, localVersion) > 0) {
          console.log('检测到金句新版本:', remoteVersion);
          // 清除旧的金句缓存
          wx.removeStorageSync('quotes_cache');
          // 更新版本号
          wx.setStorageSync('quotes_version', remoteVersion);
          resolve({ hasUpdate: true, version: remoteVersion });
        } else {
          resolve({ hasUpdate: false, version: localVersion });
        }
      }).catch(err => {
        console.warn('检查金句版本失败:', err);
        resolve({ hasUpdate: false, version: localVersion });
      });
    });
  },

  // 版本号比较
  compareVersions: function(v1, v2) {
    const parts1 = v1.split('.').map(Number);
    const parts2 = v2.split('.').map(Number);
    
    for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
      const part1 = parts1[i] || 0;
      const part2 = parts2[i] || 0;
      
      if (part1 > part2) return 1;
      if (part1 < part2) return -1;
    }
    return 0;
  },

  // 请求金句数据（带缓存和版本管理）
  requestQuotes: function() {
    const self = this;
    const cacheKey = 'quotes_cache';
    
    // 先检查版本
    return self.checkQuotesVersion().then(versionInfo => {
      // 如果没有更新，尝试从缓存加载
      if (!versionInfo.hasUpdate) {
        const cachedData = self.getCache(cacheKey);
        if (cachedData) {
          console.log('从缓存加载金句数据');
          return Promise.resolve(cachedData);
        }
      }
      
      // 从网络加载
      return self.request({
        url: '/laoliu_quotes.json'
      }).then(data => {
        if (data) {
          // 缓存数据
          self.setCache(cacheKey, data, 24 * 60 * 60 * 1000); // 缓存24小时
          console.log('金句数据加载并缓存成功');
        }
        return data;
      });
    });
  },

  // 增强的request方法，支持直接传递路径和缓存key
  request: function(urlOrOptions, cacheKey) {
    const self = this;
    
    // 兼容旧的调用方式
    if (typeof urlOrOptions === 'string') {
      const options = {
        url: urlOrOptions,
        method: 'GET'
      };
      
      // 如果提供了cacheKey，先尝试从缓存加载
      if (cacheKey) {
        const cachedData = self.getCache(cacheKey);
        if (cachedData) {
          return Promise.resolve(cachedData);
        }
        
        // 网络请求成功后缓存
        return self._requestWithRetry(options, 2).then(data => {
          if (data) {
            self.setCache(cacheKey, data);
          }
          return data;
        });
      }
      
      return self._requestWithRetry(options, 2);
    }
    
    // 新的对象参数方式
    return self._requestWithRetry(urlOrOptions, urlOrOptions.retry || 2);
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