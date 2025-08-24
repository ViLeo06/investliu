// 精简Mock数据 - 用于开发环境测试
const mockData = {
  summary: {
    "update_time": "2025-08-24 14:58:19",
    "market_status": {
      "sentiment": "neutral",
      "recommended_position": 0.6,
      "main_signals": ["技术面显示震荡趋势", "基本面配置价值显现", "资金面相对宽松"]
    },
    "recommendations_count": {
      "a_stocks": 12,
      "hk_stocks": 8,
      "total": 20
    },
    "top_picks": {
      "a_stocks": [
        {
          "code": "000001",
          "name": "平安银行",
          "current_price": 12.85,
          "change_percent": -0.8,
          "recommendation": "buy",
          "total_score": 0.75
        },
        {
          "code": "600036",
          "name": "招商银行",
          "current_price": 43.12,
          "change_percent": 1.2,
          "recommendation": "strong_buy",
          "total_score": 0.82
        }
      ],
      "hk_stocks": [
        {
          "code": "01398",
          "name": "工商银行",
          "current_price": 4.85,
          "change_percent": -0.2,
          "recommendation": "buy",
          "total_score": 0.78
        },
        {
          "code": "00700",
          "name": "腾讯控股",
          "current_price": 412.5,
          "change_percent": -1.5,
          "recommendation": "buy",
          "total_score": 0.75
        }
      ]
    },
    "portfolio_risk": "medium",
    "investment_suggestions": ["适度配置银行股", "关注消费龙头", "控制仓位风险"],
    "version": "1.0"
  },
  
  market_timing: {
    "analysis_time": "2025-08-24 14:58:19",
    "market_sentiment": "neutral",
    "recommended_position": 0.6,
    "signals": [
      "技术面显示震荡趋势",
      "基本面配置价值显现",
      "资金面相对宽松"
    ],
    "timing_indicators": {
      "technical": {
        "rsi": 55.2,
        "macd": "金叉形态",
        "ma20_ma60": "多头排列",
        "score": 0.65
      },
      "fundamental": {
        "pe_percentile": 45.8,
        "pb_percentile": 38.2,
        "earnings_growth": 8.5,
        "score": 0.72
      },
      "sentiment": {
        "vix_equivalent": 22.5,
        "margin_trading": "温和增长",
        "new_account": "持平上月",
        "score": 0.58
      }
    },
    "overall_score": 0.65,
    "position_advice": {
      "current": 0.6,
      "target": 0.6,
      "action": "维持",
      "reason": "综合评分0.7，市场情绪neutral"
    },
    "risk_warning": [
      "关注美联储政策变化",
      "注意地缘政治风险",
      "警惕个股业绩地雷"
    ]
  },
  
  stocks_a: {
    "update_time": "2025-08-24 14:58:19",
    "total_count": 12,
    "filtered_count": 12,
    "stocks": [
      {
        "code": "000001",
        "name": "平安银行",
        "market_type": "A",
        "current_price": 12.85,
        "change_percent": -0.8,
        "volume": 45230000,
        "market_cap": 248500000000,
        "pe_ratio": 5.2,
        "pb_ratio": 1.05,
        "ps_ratio": 2.1,
        "roe": 12.5,
        "roa": 0.8,
        "debt_ratio": 0.82,
        "dividend_yield": 3.2,
        "industry": "银行",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.8,
          "growth": 0.7,
          "profitability": 0.75,
          "safety": 0.6
        },
        "total_score": 0.75,
        "recommendation": "buy",
        "target_price": 14.50,
        "stop_loss": 11.00,
        "reason": "PE估值偏低，ROE12.5%表现优秀，银行行业配置价值显现"
      },
      {
        "code": "600036",
        "name": "招商银行",
        "market_type": "A",
        "current_price": 43.12,
        "change_percent": 1.2,
        "volume": 28560000,
        "market_cap": 1086000000000,
        "pe_ratio": 6.1,
        "pb_ratio": 1.05,
        "ps_ratio": 3.5,
        "roe": 16.2,
        "roa": 1.2,
        "debt_ratio": 0.82,
        "dividend_yield": 4.1,
        "industry": "银行",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.85,
          "growth": 0.8,
          "profitability": 0.85,
          "safety": 0.75
        },
        "total_score": 0.82,
        "recommendation": "strong_buy",
        "target_price": 48.00,
        "stop_loss": 37.00,
        "reason": "PE估值偏低，ROE16.2%表现优秀，分红收益率4.1%较高，银行行业配置价值显现"
      },
      {
        "code": "600519",
        "name": "贵州茅台",
        "market_type": "A",
        "current_price": 1685.50,
        "change_percent": 0.8,
        "volume": 8520000,
        "market_cap": 2118000000000,
        "pe_ratio": 28.5,
        "pb_ratio": 8.2,
        "ps_ratio": 15.6,
        "roe": 32.8,
        "roa": 22.5,
        "debt_ratio": 0.12,
        "dividend_yield": 1.5,
        "industry": "食品饮料",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.4,
          "growth": 0.95,
          "profitability": 0.95,
          "safety": 0.9
        },
        "total_score": 0.78,
        "recommendation": "buy",
        "target_price": 1750.00,
        "stop_loss": 1450.00,
        "reason": "ROE32.8%表现卓越，负债率12.0%极低，白酒龙头品牌价值突出"
      },
      {
        "code": "000858",
        "name": "五粮液",
        "market_type": "A",
        "current_price": 152.3,
        "change_percent": 2.1,
        "volume": 15420000,
        "market_cap": 589800000000,
        "pe_ratio": 18.5,
        "pb_ratio": 3.2,
        "ps_ratio": 8.9,
        "roe": 22.1,
        "roa": 15.2,
        "debt_ratio": 0.25,
        "dividend_yield": 2.8,
        "industry": "食品饮料",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.6,
          "growth": 0.9,
          "profitability": 0.9,
          "safety": 0.8
        },
        "total_score": 0.78,
        "recommendation": "strong_buy",
        "target_price": 168.00,
        "stop_loss": 130.00,
        "reason": "ROE22.1%表现优秀，负债率25.0%较低，食品饮料行业配置价值显现"
      },
      {
        "code": "300750",
        "name": "宁德时代",
        "market_type": "A",
        "current_price": 185.8,
        "change_percent": -1.5,
        "volume": 38620000,
        "market_cap": 815600000000,
        "pe_ratio": 35.2,
        "pb_ratio": 4.8,
        "ps_ratio": 3.2,
        "roe": 18.5,
        "roa": 8.2,
        "debt_ratio": 0.45,
        "dividend_yield": 0.8,
        "industry": "新能源",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.3,
          "growth": 0.8,
          "profitability": 0.8,
          "safety": 0.7
        },
        "total_score": 0.62,
        "recommendation": "hold",
        "target_price": 195.00,
        "stop_loss": 160.00,
        "reason": "新能源龙头，成长性好但估值偏高"
      },
      {
        "code": "002415",
        "name": "海康威视",
        "market_type": "A",
        "current_price": 32.5,
        "change_percent": 0.5,
        "volume": 22340000,
        "market_cap": 302800000000,
        "pe_ratio": 15.8,
        "pb_ratio": 2.1,
        "ps_ratio": 4.2,
        "roe": 18.5,
        "roa": 12.8,
        "debt_ratio": 0.28,
        "dividend_yield": 2.1,
        "industry": "科技",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.75,
          "growth": 0.8,
          "profitability": 0.8,
          "safety": 0.75
        },
        "total_score": 0.77,
        "recommendation": "buy",
        "target_price": 36.00,
        "stop_loss": 28.00,
        "reason": "PE估值合理，ROE18.5%表现优秀，科技龙头地位稳固"
      },
      {
        "code": "600276",
        "name": "恒瑞医药",
        "market_type": "A",
        "current_price": 45.8,
        "change_percent": -0.2,
        "volume": 18500000,
        "market_cap": 196800000000,
        "pe_ratio": 22.5,
        "pb_ratio": 3.8,
        "ps_ratio": 7.2,
        "roe": 16.8,
        "roa": 12.5,
        "debt_ratio": 0.18,
        "dividend_yield": 1.8,
        "industry": "医药",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.6,
          "growth": 0.75,
          "profitability": 0.8,
          "safety": 0.85
        },
        "total_score": 0.73,
        "recommendation": "buy",
        "target_price": 50.00,
        "stop_loss": 40.00,
        "reason": "ROE16.8%稳健，负债率18.0%较低，医药创新龙头"
      },
      {
        "code": "000333",
        "name": "美的集团",
        "market_type": "A",
        "current_price": 58.2,
        "change_percent": 1.8,
        "volume": 25680000,
        "market_cap": 408600000000,
        "pe_ratio": 12.8,
        "pb_ratio": 2.5,
        "ps_ratio": 1.2,
        "roe": 25.2,
        "roa": 8.5,
        "debt_ratio": 0.52,
        "dividend_yield": 3.5,
        "industry": "家电",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.85,
          "growth": 0.9,
          "profitability": 0.9,
          "safety": 0.7
        },
        "total_score": 0.83,
        "recommendation": "strong_buy",
        "target_price": 65.00,
        "stop_loss": 50.00,
        "reason": "PE估值偏低，ROE25.2%表现卓越，分红收益率3.5%较高"
      },
      {
        "code": "002594",
        "name": "比亚迪",
        "market_type": "A",
        "current_price": 268.5,
        "change_percent": -2.1,
        "volume": 45680000,
        "market_cap": 780500000000,
        "pe_ratio": 28.8,
        "pb_ratio": 4.2,
        "ps_ratio": 2.8,
        "roe": 20.5,
        "roa": 6.8,
        "debt_ratio": 0.58,
        "dividend_yield": 0.5,
        "industry": "新能源汽车",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.4,
          "growth": 0.85,
          "profitability": 0.85,
          "safety": 0.6
        },
        "total_score": 0.68,
        "recommendation": "hold",
        "target_price": 285.00,
        "stop_loss": 230.00,
        "reason": "新能源汽车龙头，成长性强但估值偏高"
      },
      {
        "code": "000651",
        "name": "格力电器",
        "market_type": "A",
        "current_price": 35.8,
        "change_percent": 0.8,
        "volume": 32580000,
        "market_cap": 203500000000,
        "pe_ratio": 9.5,
        "pb_ratio": 1.8,
        "ps_ratio": 1.0,
        "roe": 22.8,
        "roa": 15.2,
        "debt_ratio": 0.48,
        "dividend_yield": 4.2,
        "industry": "家电",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.9,
          "growth": 0.9,
          "profitability": 0.9,
          "safety": 0.7
        },
        "total_score": 0.85,
        "recommendation": "strong_buy",
        "target_price": 42.00,
        "stop_loss": 31.00,
        "reason": "PE估值极低，ROE22.8%表现卓越，分红收益率4.2%很高"
      },
      {
        "code": "300015",
        "name": "爱尔眼科",
        "market_type": "A",
        "current_price": 18.5,
        "change_percent": 1.2,
        "volume": 28650000,
        "market_cap": 125800000000,
        "pe_ratio": 32.5,
        "pb_ratio": 5.2,
        "ps_ratio": 8.5,
        "roe": 15.8,
        "roa": 8.2,
        "debt_ratio": 0.35,
        "dividend_yield": 0.8,
        "industry": "医疗服务",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.3,
          "growth": 0.75,
          "profitability": 0.75,
          "safety": 0.75
        },
        "total_score": 0.62,
        "recommendation": "hold",
        "target_price": 20.00,
        "stop_loss": 16.00,
        "reason": "医疗服务龙头，成长确定但估值较高"
      },
      {
        "code": "601318",
        "name": "中国平安",
        "market_type": "A",
        "current_price": 42.8,
        "change_percent": -0.5,
        "volume": 35680000,
        "market_cap": 780500000000,
        "pe_ratio": 8.2,
        "pb_ratio": 0.9,
        "ps_ratio": 0.6,
        "roe": 15.5,
        "roa": 1.2,
        "debt_ratio": 0.75,
        "dividend_yield": 4.8,
        "industry": "保险",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.9,
          "growth": 0.7,
          "profitability": 0.8,
          "safety": 0.6
        },
        "total_score": 0.76,
        "recommendation": "buy",
        "target_price": 48.00,
        "stop_loss": 37.00,
        "reason": "PE估值极低，分红收益率4.8%很高，保险龙头配置价值显现"
      }
    ]
  },
  
  stocks_hk: {
    "update_time": "2025-08-24 14:58:19",
    "total_count": 8,
    "filtered_count": 8,
    "stocks": [
      {
        "code": "00700",
        "name": "腾讯控股",
        "market_type": "HK",
        "current_price": 412.5,
        "change_percent": -1.5,
        "volume": 18500000,
        "market_cap": 3950000000000,
        "pe_ratio": 15.8,
        "pb_ratio": 2.1,
        "ps_ratio": 4.2,
        "roe": 18.5,
        "roa": 8.2,
        "debt_ratio": 0.15,
        "dividend_yield": 1.8,
        "industry": "互联网科技",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.7,
          "growth": 0.8,
          "profitability": 0.8,
          "safety": 0.85
        },
        "total_score": 0.75,
        "recommendation": "buy",
        "target_price": 450.00,
        "stop_loss": 350.00,
        "reason": "ROE18.5%表现优秀，负债率15.0%较低"
      },
      {
        "code": "09988",
        "name": "阿里巴巴",
        "market_type": "HK",
        "current_price": 78.5,
        "change_percent": 0.8,
        "volume": 25680000,
        "market_cap": 1580000000000,
        "pe_ratio": 12.5,
        "pb_ratio": 1.8,
        "ps_ratio": 2.1,
        "roe": 12.8,
        "roa": 6.5,
        "debt_ratio": 0.25,
        "dividend_yield": 0.0,
        "industry": "互联网科技",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.8,
          "growth": 0.7,
          "profitability": 0.7,
          "safety": 0.8
        },
        "total_score": 0.74,
        "recommendation": "buy",
        "target_price": 88.00,
        "stop_loss": 68.00,
        "reason": "PE估值偏低，互联网龙头回调后配置价值显现"
      },
      {
        "code": "03690",
        "name": "美团",
        "market_type": "HK",
        "current_price": 135.8,
        "change_percent": 1.8,
        "volume": 32580000,
        "market_cap": 825600000000,
        "pe_ratio": 28.5,
        "pb_ratio": 3.2,
        "ps_ratio": 3.8,
        "roe": 15.2,
        "roa": 4.8,
        "debt_ratio": 0.18,
        "dividend_yield": 0.0,
        "industry": "互联网科技",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.4,
          "growth": 0.8,
          "profitability": 0.75,
          "safety": 0.85
        },
        "total_score": 0.68,
        "recommendation": "hold",
        "target_price": 145.00,
        "stop_loss": 115.00,
        "reason": "本地生活龙头，成长性强但估值偏高"
      },
      {
        "code": "01398",
        "name": "工商银行",
        "market_type": "HK",
        "current_price": 4.85,
        "change_percent": -0.2,
        "volume": 52680000,
        "market_cap": 425800000000,
        "pe_ratio": 4.2,
        "pb_ratio": 0.42,
        "ps_ratio": 1.1,
        "roe": 12.8,
        "roa": 1.0,
        "debt_ratio": 0.88,
        "dividend_yield": 6.2,
        "industry": "银行",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.95,
          "growth": 0.7,
          "profitability": 0.8,
          "safety": 0.5
        },
        "total_score": 0.78,
        "recommendation": "buy",
        "target_price": 5.50,
        "stop_loss": 4.20,
        "reason": "PE估值极低，分红收益率6.2%很高，港股银行配置价值突出"
      },
      {
        "code": "01211",
        "name": "比亚迪股份",
        "market_type": "HK",
        "current_price": 228.5,
        "change_percent": -2.5,
        "volume": 15680000,
        "market_cap": 665800000000,
        "pe_ratio": 25.8,
        "pb_ratio": 3.8,
        "ps_ratio": 2.5,
        "roe": 18.5,
        "roa": 5.8,
        "debt_ratio": 0.52,
        "dividend_yield": 0.8,
        "industry": "新能源汽车",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.45,
          "growth": 0.8,
          "profitability": 0.8,
          "safety": 0.7
        },
        "total_score": 0.72,
        "recommendation": "buy",
        "target_price": 250.00,
        "stop_loss": 200.00,
        "reason": "新能源汽车全球龙头，港股估值相对合理"
      },
      {
        "code": "01299",
        "name": "友邦保险",
        "market_type": "HK",
        "current_price": 52.8,
        "change_percent": 0.5,
        "volume": 8520000,
        "market_cap": 625800000000,
        "pe_ratio": 12.5,
        "pb_ratio": 1.8,
        "ps_ratio": 2.1,
        "roe": 16.8,
        "roa": 2.1,
        "debt_ratio": 0.78,
        "dividend_yield": 3.8,
        "industry": "保险",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.75,
          "growth": 0.75,
          "profitability": 0.8,
          "safety": 0.6
        },
        "total_score": 0.73,
        "recommendation": "buy",
        "target_price": 58.00,
        "stop_loss": 46.00,
        "reason": "PE估值合理，分红收益率3.8%较高，亚洲保险龙头"
      },
      {
        "code": "00175",
        "name": "吉利汽车",
        "market_type": "HK",
        "current_price": 8.85,
        "change_percent": 1.2,
        "volume": 45680000,
        "market_cap": 86500000000,
        "pe_ratio": 18.5,
        "pb_ratio": 1.2,
        "ps_ratio": 0.8,
        "roe": 8.5,
        "roa": 3.2,
        "debt_ratio": 0.48,
        "dividend_yield": 2.2,
        "industry": "汽车",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.7,
          "growth": 0.6,
          "profitability": 0.6,
          "safety": 0.7
        },
        "total_score": 0.65,
        "recommendation": "hold",
        "target_price": 10.00,
        "stop_loss": 7.50,
        "reason": "传统车企转型，估值合理但转型存不确定性"
      },
      {
        "code": "00941",
        "name": "中国移动",
        "market_type": "HK",
        "current_price": 68.5,
        "change_percent": 0.2,
        "volume": 12580000,
        "market_cap": 1425800000000,
        "pe_ratio": 9.8,
        "pb_ratio": 0.8,
        "ps_ratio": 1.5,
        "roe": 9.2,
        "roa": 3.8,
        "debt_ratio": 0.32,
        "dividend_yield": 5.5,
        "industry": "电信运营商",
        "update_time": "2025-08-24 14:58:19",
        "data_source": "realistic_mock",
        "scores": {
          "valuation": 0.85,
          "growth": 0.5,
          "profitability": 0.7,
          "safety": 0.8
        },
        "total_score": 0.71,
        "recommendation": "buy",
        "target_price": 75.00,
        "stop_loss": 60.00,
        "reason": "PE估值偏低，分红收益率5.5%很高，5G基建价值凸显"
      }
    ]
  },
  
  stocks_a_recommendations: [
    {
      "code": "000651",
      "name": "格力电器",
      "market_type": "A",
      "current_price": 35.8,
      "change_percent": 0.8,
      "total_score": 0.85,
      "recommendation": "strong_buy"
    },
    {
      "code": "000333",
      "name": "美的集团",
      "market_type": "A",
      "current_price": 58.2,
      "change_percent": 1.8,
      "total_score": 0.83,
      "recommendation": "strong_buy"
    },
    {
      "code": "600036", 
      "name": "招商银行",
      "market_type": "A",
      "current_price": 43.12,
      "change_percent": 1.2,
      "total_score": 0.82,
      "recommendation": "strong_buy"
    },
    {
      "code": "600519",
      "name": "贵州茅台",
      "market_type": "A",
      "current_price": 1685.50,
      "change_percent": 0.8,
      "total_score": 0.78,
      "recommendation": "buy"
    },
    {
      "code": "000858",
      "name": "五粮液", 
      "market_type": "A",
      "current_price": 152.3,
      "change_percent": 2.1,
      "total_score": 0.78,
      "recommendation": "strong_buy"
    },
    {
      "code": "002415",
      "name": "海康威视",
      "market_type": "A",
      "current_price": 32.5,
      "change_percent": 0.5,
      "total_score": 0.77,
      "recommendation": "buy"
    },
    {
      "code": "601318",
      "name": "中国平安",
      "market_type": "A",
      "current_price": 42.8,
      "change_percent": -0.5,
      "total_score": 0.76,
      "recommendation": "buy"
    },
    {
      "code": "000001",
      "name": "平安银行",
      "market_type": "A",
      "current_price": 12.85,
      "change_percent": -0.8,
      "total_score": 0.75,
      "recommendation": "buy"
    }
  ],
  
  stocks_hk_recommendations: [
    {
      "code": "01398",
      "name": "工商银行",
      "market_type": "HK",
      "current_price": 4.85,
      "change_percent": -0.2,
      "total_score": 0.78,
      "recommendation": "buy"
    },
    {
      "code": "00700",
      "name": "腾讯控股",
      "market_type": "HK", 
      "current_price": 412.5,
      "change_percent": -1.5,
      "total_score": 0.75,
      "recommendation": "buy"
    },
    {
      "code": "09988",
      "name": "阿里巴巴",
      "market_type": "HK",
      "current_price": 78.5,
      "change_percent": 0.8,
      "total_score": 0.74,
      "recommendation": "buy"
    },
    {
      "code": "01299",
      "name": "友邦保险",
      "market_type": "HK",
      "current_price": 52.8,
      "change_percent": 0.5,
      "total_score": 0.73,
      "recommendation": "buy"
    },
    {
      "code": "01211",
      "name": "比亚迪股份",
      "market_type": "HK",
      "current_price": 228.5,
      "change_percent": -2.5,
      "total_score": 0.72,
      "recommendation": "buy"
    },
    {
      "code": "00941",
      "name": "中国移动",
      "market_type": "HK",
      "current_price": 68.5,
      "change_percent": 0.2,
      "total_score": 0.71,
      "recommendation": "buy"
    }
  ],
  
  analysis_samples: {
    "update_time": "2025-08-24 14:58:19",
    "total_count": 8,
    "analysis_results": [
      {
        "basic_info": {
          "code": "000651",
          "name": "格力电器",
          "industry": "家电",
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 35.8,
          "pe_ratio": 9.5,
          "pb_ratio": 1.8,
          "roe": 22.8,
          "debt_ratio": 0.48
        },
        "analysis_result": {
          "total_score": 0.85,
          "recommendation": "strong_buy",
          "reason": "PE估值极低，ROE22.8%表现卓越，分红收益率4.2%很高"
        }
      },
      {
        "basic_info": {
          "code": "000333",
          "name": "美的集团",
          "industry": "家电",
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 58.2,
          "pe_ratio": 12.8,
          "pb_ratio": 2.5,
          "roe": 25.2,
          "debt_ratio": 0.52
        },
        "analysis_result": {
          "total_score": 0.83,
          "recommendation": "strong_buy",
          "reason": "PE估值偏低，ROE25.2%表现卓越，分红收益率3.5%较高"
        }
      },
      {
        "basic_info": {
          "code": "600036",
          "name": "招商银行", 
          "industry": "银行",
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 43.12,
          "pe_ratio": 6.1,
          "pb_ratio": 1.05,
          "roe": 16.2,
          "debt_ratio": 0.82
        },
        "analysis_result": {
          "total_score": 0.82,
          "recommendation": "strong_buy",
          "reason": "ROE16.2%表现优秀，银行行业配置价值显现"
        }
      },
      {
        "basic_info": {
          "code": "600519",
          "name": "贵州茅台",
          "industry": "食品饮料", 
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 1685.50,
          "pe_ratio": 28.5,
          "pb_ratio": 8.2,
          "roe": 32.8,
          "debt_ratio": 0.12
        },
        "analysis_result": {
          "total_score": 0.78,
          "recommendation": "buy",
          "reason": "ROE32.8%表现卓越，负债率12.0%极低，白酒龙头品牌价值突出"
        }
      },
      {
        "basic_info": {
          "code": "01398",
          "name": "工商银行",
          "industry": "银行", 
          "market_type": "HK"
        },
        "financial_data": {
          "current_price": 4.85,
          "pe_ratio": 4.2,
          "pb_ratio": 0.42,
          "roe": 12.8,
          "debt_ratio": 0.88
        },
        "analysis_result": {
          "total_score": 0.78,
          "recommendation": "buy",
          "reason": "PE估值极低，分红收益率6.2%很高，港股银行配置价值突出"
        }
      },
      {
        "basic_info": {
          "code": "002415",
          "name": "海康威视",
          "industry": "科技",
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 32.5,
          "pe_ratio": 15.8,
          "pb_ratio": 2.1,
          "roe": 18.5,
          "debt_ratio": 0.28
        },
        "analysis_result": {
          "total_score": 0.77,
          "recommendation": "buy",
          "reason": "PE估值合理，ROE18.5%表现优秀，科技龙头地位稳固"
        }
      },
      {
        "basic_info": {
          "code": "00700",
          "name": "腾讯控股",
          "industry": "互联网科技",
          "market_type": "HK"
        },
        "financial_data": {
          "current_price": 412.5,
          "pe_ratio": 15.8,
          "pb_ratio": 2.1,
          "roe": 18.5,
          "debt_ratio": 0.15
        },
        "analysis_result": {
          "total_score": 0.75,
          "recommendation": "buy",
          "reason": "ROE18.5%表现优秀，负债率15.0%较低，港股科技龙头"
        }
      },
      {
        "basic_info": {
          "code": "000001",
          "name": "平安银行",
          "industry": "银行",
          "market_type": "A"
        },
        "financial_data": {
          "current_price": 12.85,
          "pe_ratio": 5.2,
          "pb_ratio": 1.05,
          "roe": 12.5,
          "debt_ratio": 0.82
        },
        "analysis_result": {
          "total_score": 0.75,
          "recommendation": "buy",
          "reason": "PE估值偏低，ROE12.5%表现优秀"
        }
      }
    ]
  },
  
  laoliu_quotes: {
    "version": "1.0.0",
    "categories": {
      "masters": {
        "name": "投资大师",
        "quotes": [
          {
            "id": "m001",
            "content": "败于原价，死于抄底，终于杠杆",
            "author": "老刘投资笔记"
          },
          {
            "id": "m002", 
            "content": "人弃我取，人取我弃",
            "author": "老刘投资笔记"
          },
          {
            "id": "m003",
            "content": "买股票就是买公司，买公司就是买未来",
            "author": "老刘投资笔记"
          }
        ]
      },
      "risk": {
        "name": "风险控制",
        "quotes": [
          {
            "id": "r001",
            "content": "不要把所有鸡蛋放在一个篮子里",
            "author": "老刘投资笔记"
          },
          {
            "id": "r002",
            "content": "投资有风险，入市需谨慎",
            "author": "老刘投资笔记"
          }
        ]
      }
    }
  }
}

module.exports = mockData