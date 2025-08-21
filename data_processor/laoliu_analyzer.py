#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老刘投资策略分析器
基于老刘投资笔记的投资理念和量价关系分析
"""

import random
from typing import Dict, List, Any
from datetime import datetime

class LaoLiuAnalyzer:
    def __init__(self):
        """初始化老刘分析器"""
        # 老刘投资理念关键词
        self.laoliu_principles = {
            # 败于原价，死于抄底，终于杠杆
            "risk_control": ["不抄底", "控制杠杆", "分批建仓", "设置止损"],
            
            # 人弃我取，人取我弃 - 逆向思维
            "contrarian_thinking": ["市场恐慌时买入", "热点高潮时谨慎", "独立思考"],
            
            # 跟着游资，跟着热点，跟着龙头
            "follow_smart_money": ["游资偏好", "热点概念", "行业龙头", "资金流向"],
            
            # 价值投资 + 成长性
            "value_growth": ["低估值", "高ROE", "成长性", "护城河"],
            
            # 量价关系精髓
            "volume_price": ["放量上涨", "缩量下跌", "量价配合", "成交异动"]
        }
        
        # 行业权重评估（基于老刘偏好）
        self.industry_weights = {
            "银行": 1.2,  # 老刘重视银行股
            "食品饮料": 1.15,  # 白酒等消费龙头
            "医药": 1.1,  # 高ROE行业
            "科技": 1.0,  # 跟热点但需谨慎
            "新能源": 0.95,  # 高估值需谨慎
            "房地产": 0.8,  # 政策敏感
            "军工": 0.9,  # 题材性较强
            "保险": 1.1,  # 价值投资标的
            "互联网科技": 0.95,  # 港股估值合理
            "电信运营": 1.1,  # 高分红稳定
            "消费": 1.05,  # 长期价值
            "基建": 0.85,  # 周期性强
            "煤炭": 0.9,  # 周期底部
            "钢铁": 0.85  # 产能过剩
        }
        
        print("老刘投资策略分析器初始化完成")
    
    def analyze_stock_laoliu_style(self, stock_data: Dict) -> Dict:
        """基于老刘理念分析单只股票"""
        analysis = {
            "code": stock_data.get("code"),
            "name": stock_data.get("name"),
            "laoliu_score": 0,
            "analysis_points": [],
            "risk_warnings": [],
            "investment_advice": "",
            "volume_price_signal": "",
            "contrarian_opportunity": False
        }
        
        # 1. 基础面分析（老刘重视ROE和估值）
        roe = stock_data.get("roe", 10)
        pe_ratio = stock_data.get("pe_ratio", 20)
        pb_ratio = stock_data.get("pb_ratio", 2)
        
        if roe >= 15:
            analysis["laoliu_score"] += 25
            analysis["analysis_points"].append(f"ROE达{roe}%，盈利能力强")
        elif roe >= 10:
            analysis["laoliu_score"] += 15
            analysis["analysis_points"].append(f"ROE为{roe}%，盈利能力较好")
        else:
            analysis["risk_warnings"].append(f"ROE仅{roe}%，盈利能力一般")
        
        # 2. 估值分析
        if pe_ratio <= 15:
            analysis["laoliu_score"] += 20
            analysis["analysis_points"].append(f"PE仅{pe_ratio}倍，估值偏低")
        elif pe_ratio <= 25:
            analysis["laoliu_score"] += 10
            analysis["analysis_points"].append(f"PE为{pe_ratio}倍，估值合理")
        else:
            analysis["risk_warnings"].append(f"PE高达{pe_ratio}倍，估值偏高")
        
        if pb_ratio <= 2:
            analysis["laoliu_score"] += 15
            analysis["analysis_points"].append(f"PB仅{pb_ratio}倍，账面价值安全")
        elif pb_ratio > 5:
            analysis["risk_warnings"].append(f"PB达{pb_ratio}倍，市净率偏高")
        
        # 3. 行业权重调整
        industry = stock_data.get("industry", "其他")
        industry_weight = self.industry_weights.get(industry, 1.0)
        analysis["laoliu_score"] = int(analysis["laoliu_score"] * industry_weight)
        
        if industry_weight > 1.0:
            analysis["analysis_points"].append(f"{industry}行业符合老刘投资偏好")
        elif industry_weight < 0.9:
            analysis["risk_warnings"].append(f"{industry}行业需谨慎对待")
        
        # 4. 量价关系分析
        change_percent = stock_data.get("change_percent", 0)
        volume = stock_data.get("volume", 0)
        
        analysis["volume_price_signal"] = self._analyze_volume_price(change_percent, volume)
        
        # 5. 逆向投资机会判断
        if change_percent < -5 and pe_ratio < 20 and roe > 10:
            analysis["contrarian_opportunity"] = True
            analysis["analysis_points"].append("符合'人弃我取'逆向投资机会")
            analysis["laoliu_score"] += 10
        
        # 6. 投资建议生成
        if analysis["laoliu_score"] >= 80:
            analysis["investment_advice"] = "强烈推荐：符合老刘多项投资标准"
        elif analysis["laoliu_score"] >= 60:
            analysis["investment_advice"] = "推荐：基本面良好，可适当配置"
        elif analysis["laoliu_score"] >= 40:
            analysis["investment_advice"] = "观望：存在一定投资价值"
        else:
            analysis["investment_advice"] = "回避：不符合老刘投资标准"
        
        return analysis
    
    def _analyze_volume_price(self, change_percent: float, volume: int) -> str:
        """分析量价关系 - 基于老刘笔记第4页量价关系精髓"""
        if volume == 0:
            return "无成交量数据"
        
        # 根据老刘笔记的量价关系理论
        if change_percent > 3 and volume > 50000000:
            return "放量上涨 - 资金追捧，可关注"
        elif change_percent > 1 and volume < 20000000:
            return "缩量上涨 - 惜售心理，继续上涨"
        elif change_percent < -3 and volume > 50000000:
            return "放量下跌 - 恐慌抛售，或现低点"
        elif change_percent < -1 and volume < 20000000:
            return "缩量下跌 - 继续下跌趋势"
        elif abs(change_percent) < 1 and volume > 80000000:
            if change_percent >= 0:
                return "放量不涨 - 头部出现信号"
            else:
                return "放量不跌 - 底部已现信号"
        elif volume < 10000000:
            return "无量状态 - 需要放量确认方向"
        else:
            return "量价关系正常"
    
    def screen_stocks_by_laoliu_criteria(self, stocks: List[Dict], 
                                         min_roe: float = 8, 
                                         max_pe: float = 30,
                                         min_score: int = 50) -> List[Dict]:
        """按老刘标准筛选股票"""
        qualified_stocks = []
        
        for stock in stocks:
            analysis = self.analyze_stock_laoliu_style(stock)
            
            # 基础筛选条件
            roe = stock.get("roe", 0)
            pe_ratio = stock.get("pe_ratio", 100)
            
            if (roe >= min_roe and 
                pe_ratio <= max_pe and 
                analysis["laoliu_score"] >= min_score):
                
                # 合并分析结果到股票数据
                enhanced_stock = {**stock, **analysis}
                qualified_stocks.append(enhanced_stock)
        
        # 按老刘评分排序
        qualified_stocks.sort(key=lambda x: x["laoliu_score"], reverse=True)
        
        return qualified_stocks
    
    def generate_market_sentiment_analysis(self, stocks: List[Dict]) -> Dict:
        """生成市场情绪分析 - 基于老刘逆向思维"""
        total_stocks = len(stocks)
        if total_stocks == 0:
            return {"sentiment": "unknown", "advice": "数据不足"}
        
        # 统计涨跌股票数量
        rising_stocks = len([s for s in stocks if s.get("change_percent", 0) > 0])
        falling_stocks = total_stocks - rising_stocks
        
        rise_ratio = rising_stocks / total_stocks
        
        # 基于老刘"人弃我取，人取我弃"理念
        if rise_ratio > 0.8:
            sentiment = "过度乐观"
            advice = "市场过热，应保持警惕，考虑逢高减仓"
            opportunity_type = "卖出机会"
        elif rise_ratio > 0.6:
            sentiment = "乐观"
            advice = "市场情绪良好，可维持仓位，精选个股"
            opportunity_type = "持有观望"
        elif rise_ratio < 0.2:
            sentiment = "过度悲观"
            advice = "市场恐慌，正是'人弃我取'的好时机"
            opportunity_type = "逆向买入机会"
        elif rise_ratio < 0.4:
            sentiment = "悲观"
            advice = "市场低迷，可考虑分批建仓优质标的"
            opportunity_type = "分批买入机会"
        else:
            sentiment = "平衡"
            advice = "市场相对平衡，按既定策略执行"
            opportunity_type = "正常操作"
        
        # 计算平均估值水平
        avg_pe = sum([s.get("pe_ratio", 20) for s in stocks]) / total_stocks
        avg_roe = sum([s.get("roe", 10) for s in stocks]) / total_stocks
        
        return {
            "sentiment": sentiment,
            "rise_ratio": rise_ratio,
            "advice": advice,
            "opportunity_type": opportunity_type,
            "avg_pe": round(avg_pe, 1),
            "avg_roe": round(avg_roe, 1),
            "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "laoliu_wisdom": "败于原价，死于抄底，终于杠杆 - 控制风险是第一要务"
        }
    
    def get_industry_rotation_advice(self) -> Dict:
        """获取行业轮动建议 - 基于老刘跟热点理念"""
        return {
            "current_hot_sectors": [
                {"name": "银行", "reason": "估值低，ROE稳定，政策支持", "weight": 1.2},
                {"name": "食品饮料", "reason": "消费龙头，长期价值", "weight": 1.15},
                {"name": "医药", "reason": "高ROE，创新驱动", "weight": 1.1}
            ],
            "avoid_sectors": [
                {"name": "房地产", "reason": "政策压制，流动性差", "weight": 0.8},
                {"name": "基建", "reason": "周期性强，估值偏高", "weight": 0.85}
            ],
            "rotation_strategy": "跟着游资，跟着热点，跟着龙头 - 但要注意风险控制",
            "timing_advice": "游资快，公募慢 - 抓住短期机会，但要及时止盈"
        }