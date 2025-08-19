Page({
  data: {
    portfolio: [],
    totalValue: 0,
    totalCost: 0,
    totalProfit: 0,
    profitRate: 0
  },

  onLoad: function (options) {
    console.log('组合页面加载');
    this.loadPortfolio();
  },

  onShow: function () {
    this.loadPortfolio();
  },

  loadPortfolio: function () {
    const app = getApp();
    const mockData = [
      {
        code: '000001',
        name: '平安银行',
        shares: 1000,
        cost: 12.50,
        current: 13.20,
        profit: 700,
        profitRate: 5.6
      },
      {
        code: '000002',
        name: '万科A',
        shares: 500,
        cost: 25.80,
        current: 24.90,
        profit: -450,
        profitRate: -3.5
      }
    ];

    this.setData({
      portfolio: mockData,
      totalValue: mockData.reduce((sum, stock) => sum + stock.shares * stock.current, 0),
      totalCost: mockData.reduce((sum, stock) => sum + stock.shares * stock.cost, 0)
    });

    this.setData({
      totalProfit: this.data.totalValue - this.data.totalCost,
      profitRate: ((this.data.totalValue - this.data.totalCost) / this.data.totalCost * 100).toFixed(2)
    });
  },

  onStockTap: function (e) {
    const stock = e.currentTarget.dataset.stock;
    wx.navigateTo({
      url: `/pages/analysis/analysis?code=${stock.code}&name=${stock.name}`
    });
  }
});