// 开发环境Mock数据
const mockData = {
  summary: {
    "update_time": "2025-08-19 21:30:00",
    "market_status": {
      "sentiment": "neutral",
      "position_suggestion": 0.5,
      "signals": [
        "上证指数在3000点附近震荡",
        "成交量相比上周略有增加", 
        "银行股表现相对稳定"
      ]
    },
    "recommendations_count": {
      "a_stocks": 8,
      "hk_stocks": 5,
      "total": 13
    },
    "top_picks": {
      "a_stocks": [
        {
          "code": "000001",
          "name": "平安银行",
          "current_price": 13.25,
          "change_percent": 1.2,
          "recommendation": "buy",
          "total_score": 0.75,
          "pe_ratio": 5.2,
          "pb_ratio": 0.68,
          "roe": 12.8,
          "reason": "PE估值偏低，ROE稳定，银行股配置价值显现"
        },
        {
          "code": "600036",
          "name": "招商银行",
          "current_price": 42.80,
          "change_percent": 0.8,
          "recommendation": "buy",
          "total_score": 0.82,
          "pe_ratio": 6.1,
          "pb_ratio": 1.05,
          "roe": 16.2,
          "reason": "银行业龙头，资产质量优秀，分红稳定"
        },
        {
          "code": "000858",
          "name": "五粮液",
          "current_price": 162.50,
          "change_percent": -0.5,
          "recommendation": "hold",
          "total_score": 0.68,
          "pe_ratio": 28.5,
          "pb_ratio": 5.2,
          "roe": 24.1,
          "reason": "白酒龙头，品牌价值突出，但估值偏高"
        }
      ],
      "hk_stocks": [
        {
          "code": "00700",
          "name": "腾讯控股",
          "current_price": 368.20,
          "change_percent": 2.1,
          "recommendation": "buy",
          "total_score": 0.78,
          "pe_ratio": 15.6,
          "pb_ratio": 3.2,
          "roe": 18.9,
          "reason": "互联网龙头，游戏业务复苏，AI布局积极"
        },
        {
          "code": "00941",
          "name": "中国移动",
          "current_price": 72.15,
          "change_percent": 1.5,
          "recommendation": "buy",
          "total_score": 0.71,
          "pe_ratio": 12.8,
          "pb_ratio": 1.1,
          "roe": 8.6,
          "reason": "运营商龙头，5G建设受益，分红收益率高"
        }
      ]
    },
    "portfolio_risk": "medium",
    "investment_suggestions": [
      "当前市场情绪中性，建议保持5成仓位",
      "重点关注估值偏低的银行股配置机会",
      "港股腾讯等科技股出现反弹信号",
      "控制单一股票仓位不超过总资金20%",
      "密切关注美联储政策变化对A股的影响"
    ]
  },
  
  market_timing: {
    "update_time": "2025-08-19 21:30:00",
    "market_phase": "震荡市",
    "position_suggestion": 0.5,
    "sentiment_score": 0.48,
    "timing_signals": [
      {
        "name": "技术面",
        "signal": "neutral",
        "score": 0.5,
        "description": "上证指数在3000点附近整理"
      },
      {
        "name": "资金面",
        "signal": "positive",
        "score": 0.6,
        "description": "北向资金持续流入"
      },
      {
        "name": "政策面",
        "signal": "neutral",
        "score": 0.5,
        "description": "政策预期相对平稳"
      },
      {
        "name": "估值面",
        "signal": "positive",
        "score": 0.65,
        "description": "A股整体估值处于历史中低位"
      }
    ],
    "recommendations": [
      "当前位置可适度配置，建议仓位控制在5成左右",
      "重点关注低估值蓝筹股的配置机会",
      "密切关注美联储政策变化对市场的影响"
    ]
  },
  
  stocks_a: {
    "update_time": "2025-08-19 21:30:00",
    "total_count": 8,
    "stocks": [
      {
        "code": "000001",
        "name": "平安银行",
        "current_price": 13.25,
        "change_percent": 1.2,
        "pe_ratio": 5.2,
        "pb_ratio": 0.68,
        "roe": 12.8,
        "debt_ratio": 0.15,
        "recommendation": "buy",
        "total_score": 0.75,
        "valuation_score": 0.85,
        "growth_score": 0.65,
        "profitability_score": 0.78,
        "safety_score": 0.72,
        "industry": "银行",
        "market_cap": 256800000000,
        "reasons": [
          "PE估值偏低，仅5.2倍",
          "ROE维持在12.8%的较高水平",
          "银行股配置价值显现"
        ],
        "risks": [
          "信贷风险需关注",
          "利率环境变化影响"
        ]
      },
      {
        "code": "600036",
        "name": "招商银行",
        "current_price": 42.80,
        "change_percent": 0.8,
        "pe_ratio": 6.1,
        "pb_ratio": 1.05,
        "roe": 16.2,
        "debt_ratio": 0.12,
        "recommendation": "buy",
        "total_score": 0.82,
        "valuation_score": 0.78,
        "growth_score": 0.75,
        "profitability_score": 0.88,
        "safety_score": 0.85,
        "industry": "银行",
        "market_cap": 1256000000000,
        "reasons": [
          "银行业龙头，资产质量优秀",
          "ROE高达16.2%，盈利能力突出",
          "分红稳定，股息率吸引"
        ],
        "risks": [
          "估值相对较高",
          "经济周期影响"
        ]
      }
    ]
  },
  
  stocks_hk: {
    "update_time": "2025-08-19 21:30:00",
    "total_count": 5,
    "stocks": [
      {
        "code": "00700",
        "name": "腾讯控股",
        "current_price": 368.20,
        "change_percent": 2.1,
        "pe_ratio": 15.6,
        "pb_ratio": 3.2,
        "roe": 18.9,
        "debt_ratio": 0.08,
        "recommendation": "buy",
        "total_score": 0.78,
        "valuation_score": 0.72,
        "growth_score": 0.85,
        "profitability_score": 0.82,
        "safety_score": 0.75,
        "industry": "互联网",
        "market_cap": 3528000000000,
        "reasons": [
          "互联网龙头，游戏业务复苏",
          "AI布局积极，长期成长性强",
          "现金流充沛，财务健康"
        ],
        "risks": [
          "监管环境变化",
          "竞争加剧"
        ]
      }
    ]
  },
  
  laoliu_quotes: {
    "version": "1.0.0",
    "last_updated": "2025-08-21",
    "total_quotes": 17,
    "daily_rotation": {
      "current_index": 0,
      "update_interval": 24,
      "last_update": "2025-08-21 13:19:23"
    },
    "categories": {
      "masters": {
        "name": "投资大师",
        "icon": "🎯",
        "description": "汲取投资大师的智慧结晶",
        "count": 5,
        "quotes": [
          {
            "id": "m001",
            "content": "败于原价，死于抄底，终于杠杆",
            "author": "格雷厄姆",
            "source_page": 1,
            "tags": ["风险控制", "经典名言"],
            "category": "masters"
          },
          {
            "id": "m002",
            "content": "我们宁愿以低廉的价格买入一个伟大的公司，也不愿以一个伟大的价格买入一个普通的公司",
            "author": "巴菲特理念",
            "source_page": 2,
            "tags": ["价值投资", "选股原则"],
            "category": "masters"
          }
        ]
      },
      "strategies": {
        "name": "投资策略",
        "icon": "📈",
        "description": "实用的投资策略和技巧",
        "count": 6,
        "quotes": [
          {
            "id": "s001",
            "content": "选择高ROE公司进行长期投资",
            "author": "老刘笔记",
            "source_page": 5,
            "tags": ["选股标准", "ROE"],
            "category": "strategies"
          },
          {
            "id": "s002",
            "content": "分批建仓，控制风险",
            "author": "老刘笔记",
            "source_page": 8,
            "tags": ["建仓策略", "风险控制"],
            "category": "strategies"
          }
        ]
      },
      "philosophy": {
        "name": "市场哲学",
        "icon": "💭",
        "description": "对市场的深度思考和哲学感悟",
        "count": 6,
        "quotes": [
          {
            "id": "p001",
            "content": "市场总是在绝望中见底，在希望中上涨，在疯狂中见顶",
            "author": "市场智慧",
            "source_page": 12,
            "tags": ["市场周期", "情绪指标"],
            "category": "philosophy"
          },
          {
            "id": "p002",
            "content": "时间是价值投资者的朋友",
            "author": "投资哲学",
            "source_page": 15,
            "tags": ["时间价值", "长期投资"],
            "category": "philosophy"
          }
        ]
      }
    }
  },
  
  miniprogram_config: {
    "version": "1.0.0",
    "app_name": "老刘投资决策",
    "update_frequency": "daily",
    "data_sources": [
      "A股数据",
      "港股数据", 
      "投资金句"
    ],
    "api_endpoints": {
      "summary": "/summary.json",
      "stocks_a": "/stocks_a.json",
      "stocks_hk": "/stocks_hk.json",
      "market_timing": "/market_timing.json",
      "quotes": "/laoliu_quotes.json"
    },
    "cache_duration": 3600,
    "features": {
      "quotes_rotation": true,
      "share_cards": true,
      "offline_mode": true
    }
  }
};

module.exports = mockData;