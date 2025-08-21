#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析器 - 基于老刘投资规则分析股票
"""

import math
import random
from typing import Dict, List, Any
from datetime import datetime

class StockAnalyzer:
    def __init__(self):
        """初始化股票分析器"""
        # 老刘的估值标准
        self.valuation_criteria = {
            'pe_low_threshold': 15,
            'pe_high_threshold': 30,
            'pb_low_threshold': 1.5,
            'pb_high_threshold': 3.0,
            'roe_min_threshold': 10,
            'debt_ratio_max': 0.7
        }
        
        # 行业权重配置
        self.industry_weights = {
            '银行': 1.2,
            '食品饮料': 1.1,
            '医药': 1.0,
            '科技': 0.9,
            '互联网科技': 0.9,
            '保险': 1.0,
            '其他': 0.8
        }
        
        print("股票分析器初始化完成")
    
    def analyze_stocks(self, stocks: List[Dict], market_type: str) -> List[Dict]:
        """分析股票列表"""
        print(f"正在分析{market_type}股票...")
        
        analyzed_stocks = []
        for stock in stocks:
            try:
                analyzed_stock = self._analyze_single_stock(stock, market_type)
                if analyzed_stock:
                    analyzed_stocks.append(analyzed_stock)
            except Exception as e:
                print(f"分析股票{stock.get('name', 'Unknown')}失败: {str(e)}")
                continue
        
        print(f"{market_type}股票分析完成，共{len(analyzed_stocks)}只")
        return analyzed_stocks
    
    def _analyze_single_stock(self, stock: Dict, market_type: str) -> Dict:
        """分析单只股票"""
        try:
            # 基础数据
            pe_ratio = stock.get('pe_ratio', 0)
            pb_ratio = stock.get('pb_ratio', 0)
            roe = stock.get('roe', 0)
            debt_ratio = stock.get('debt_ratio', 0)
            dividend_yield = stock.get('dividend_yield', 0)
            industry = stock.get('industry', '其他')
            
            # 计算各项评分
            valuation_score = self._calculate_valuation_score(pe_ratio, pb_ratio)
            growth_score = self._calculate_growth_score(roe)
            profitability_score = self._calculate_profitability_score(roe, dividend_yield)
            safety_score = self._calculate_safety_score(debt_ratio, pb_ratio)
            
            # 行业调整
            industry_weight = self.industry_weights.get(industry, 1.0)
            
            # 综合评分
            total_score = (
                valuation_score * 0.3 + 
                growth_score * 0.25 + 
                profitability_score * 0.25 + 
                safety_score * 0.2
            ) * industry_weight
            
            # 生成推荐等级
            recommendation = self._generate_recommendation(total_score, valuation_score)
            
            # 计算目标价和止损价
            target_price, stop_loss = self._calculate_price_targets(
                stock.get('current_price', 0), total_score, pe_ratio
            )
            
            # 生成投资理由
            reason = self._generate_investment_reason(
                stock, valuation_score, growth_score, profitability_score, safety_score
            )
            
            # 返回分析结果
            analyzed_stock = stock.copy()
            analyzed_stock.update({
                'scores': {
                    'valuation': round(valuation_score, 2),
                    'growth': round(growth_score, 2),
                    'profitability': round(profitability_score, 2),
                    'safety': round(safety_score, 2)
                },
                'total_score': round(total_score, 2),
                'recommendation': recommendation,
                'target_price': target_price,
                'stop_loss': stop_loss,
                'reason': reason
            })
            
            return analyzed_stock
            
        except Exception as e:
            print(f"分析股票失败: {str(e)}")
            return None
    
    def _calculate_valuation_score(self, pe_ratio: float, pb_ratio: float) -> float:
        """计算估值评分"""
        score = 0.5
        
        # PE评分
        if pe_ratio > 0:
            if pe_ratio < self.valuation_criteria['pe_low_threshold']:
                score += 0.3
            elif pe_ratio > self.valuation_criteria['pe_high_threshold']:
                score -= 0.2
        
        # PB评分
        if pb_ratio > 0:
            if pb_ratio < self.valuation_criteria['pb_low_threshold']:
                score += 0.2
            elif pb_ratio > self.valuation_criteria['pb_high_threshold']:
                score -= 0.1
        
        return max(0, min(1, score))
    
    def _calculate_growth_score(self, roe: float) -> float:
        """计算成长性评分"""
        if roe >= 20:
            return 0.9
        elif roe >= 15:
            return 0.7
        elif roe >= self.valuation_criteria['roe_min_threshold']:
            return 0.5
        else:
            return 0.2
    
    def _calculate_profitability_score(self, roe: float, dividend_yield: float) -> float:
        """计算盈利能力评分"""
        score = 0.3
        
        # ROE评分
        if roe >= 15:
            score += 0.4
        elif roe >= 10:
            score += 0.2
        
        # 分红评分
        if dividend_yield >= 3:
            score += 0.3
        elif dividend_yield >= 2:
            score += 0.1
        
        return max(0, min(1, score))
    
    def _calculate_safety_score(self, debt_ratio: float, pb_ratio: float) -> float:
        """计算安全性评分"""
        score = 0.5
        
        # 负债率评分
        if debt_ratio < 0.3:
            score += 0.3
        elif debt_ratio < 0.5:
            score += 0.1
        elif debt_ratio > self.valuation_criteria['debt_ratio_max']:
            score -= 0.2
        
        # PB安全边际
        if pb_ratio < 1:
            score += 0.2
        elif pb_ratio < 2:
            score += 0.1
        
        return max(0, min(1, score))
    
    def _generate_recommendation(self, total_score: float, valuation_score: float) -> str:
        """生成推荐等级"""
        if total_score >= 0.8:
            return 'strong_buy'
        elif total_score >= 0.6:
            return 'buy'
        elif total_score >= 0.4:
            return 'hold'
        elif total_score >= 0.2:
            return 'sell'
        else:
            return 'strong_sell'
    
    def _calculate_price_targets(self, current_price: float, total_score: float, pe_ratio: float) -> tuple:
        """计算目标价和止损价"""
        if current_price <= 0:
            return 0, 0
        
        # 基于评分的目标价
        score_multiplier = 1 + (total_score - 0.5) * 0.6  # 0.7-1.3倍
        target_price = round(current_price * score_multiplier, 2)
        
        # 止损价设定为当前价的85-90%
        stop_loss_ratio = 0.85 if total_score > 0.6 else 0.90
        stop_loss = round(current_price * stop_loss_ratio, 2)
        
        return target_price, stop_loss
    
    def _generate_investment_reason(self, stock: Dict, val_score: float, 
                                   growth_score: float, profit_score: float, safety_score: float) -> str:
        """生成投资理由"""
        reasons = []
        
        # 估值理由
        if val_score > 0.7:
            reasons.append(f"PE估值偏低")
        elif val_score < 0.3:
            reasons.append(f"估值偏高")
        
        # 成长性理由
        roe = stock.get('roe', 0)
        if growth_score > 0.7:
            reasons.append(f"ROE{roe}%表现优秀")
        
        # 盈利能力理由
        dividend_yield = stock.get('dividend_yield', 0)
        if profit_score > 0.7 and dividend_yield > 3:
            reasons.append(f"分红收益率{dividend_yield}%较高")
        
        # 安全性理由
        debt_ratio = stock.get('debt_ratio', 0)
        if safety_score > 0.7:
            reasons.append(f"负债率{debt_ratio*100:.1f}%较低")
        
        # 行业理由
        industry = stock.get('industry', '')
        if industry in ['银行', '食品饮料']:
            reasons.append(f"{industry}行业配置价值显现")
        
        return "，".join(reasons) if reasons else "综合评分一般，谨慎关注"
    
    def generate_recommendations(self, analyzed_stocks: List[Dict]) -> Dict:
        """生成推荐报告"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 按评分排序
        sorted_stocks = sorted(analyzed_stocks, key=lambda x: x.get('total_score', 0), reverse=True)
        
        # 统计推荐等级
        recommendation_stats = {
            'strong_buy': 0,
            'buy': 0,
            'hold': 0,
            'sell': 0,
            'strong_sell': 0
        }
        
        for stock in sorted_stocks:
            rec = stock.get('recommendation', 'hold')
            recommendation_stats[rec] = recommendation_stats.get(rec, 0) + 1
        
        # 计算平均指标
        if sorted_stocks:
            avg_pe = sum(s.get('pe_ratio', 0) for s in sorted_stocks) / len(sorted_stocks)
            avg_pb = sum(s.get('pb_ratio', 0) for s in sorted_stocks) / len(sorted_stocks)
            avg_roe = sum(s.get('roe', 0) for s in sorted_stocks) / len(sorted_stocks)
        else:
            avg_pe = avg_pb = avg_roe = 0
        
        return {
            'update_time': current_time,
            'total_count': len(sorted_stocks),
            'filtered_count': len(sorted_stocks),
            'stocks': sorted_stocks,
            'market_summary': {
                'avg_pe': round(avg_pe, 2),
                'avg_pb': round(avg_pb, 2),
                'avg_roe': round(avg_roe, 2),
                'strong_buy': recommendation_stats['strong_buy'],
                'buy': recommendation_stats['buy'],
                'hold': recommendation_stats['hold'],
                'sell': recommendation_stats['sell'],
                'strong_sell': recommendation_stats['strong_sell']
            }
        }
    
    def analyze_market_timing(self, market_data: Dict, stocks: List[Dict]) -> Dict:
        """分析市场择时"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 模拟择时分析
        shanghai_change = market_data.get('shanghai_index', {}).get('change', 0)
        
        # 市场情绪判断
        if shanghai_change > 1:
            sentiment = 'bullish'
            position = 0.7
        elif shanghai_change < -1:
            sentiment = 'bearish'
            position = 0.3
        else:
            sentiment = 'neutral'
            position = 0.5
        
        # 技术指标模拟
        technical_score = random.uniform(0.4, 0.8)
        fundamental_score = random.uniform(0.5, 0.9)
        sentiment_score = random.uniform(0.3, 0.7)
        
        overall_score = (technical_score + fundamental_score + sentiment_score) / 3
        
        # 生成信号
        signals = []
        if overall_score > 0.6:
            signals.append("技术面：多项指标显示向上趋势")
        if len([s for s in stocks if s.get('total_score', 0) > 0.7]) > 3:
            signals.append("基本面：优质标的增多")
        
        return {
            'analysis_time': current_time,
            'market_sentiment': sentiment,
            'recommended_position': position,
            'signals': signals,
            'timing_indicators': {
                'technical': {
                    'rsi': random.uniform(30, 70),
                    'macd': '金叉形态' if random.random() > 0.5 else '死叉形态',
                    'ma20_ma60': '多头排列' if random.random() > 0.5 else '空头排列',
                    'score': technical_score
                },
                'fundamental': {
                    'pe_percentile': random.uniform(20, 80),
                    'pb_percentile': random.uniform(15, 75),
                    'earnings_growth': random.uniform(5, 15),
                    'score': fundamental_score
                },
                'sentiment': {
                    'vix_equivalent': random.uniform(15, 35),
                    'margin_trading': '温和增长' if random.random() > 0.5 else '快速增长',
                    'new_account': '持平上月' if random.random() > 0.5 else '增长明显',
                    'score': sentiment_score
                }
            },
            'overall_score': overall_score,
            'position_advice': {
                'current': position,
                'target': position,
                'action': '维持' if abs(position - 0.5) < 0.1 else ('加仓' if position > 0.5 else '减仓'),
                'reason': f"综合评分{overall_score:.1f}，市场情绪{sentiment}"
            },
            'risk_warning': [
                '关注美联储政策变化',
                '注意地缘政治风险',
                '警惕个股业绩地雷'
            ]
        }
    
    def assess_portfolio_risk(self, stocks: List[Dict]) -> str:
        """评估投资组合风险"""
        if not stocks:
            return 'medium'
        
        # 计算平均评分
        avg_score = sum(stock.get('total_score', 0.5) for stock in stocks) / len(stocks)
        
        # 行业分散度
        industries = set(stock.get('industry', '其他') for stock in stocks)
        industry_diversity = len(industries) / len(stocks)
        
        # 风险评估
        if avg_score > 0.7 and industry_diversity > 0.3:
            return 'low'
        elif avg_score > 0.5 or industry_diversity > 0.2:
            return 'medium'
        else:
            return 'high'