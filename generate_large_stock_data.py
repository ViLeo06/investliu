#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成大量股票数据 - 基于老刘投资理念的完整股票数据库
"""

import json
import random
import time
from datetime import datetime

# 根据老刘投资笔记扩展的股票池
def generate_comprehensive_stock_data():
    """生成包含大量股票的数据"""
    print("开始生成大量股票数据...")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 扩展A股股票池（基于各行业龙头和老刘偏好）
    a_stock_universe = [
        # 银行股 - 老刘重视的价值股
        ("000001", "平安银行", "银行", 13.45, 5.2, 0.68, 12.8),
        ("600036", "招商银行", "银行", 43.12, 6.1, 1.05, 16.2),
        ("600000", "浦发银行", "银行", 8.76, 4.8, 0.55, 11.5),
        ("601166", "兴业银行", "银行", 17.89, 5.5, 0.72, 13.4),
        ("002142", "宁波银行", "银行", 34.56, 8.9, 1.1, 18.7),
        ("600016", "民生银行", "银行", 4.23, 3.8, 0.45, 8.9),
        ("601398", "工商银行", "银行", 5.12, 4.2, 0.58, 12.1),
        ("601939", "建设银行", "银行", 6.78, 4.5, 0.62, 11.8),
        ("601288", "农业银行", "银行", 3.89, 3.9, 0.48, 10.2),
        ("601328", "交通银行", "银行", 5.34, 3.5, 0.52, 9.8),
        
        # 食品饮料 - 消费龙头
        ("600519", "贵州茅台", "食品饮料", 1876.50, 32.5, 8.9, 28.1),
        ("000858", "五粮液", "食品饮料", 142.80, 18.5, 4.2, 22.3),
        ("002304", "洋河股份", "食品饮料", 98.65, 15.2, 3.1, 18.9),
        ("600809", "山西汾酒", "食品饮料", 156.78, 25.8, 5.6, 24.7),
        ("000568", "泸州老窖", "食品饮料", 189.34, 22.1, 4.8, 26.2),
        ("600887", "伊利股份", "食品饮料", 28.45, 19.8, 2.9, 20.1),
        ("000895", "双汇发展", "食品饮料", 32.67, 14.2, 2.1, 16.8),
        ("603288", "海天味业", "食品饮料", 78.90, 28.5, 6.2, 25.4),
        
        # 医药生物 - 高ROE行业
        ("600276", "恒瑞医药", "医药", 45.67, 28.9, 3.5, 15.6),
        ("000661", "长春高新", "医药", 156.78, 18.2, 2.8, 22.4),
        ("300015", "爱尔眼科", "医药", 12.34, 35.6, 4.1, 18.9),
        ("300760", "迈瑞医疗", "医药", 298.45, 45.2, 8.9, 26.7),
        ("002821", "凯莱英", "医药", 89.12, 28.1, 3.4, 19.8),
        ("300122", "智飞生物", "医药", 67.89, 15.8, 2.9, 35.2),
        
        # 科技股 - 跟热点走
        ("002415", "海康威视", "科技", 34.56, 18.9, 2.1, 24.3),
        ("300059", "东方财富", "科技", 16.78, 22.4, 1.8, 28.9),
        ("000063", "中兴通讯", "科技", 28.90, 25.6, 2.8, 16.7),
        ("002230", "科大讯飞", "科技", 45.67, 68.9, 4.2, 8.9),
        ("300750", "宁德时代", "科技", 198.76, 28.9, 5.4, 22.1),
        
        # 新能源汽车
        ("002594", "比亚迪", "新能源", 178.90, 15.6, 2.8, 18.9),
        ("002460", "赣锋锂业", "新能源", 34.56, 12.8, 1.9, 22.4),
        
        # 消费电子
        ("000651", "格力电器", "家电", 34.78, 11.2, 1.5, 15.6),
        ("000333", "美的集团", "家电", 56.89, 12.8, 2.1, 18.9),
        ("600690", "海尔智家", "家电", 23.45, 10.9, 1.8, 14.2),
        
        # 房地产
        ("000002", "万科A", "房地产", 8.90, 6.8, 0.8, 8.9),
        ("001979", "招商蛇口", "房地产", 12.34, 5.9, 0.9, 7.8),
        
        # 保险证券
        ("601318", "中国平安", "保险", 45.67, 7.8, 1.2, 16.8),
        ("601601", "中国太保", "保险", 28.90, 6.9, 1.1, 14.5),
        ("600030", "中信证券", "证券", 19.78, 12.8, 1.8, 12.4),
        
        # 周期股
        ("601088", "中国神华", "煤炭", 28.90, 6.8, 1.1, 18.9),
        ("600019", "宝钢股份", "钢铁", 5.67, 8.9, 0.9, 12.1),
        ("600585", "海螺水泥", "建材", 32.45, 9.8, 1.4, 15.6)
    ]
    
    # 港股股票池
    hk_stock_universe = [
        # 科技互联网
        ("00700", "腾讯控股", "互联网科技", 378.40, 15.6, 3.2, 18.9),
        ("03690", "美团", "互联网科技", 89.50, 28.9, 4.1, 12.4),
        ("09988", "阿里巴巴", "互联网科技", 78.90, 12.8, 2.1, 15.6),
        ("09618", "京东集团", "互联网科技", 123.45, 18.9, 2.8, 8.9),
        ("01024", "快手", "互联网科技", 45.67, 35.6, 3.4, -5.6),
        
        # 电信运营
        ("00941", "中国移动", "电信运营", 73.25, 12.8, 1.1, 8.6),
        ("00728", "中国电信", "电信运营", 4.12, 11.2, 1.0, 7.8),
        
        # 银行保险
        ("01299", "友邦保险", "保险", 67.80, 14.5, 2.1, 16.8),
        ("02318", "中国平安", "保险", 45.67, 7.8, 1.2, 16.8),
        ("01398", "工商银行", "银行", 5.12, 4.2, 0.58, 12.1),
        ("03988", "中国银行", "银行", 3.67, 3.8, 0.52, 10.8),
        ("03968", "招商银行", "银行", 43.12, 6.1, 1.05, 16.2),
        
        # 汽车制造
        ("00175", "吉利汽车", "汽车", 9.87, 8.9, 1.2, 12.4),
        ("01211", "比亚迪股份", "汽车", 189.45, 15.6, 2.8, 18.9),
        ("02333", "长城汽车", "汽车", 8.90, 12.1, 1.1, 8.7),
        
        # 能源石油
        ("00883", "中国海洋石油", "能源", 18.90, 8.9, 1.1, 15.6),
        ("00386", "中国石油化工", "能源", 4.56, 7.8, 0.9, 12.1),
        
        # 地产建筑
        ("01109", "华润置地", "房地产", 34.56, 8.9, 1.2, 9.8),
        ("00016", "新鸿基地产", "房地产", 89.12, 12.4, 1.8, 11.2),
        
        # 医药生物
        ("01093", "石药集团", "医药", 8.90, 18.9, 1.8, 22.4),
        ("06160", "百济神州", "医药", 89.50, 45.6, 3.4, -8.9),
        
        # 消费零售
        ("06837", "海底捞", "消费", 12.34, 28.9, 2.1, 5.6),
        ("09961", "携程集团", "消费", 256.78, 22.4, 3.8, 18.9),
        
        # 新经济
        ("09992", "泡泡玛特", "消费", 23.45, 45.6, 8.9, 12.4),
        ("02015", "理想汽车", "汽车", 89.12, 28.9, 3.4, -12.1),
        ("09866", "蔚来", "汽车", 45.67, 35.6, 2.8, -15.6),
        ("09868", "小鹏汽车", "汽车", 34.56, 28.9, 2.1, -8.9)
    ]
    
    def generate_stock_analysis(code, name, industry, price, pe, pb, roe, market_type="A"):
        """生成股票分析数据"""
        # 基于老刘理念的评分
        laoliu_score = 0
        analysis_points = []
        risk_warnings = []
        
        # ROE评分
        if roe >= 15:
            laoliu_score += 25
            analysis_points.append(f"ROE达{roe}%，盈利能力强")
        elif roe >= 10:
            laoliu_score += 15
            analysis_points.append(f"ROE为{roe}%，盈利能力较好")
        elif roe > 0:
            laoliu_score += 5
            analysis_points.append(f"ROE为{roe}%，盈利能力一般")
        else:
            risk_warnings.append(f"ROE为{roe}%，存在亏损风险")
        
        # 估值评分
        if pe <= 15:
            laoliu_score += 20
            analysis_points.append(f"PE仅{pe}倍，估值偏低")
        elif pe <= 25:
            laoliu_score += 10
            analysis_points.append(f"PE为{pe}倍，估值合理")
        elif pe > 40:
            risk_warnings.append(f"PE高达{pe}倍，估值偏高")
        
        # 行业权重
        industry_weights = {
            "银行": 1.2, "食品饮料": 1.15, "医药": 1.1, "保险": 1.1,
            "科技": 1.0, "家电": 1.05, "新能源": 0.95, "房地产": 0.8
        }
        weight = industry_weights.get(industry, 1.0)
        laoliu_score = int(laoliu_score * weight)
        
        # 投资建议
        if laoliu_score >= 80:
            recommendation = "strong_buy"
            advice = "强烈推荐：符合老刘多项投资标准"
        elif laoliu_score >= 60:
            recommendation = "buy"
            advice = "推荐：基本面良好，可适当配置"
        elif laoliu_score >= 40:
            recommendation = "hold"
            advice = "观望：存在一定投资价值"
        else:
            recommendation = "sell"
            advice = "回避：不符合老刘投资标准"
        
        # 量价关系分析
        change_percent = round(random.uniform(-5, 5), 2)
        volume = random.randint(10000000, 200000000)
        
        if change_percent > 3 and volume > 50000000:
            volume_price_signal = "放量上涨 - 资金追捧，可关注"
        elif change_percent > 1 and volume < 20000000:
            volume_price_signal = "缩量上涨 - 惜售心理，继续上涨"
        elif change_percent < -3 and volume > 50000000:
            volume_price_signal = "放量下跌 - 恐慌抛售，或现低点"
        else:
            volume_price_signal = "量价关系正常"
        
        return {
            "code": code,
            "name": name,
            "industry": industry,
            "market_type": market_type,
            "current_price": price,
            "change_percent": change_percent,
            "pe_ratio": pe,
            "pb_ratio": pb,
            "roe": roe,
            "debt_ratio": round(random.uniform(0.1, 0.9), 2),
            "volume": volume,
            "market_cap": int(price * random.randint(100000000, 50000000000)),
            "recommendation": recommendation,
            "total_score": laoliu_score / 100,
            "laoliu_score": laoliu_score,
            "analysis_points": analysis_points,
            "risk_warnings": risk_warnings,
            "investment_advice": advice,
            "volume_price_signal": volume_price_signal,
            "data_source": "laoliu_analyzer",
            "reasons": analysis_points[:3] if analysis_points else ["基本面分析中"],
            "risks": risk_warnings[:3] if risk_warnings else ["市场风险"]
        }
    
    # 生成A股数据
    print("生成A股数据...")
    a_stocks = []
    for stock_info in a_stock_universe:
        code, name, industry, price, pe, pb, roe = stock_info
        stock_data = generate_stock_analysis(code, name, industry, price, pe, pb, roe, "A")
        a_stocks.append(stock_data)
    
    # 生成港股数据
    print("生成港股数据...")
    hk_stocks = []
    for stock_info in hk_stock_universe:
        code, name, industry, price, pe, pb, roe = stock_info
        stock_data = generate_stock_analysis(code, name, industry, price, pe, pb, roe, "HK")
        hk_stocks.append(stock_data)
    
    # 按老刘评分排序
    a_stocks.sort(key=lambda x: x["laoliu_score"], reverse=True)
    hk_stocks.sort(key=lambda x: x["laoliu_score"], reverse=True)
    
    print(f"A股数据生成完成，共{len(a_stocks)}只")
    print(f"港股数据生成完成，共{len(hk_stocks)}只")
    
    # 生成各类数据文件
    files_to_generate = {
        "stocks_a.json": {
            "update_time": current_time,
            "total_count": len(a_stocks),
            "analysis_method": "老刘投资理念 + 量价关系分析",
            "screening_criteria": {
                "philosophy": "败于原价，死于抄底，终于杠杆",
                "focus": "高ROE + 低估值 + 量价配合",
                "risk_control": "分批建仓，控制杠杆"
            },
            "stocks": a_stocks
        },
        "stocks_hk.json": {
            "update_time": current_time,
            "total_count": len(hk_stocks),
            "analysis_method": "老刘投资理念 + 港股估值优势",
            "screening_criteria": {
                "philosophy": "人弃我取，人取我弃",
                "focus": "港股估值洼地 + 龙头企业",
                "advantage": "估值合理，分红稳定"
            },
            "stocks": hk_stocks
        },
        "summary.json": {
            "update_time": current_time,
            "market_status": {
                "sentiment": "neutral_positive",
                "position_suggestion": 0.6,
                "signals": [
                    f"A股市场共分析{len(a_stocks)}只股票，港股{len(hk_stocks)}只",
                    "按老刘投资理念筛选，重点关注高ROE低估值标的",
                    "当前市场存在结构性机会，建议精选个股"
                ]
            },
            "recommendations_count": {
                "a_stocks": len([s for s in a_stocks if s["laoliu_score"] >= 60]),
                "hk_stocks": len([s for s in hk_stocks if s["laoliu_score"] >= 60]),
                "total": len([s for s in a_stocks + hk_stocks if s["laoliu_score"] >= 60])
            },
            "top_picks": {
                "a_stocks": a_stocks[:5],
                "hk_stocks": hk_stocks[:3]
            },
            "portfolio_risk": "medium",
            "investment_suggestions": [
                "当前市场按老刘理念可适度配置，建议6成仓位",
                "重点关注银行、食品饮料等老刘偏好行业",
                "港股估值优势明显，腾讯等龙头可适当配置",
                "严格控制风险：败于原价，死于抄底，终于杠杆",
                "跟着游资，跟着热点，跟着龙头 - 但要控制风险"
            ],
            "laoliu_wisdom": {
                "core_principle": "败于原价，死于抄底，终于杠杆",
                "contrarian_thinking": "人弃我取，人取我弃",
                "follow_smart_money": "跟着游资，跟着热点，跟着龙头",
                "value_growth": "低估值 + 高ROE + 成长性"
            }
        },
        "market_timing.json": {
            "update_time": current_time,
            "market_phase": "震荡市",
            "position_suggestion": 0.6,
            "sentiment_score": 0.55,
            "timing_signals": [
                {
                    "name": "基本面",
                    "signal": "positive",
                    "score": 0.65,
                    "description": f"平均ROE为{sum([s['roe'] for s in a_stocks[:20]])/20:.1f}%，盈利能力良好"
                },
                {
                    "name": "估值面", 
                    "signal": "positive",
                    "score": 0.7,
                    "description": f"平均PE为{sum([s['pe_ratio'] for s in a_stocks[:20]])/20:.1f}倍，估值合理"
                },
                {
                    "name": "情绪面",
                    "signal": "neutral",
                    "score": 0.5,
                    "description": "市场情绪相对平衡"
                },
                {
                    "name": "量价面",
                    "signal": "neutral",
                    "score": 0.55,
                    "description": "量价关系正常，无异常信号"
                }
            ],
            "market_status": {
                "sentiment": "neutral_positive",
                "position_suggestion": 0.6,
                "signals": [
                    "市场按老刘标准筛选后，发现较多投资机会",
                    "银行、食品饮料等价值股估值合理",
                    "港股相比A股估值优势更加明显"
                ]
            },
            "recommendations": [
                "按老刘'人弃我取'理念，当前可适度加仓到6成",
                "重点配置银行(估值低ROE稳定)、食品饮料(消费龙头)",
                "港股腾讯、中国移动等龙头估值合理可配置",
                "严格遵循'败于原价，死于抄底，终于杠杆'风控原则"
            ],
            "laoliu_timing_wisdom": "多看少动是个好习惯，价格严重超跌才是买入时机",
            "opportunity_type": "结构性机会"
        }
    }
    
    # 保存文件
    for filename, data in files_to_generate.items():
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存: {filename}")
    
    print(f"\n大量股票数据生成完成!")
    print(f"A股推荐: {len(a_stocks)}只 (老刘评分前20: {[s['name'] for s in a_stocks[:20]]})")
    print(f"港股推荐: {len(hk_stocks)}只 (老刘评分前10: {[s['name'] for s in hk_stocks[:10]]})")
    print(f"更新时间: {current_time}")
    print(f"分析方法: 老刘投资理念 + 量价关系分析")
    print(f"核心理念: 败于原价，死于抄底，终于杠杆")

if __name__ == "__main__":
    generate_comprehensive_stock_data()