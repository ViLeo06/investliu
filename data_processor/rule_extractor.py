#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则提取器 - 生成基于老刘经验的投资建议
"""

from typing import Dict, List, Any
from datetime import datetime

class RuleExtractor:
    def __init__(self):
        """初始化规则提取器"""
        # 老刘的投资理念和建议模板
        self.investment_philosophies = [
            "价值投资需要耐心等待",
            "优质企业的时间价值",
            "分散投资降低风险",
            "不要把鸡蛋放在一个篮子里",
            "投资要有安全边际"
        ]
        
        self.market_timing_rules = {
            'bullish': [
                "市场情绪乐观，可适当加仓",
                "优质标的增多，选择余地大",
                "注意不要追高，保持理性"
            ],
            'bearish': [
                "市场调整期，控制仓位",
                "寻找超跌优质股机会",
                "现金为王，耐心等待"
            ],
            'neutral': [
                "市场震荡，保持平衡仓位",
                "精选个股，注重质量",
                "分批建仓，降低成本"
            ]
        }
        
        print("规则提取器初始化完成")
    
    def generate_investment_suggestions(self, timing_analysis: Dict, 
                                      a_recommendations: Dict, hk_recommendations: Dict) -> List[str]:
        """生成投资建议"""
        suggestions = []
        
        # 基于市场择时的建议
        market_sentiment = timing_analysis.get('market_sentiment', 'neutral')
        position = timing_analysis.get('recommended_position', 0.5)
        
        # 基于老刘投资理念的建议
        suggestions = [
            f"当前市场按老刘理念可适度配置，建议{int(position*10)}成仓位",
            "重点关注银行、食品饮料等老刘偏好行业",
            "港股估值优势明显，腾讯等龙头可适当配置",
            "严格控制风险：败于原价，死于抄底，终于杠杆",
            "跟着游资，跟着热点，跟着龙头 - 但要控制风险"
        ]
        
        return suggestions[:5]  # 最多返回5条建议
    
    def extract_stock_insights(self, stock: Dict) -> Dict:
        """提取单只股票的投资洞察"""
        insights = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # 分析优势
        if stock.get('pe_ratio', 0) < 15:
            insights['strengths'].append('估值偏低，安全边际较高')
        
        if stock.get('roe', 0) > 15:
            insights['strengths'].append('盈利能力强，ROE表现优秀')
        
        if stock.get('dividend_yield', 0) > 3:
            insights['strengths'].append('分红收益率较高，现金回报稳定')
        
        # 分析劣势
        if stock.get('debt_ratio', 0) > 0.7:
            insights['weaknesses'].append('负债率偏高，财务风险需关注')
        
        if stock.get('pe_ratio', 0) > 30:
            insights['weaknesses'].append('估值偏高，存在回调风险')
        
        # 分析机会
        industry = stock.get('industry', '')
        if industry in ['银行', '保险']:
            insights['opportunities'].append('金融板块估值修复机会')
        elif industry in ['食品饮料']:
            insights['opportunities'].append('消费升级长期受益')
        
        # 分析威胁
        change_percent = abs(stock.get('change_percent', 0))
        if change_percent > 5:
            insights['threats'].append('短期波动较大，需控制风险')
        
        return insights
    
    def generate_portfolio_advice(self, stocks: List[Dict]) -> Dict:
        """生成投资组合建议"""
        if not stocks:
            return {
                'allocation_advice': '暂无合适标的',
                'risk_level': 'high',
                'suggestions': ['等待更好的投资机会']
            }
        
        # 按行业分类
        industry_groups = {}
        for stock in stocks:
            industry = stock.get('industry', '其他')
            if industry not in industry_groups:
                industry_groups[industry] = []
            industry_groups[industry].append(stock)
        
        # 生成配置建议
        allocation_advice = []
        total_industries = len(industry_groups)
        
        for industry, industry_stocks in industry_groups.items():
            count = len(industry_stocks)
            if count > 1:
                allocation_advice.append(f"{industry}板块可配置{count}只股票，分散风险")
            else:
                allocation_advice.append(f"{industry}板块重点关注{industry_stocks[0]['name']}")
        
        # 评估风险等级
        avg_score = sum(stock.get('total_score', 0.5) for stock in stocks) / len(stocks)
        if avg_score > 0.7:
            risk_level = 'low'
        elif avg_score > 0.5:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # 生成具体建议
        suggestions = []
        if total_industries >= 3:
            suggestions.append('投资组合行业分散度良好')
        else:
            suggestions.append('建议增加行业分散度，降低集中风险')
        
        if avg_score > 0.6:
            suggestions.append('整体标的质量较高，可适当增加仓位')
        else:
            suggestions.append('标的质量一般，建议控制仓位')
        
        return {
            'allocation_advice': allocation_advice,
            'risk_level': risk_level,
            'suggestions': suggestions
        }
    
    def get_market_outlook(self, timing_analysis: Dict) -> str:
        """获取市场展望"""
        sentiment = timing_analysis.get('market_sentiment', 'neutral')
        overall_score = timing_analysis.get('overall_score', 0.5)
        
        if sentiment == 'bullish' and overall_score > 0.6:
            return "市场短期向好，可关注优质成长股机会"
        elif sentiment == 'bearish' and overall_score < 0.4:
            return "市场面临调整压力，建议控制仓位等待机会"
        else:
            return "市场处于震荡格局，建议精选个股，保持耐心"
    
    def generate_daily_summary(self, all_data: Dict) -> Dict:
        """生成每日投资总结"""
        current_time = datetime.now().strftime("%Y-%m-%d")
        
        summary = {
            'date': current_time,
            'market_outlook': self.get_market_outlook(all_data.get('timing_analysis', {})),
            'key_recommendations': [],
            'risk_alerts': [],
            'philosophy': self.investment_philosophies[hash(current_time) % len(self.investment_philosophies)]
        }
        
        # 提取关键推荐
        a_stocks = all_data.get('a_recommendations', {}).get('stocks', [])
        hk_stocks = all_data.get('hk_recommendations', {}).get('stocks', [])
        
        top_stocks = sorted(a_stocks + hk_stocks, key=lambda x: x.get('total_score', 0), reverse=True)[:3]
        
        for stock in top_stocks:
            summary['key_recommendations'].append({
                'name': stock.get('name', ''),
                'code': stock.get('code', ''),
                'reason': stock.get('reason', ''),
                'score': stock.get('total_score', 0)
            })
        
        # 风险提醒
        timing = all_data.get('timing_analysis', {})
        if timing.get('recommended_position', 0.5) < 0.4:
            summary['risk_alerts'].append('市场风险较高，建议控制仓位')
        
        risk_warnings = timing.get('risk_warning', [])
        summary['risk_alerts'].extend(risk_warnings[:2])
        
        return summary