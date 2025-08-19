Page({
  data: {
    riskLevel: 'medium',
    dataSource: 'github',
    autoRefresh: true,
    notifications: true
  },

  onLoad: function (options) {
    console.log('设置页面加载');
    this.loadSettings();
  },

  loadSettings: function () {
    const settings = wx.getStorageSync('settings') || {};
    this.setData({
      riskLevel: settings.riskLevel || 'medium',
      dataSource: settings.dataSource || 'github',
      autoRefresh: settings.autoRefresh !== false,
      notifications: settings.notifications !== false
    });
  },

  onRiskLevelChange: function (e) {
    this.setData({
      riskLevel: e.detail.value
    });
    this.saveSettings();
  },

  onDataSourceChange: function (e) {
    this.setData({
      dataSource: e.detail.value
    });
    this.saveSettings();
  },

  onAutoRefreshChange: function (e) {
    this.setData({
      autoRefresh: e.detail.value
    });
    this.saveSettings();
  },

  onNotificationsChange: function (e) {
    this.setData({
      notifications: e.detail.value
    });
    this.saveSettings();
  },

  saveSettings: function () {
    const settings = {
      riskLevel: this.data.riskLevel,
      dataSource: this.data.dataSource,
      autoRefresh: this.data.autoRefresh,
      notifications: this.data.notifications
    };
    wx.setStorageSync('settings', settings);
    wx.showToast({
      title: '设置已保存',
      icon: 'success'
    });
  },

  onClearCache: function () {
    wx.showModal({
      title: '清除缓存',
      content: '确定要清除所有缓存数据吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          wx.showToast({
            title: '缓存已清除',
            icon: 'success'
          });
        }
      }
    });
  },

  onAbout: function () {
    wx.showModal({
      title: '关于老刘投资决策',
      content: '基于老刘多年投资经验打造的股票决策辅助工具\n版本：1.0.0',
      showCancel: false
    });
  }
});