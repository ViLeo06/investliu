// 小程序入口文件
const mockData = require('./utils/mockData_light.js');
const mockDataFixed = require('./utils/mockData_fixed.js');

App({
  globalData: {
    // 全局数据
    userInfo: null,
    // ✅ 已配置为当前GitHub Pages地址
    // 格式: https://你的用户名.github.io/investliu
    apiBaseUrl: 'https://ViLeo06.github.io/investliu',
    updateTime: '',
    cacheTime: 3600000, // 缓存1小时
    systemInfo: null,
    isDev: false // 开发环境标识
  },

  onLaunch: function() {
    console.log('老刘投资决策小程序启动')
    
    // 检测开发环境
    this.checkDevelopmentEnvironment()
    
    // 在开发环境下清理股票缓存，确保使用最新数据
    if (this.globalData.isDev) {
      this.clearStockCache()
    }
    
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

  // 检测开发环境
  checkDevelopmentEnvironment: function() {
    // 检测是否在开发环境
    const accountInfo = wx.getAccountInfoSync && wx.getAccountInfoSync();
    if (accountInfo && accountInfo.miniProgram) {
      // 如果版本号为 devtools 或 develop，则为开发环境
      this.globalData.isDev = accountInfo.miniProgram.envVersion === 'develop' || 
                              accountInfo.miniProgram.envVersion === 'trial' ||
                              !accountInfo.miniProgram.envVersion;
      console.log('环境检测:', this.globalData.isDev ? '开发环境' : '生产环境');
      console.log('账户信息:', accountInfo);
    } else {
      // 如果获取不到账户信息，默认为开发环境（开发者工具情况）
      this.globalData.isDev = true;
      console.log('无法获取账户信息，默认为开发环境');
    }
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

  // 加载本地数据（开发环境）
  loadLocalData: function(url) {
    const self = this;
    
    console.log('loadLocalData调用:', {
      url: url,
      isDev: self.globalData.isDev
    });
    
    if (!self.globalData.isDev) {
      console.log('非开发环境，不使用Mock数据');
      return null;
    }
    
    // 对于开发环境，直接尝试require本地JSON文件
    console.log('开发环境：尝试读取本地JSON文件', url);
    
    try {
      console.log('开发环境：尝试使用Mock数据', url);
      
      // 在开发环境下，直接使用Mock数据，不尝试require JSON文件
      // 因为微信小程序不支持require JSON文件
      const data = self.getMockData(url);
      console.log('Mock数据结果:', data ? '有数据' : '无数据');
      
      return Promise.resolve(data);
      
    } catch (error) {
      console.log('Mock数据加载失败:', error);
      return Promise.resolve(null);
    }
  },

  // 获取Mock数据
  getMockData: function(url) {
    const urlToDataMap = {
      '/summary.json': mockData.summary,
      '/market_timing.json': mockData.market_timing,
      '/laoliu_quotes.json': mockData.laoliu_quotes,
      '/stocks_a.json': mockData.stocks_a,
      '/stocks_hk.json': mockData.stocks_hk,
      '/analysis_samples.json': mockDataFixed['/analysis_samples.json'],
      '/stocks_a_recommendations.json': mockData.stocks_a_recommendations,
      '/stocks_hk_recommendations.json': mockData.stocks_hk_recommendations
    };
    
    const result = urlToDataMap[url] || null;
    
    // 特别针对analysis_samples.json添加详细日志
    if (url === '/analysis_samples.json') {
      console.log('analysis_samples详细信息:', {
        url: url,
        存在映射: !!result,
        数据类型: typeof result,
        total_count: result ? result.total_count : '无数据',
        analysis_results数量: result && result.analysis_results ? result.analysis_results.length : '无analysis_results',
        第一条数据有valuation_metrics: result && result.analysis_results && result.analysis_results[0] ? !!result.analysis_results[0].valuation_metrics : '无法检查'
      });
    } else {
      console.log('getMockData:', {
        url: url,
        存在映射: !!result,
        数据类型: typeof result,
        股票数量: result && result.stocks ? result.stocks.length : (result && Array.isArray(result) ? result.length : '无stocks字段')
      });
    }
    
    return result;
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
        if (data) {
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
        } else {
          console.log('金句数据为空，使用本地版本');
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
      
      // 在开发环境下，尝试使用本地数据
      if (self.globalData.isDev) {
        const localDataResult = self.loadLocalData(urlOrOptions);
        if (localDataResult) {
          return localDataResult;
        }
      }
      
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
    // 在开发环境下，尝试使用本地数据
    if (self.globalData.isDev && urlOrOptions.url) {
      const localDataResult = self.loadLocalData(urlOrOptions.url);
      if (localDataResult) {
        return localDataResult;
      }
    }
    
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
  },

  // 强制清理所有股票相关缓存
  clearStockCache: function() {
    try {
      const keysToRemove = [
        'stocks_a',
        'stocks_hk', 
        'stocks_last_update',
        'app_config'
      ];
      
      keysToRemove.forEach(key => {
        wx.removeStorageSync(key);
        console.log('清理缓存:', key);
      });
      
      console.log('所有股票缓存已清理');
    } catch (e) {
      console.error('清理股票缓存失败:', e);
    }
  }
})