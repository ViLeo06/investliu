"""
股票分析和推荐算法
基于老刘的投资规则分析股票并生成推荐
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class StockAnalyzer:
    def __init__(self, rules_file_path="notes/processed/extracted_rules.json"):
        self.rules = self._load_rules(rules_file_path)
        self.scoring_weights = {
            'selection': 0.4,   # 选股规则权重
            'timing': 0.3,      # 择时规则权重
            'position': 0.2,    # 仓位规则权重
            'risk': 0.1         # 风险规则权重
        }
    
    def _load_rules(self, rules_file_path):
        """加载投资规则"""
        try:
            with open(rules_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"规则文件未找到: {rules_file_path}")
            return self._get_default_rules()
        except Exception as e:
            logger.error(f"加载规则文件失败: {e}")
            return self._get_default_rules()
    
    def _get_default_rules(self):
        """获取默认投资规则（基于价值投资理念）"""
        return {
            'selection_rules': [
                {
                    'type': 'selection',
                    'conditions': [
                        {'indicator': 'PE', 'operator': '<', 'value': 30},
                        {'indicator': 'PB', 'operator': '<', 'value': 3},
                        {'indicator': 'ROE', 'operator': '>', 'value': 0.15}
                    ],
                    'action': 'buy',
                    'confidence': 0.8,
                    'content': '低估值高ROE股票'
                },
                {
                    'type': 'selection', 
                    'conditions': [
                        {'indicator': 'market_cap', 'operator': '>', 'value': 50},
                        {'indicator': 'debt_ratio', 'operator': '<', 'value': 0.5}
                    ],
                    'action': 'buy',
                    'confidence': 0.7,
                    'content': '大盘低负债股票'
                }
            ],
            'timing_rules': [
                {
                    'type': 'timing',
                    'signal': 'oversold',
                    'action': 'buy',
                    'confidence': 0.6,
                    'content': '超跌反弹机会'
                },
                {
                    'type': 'timing',
                    'signal': 'breakout',
                    'action': 'buy',
                    'confidence': 0.7,
                    'content': '突破买入信号'
                }
            ],
            'position_rules': [
                {
                    'type': 'position',
                    'condition': 'bull_market',
                    'position': 0.8,
                    'confidence': 0.8,
                    'content': '牛市重仓'
                },
                {
                    'type': 'position',
                    'condition': 'bear_market',
                    'position': 0.3,
                    'confidence': 0.8,
                    'content': '熊市轻仓'
                }
            ],
            'risk_rules': [
                {
                    'type': 'risk',
                    'content': '单只股票不超过20%',
                    'max_single_position': 0.2,
                    'confidence': 0.9
                }
            ],
            'insights': [
                {
                    'content': '价值投资需要耐心',
                    'type': 'philosophy',
                    'confidence': 1.0
                }
            ]
        }
    
    def analyze_stock(self, stock_data, financial_data=None):
        """分析单只股票"""
        try:
            analysis_result = {
                'code': stock_data.get('code', ''),
                'name': stock_data.get('name', ''),
                'current_price': stock_data.get('current_price', 0),
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'scores': {},
                'total_score': 0,
                'recommendation': 'hold',
                'reasons': [],
                'warnings': []
            }
            
            # 选股评分
            selection_score = self._evaluate_selection_rules(stock_data, financial_data)
            analysis_result['scores']['selection'] = selection_score
            
            # 择时评分
            timing_score = self._evaluate_timing_rules(stock_data)
            analysis_result['scores']['timing'] = timing_score
            
            # 风险评分
            risk_score = self._evaluate_risk_rules(stock_data, financial_data)
            analysis_result['scores']['risk'] = risk_score
            
            # 计算总分
            total_score = (
                selection_score * self.scoring_weights['selection'] +
                timing_score * self.scoring_weights['timing'] +
                risk_score * self.scoring_weights['risk']
            )
            
            analysis_result['total_score'] = round(total_score, 2)
            
            # 生成推荐
            analysis_result['recommendation'] = self._generate_recommendation(total_score)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析股票失败: {stock_data.get('code', 'unknown')}, {e}")
            return None
    
    def _evaluate_selection_rules(self, stock_data, financial_data):
        """评估选股规则"""
        if not self.rules.get('selection_rules'):
            return 0.5
        
        total_score = 0
        total_weight = 0
        matched_rules = []
        
        for rule in self.rules['selection_rules']:
            rule_score = 0
            rule_weight = rule.get('confidence', 0.5)
            conditions = rule.get('conditions', [])
            
            if not conditions:
                continue
            
            satisfied_conditions = 0
            
            for condition in conditions:
                indicator = condition.get('indicator', '')
                operator = condition.get('operator', '=')
                value = condition.get('value', 0)
                
                stock_value = self._get_stock_indicator_value(stock_data, financial_data, indicator)
                
                if stock_value is not None and self._evaluate_condition(stock_value, operator, value):
                    satisfied_conditions += 1
            
            # 计算规则得分
            if conditions:
                rule_score = satisfied_conditions / len(conditions)
                
                if rule_score > 0.5:  # 超过一半条件满足
                    total_score += rule_score * rule_weight
                    total_weight += rule_weight
                    matched_rules.append(rule.get('content', ''))
        
        return (total_score / total_weight) if total_weight > 0 else 0.5
    
    def _evaluate_timing_rules(self, stock_data):
        """评估择时规则"""
        if not self.rules.get('timing_rules'):
            return 0.5
        
        # 简化的择时评估
        change_percent = stock_data.get('change_percent', 0)
        volume = stock_data.get('volume', 0)
        
        score = 0.5  # 基础分数
        
        # 基于涨跌幅的择时判断
        if change_percent < -5:  # 大跌可能是买入机会
            score += 0.2
        elif change_percent > 5:  # 大涨可能过热
            score -= 0.2
        
        # 基于成交量的判断
        if volume > 0:  # 有成交量数据
            # 这里可以加入更复杂的量价分析
            score += 0.1
        
        return max(0, min(1, score))
    
    def _evaluate_risk_rules(self, stock_data, financial_data):
        """评估风险规则"""
        score = 0.5  # 基础风险分数
        
        # 市值风险评估
        market_cap = stock_data.get('market_cap', 0)
        if market_cap > 100:  # 大于100亿市值
            score += 0.2
        elif market_cap < 20:  # 小于20亿市值风险较高
            score -= 0.3
        
        # 波动性风险评估
        change_percent = abs(stock_data.get('change_percent', 0))
        if change_percent > 9:  # 涨跌幅过大
            score -= 0.2
        
        # 负债率风险评估
        if financial_data:
            debt_ratio = financial_data.get('debt_ratio', 0)
            if debt_ratio > 0.7:  # 高负债
                score -= 0.3
            elif debt_ratio < 0.3:  # 低负债
                score += 0.2
        
        return max(0, min(1, score))
    
    def _get_stock_indicator_value(self, stock_data, financial_data, indicator):
        """获取股票指标值"""
        # 首先从stock_data中查找
        if indicator in stock_data:
            return stock_data[indicator]
        
        # 然后从financial_data中查找
        if financial_data and indicator in financial_data:
            return financial_data[indicator]
        
        # 指标映射
        indicator_map = {
            'PE': 'pe_ratio',
            'PB': 'pb_ratio', 
            'ROE': 'roe',
            'market_cap': 'market_cap',
            'debt_ratio': 'debt_ratio'
        }
        
        mapped_indicator = indicator_map.get(indicator, indicator)
        
        if mapped_indicator in stock_data:
            return stock_data[mapped_indicator]
        
        if financial_data and mapped_indicator in financial_data:
            return financial_data[mapped_indicator]
        
        return None
    
    def _evaluate_condition(self, value, operator, target):
        """评估条件"""
        if operator == '>':
            return value > target
        elif operator == '<':
            return value < target
        elif operator == '>=':
            return value >= target
        elif operator == '<=':
            return value <= target
        elif operator == '=':
            return abs(value - target) < 0.01
        else:
            return False
    
    def _generate_recommendation(self, total_score):
        """生成投资建议"""
        if total_score >= 0.7:
            return 'strong_buy'
        elif total_score >= 0.6:
            return 'buy'
        elif total_score >= 0.4:
            return 'hold'
        elif total_score >= 0.3:
            return 'sell'
        else:
            return 'strong_sell'
    
    def analyze_market_timing(self, market_indices):
        """分析市场择时"""
        try:
            timing_result = {
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_sentiment': 'neutral',
                'recommended_position': 0.5,
                'signals': []
            }
            
            if not market_indices:
                return timing_result
            
            # 分析主要指数
            total_change = 0
            index_count = 0
            
            for index_code, index_data in market_indices.items():
                change_percent = index_data.get('change_percent', 0)
                total_change += change_percent
                index_count += 1
            
            if index_count > 0:
                avg_change = total_change / index_count
                
                # 市场情绪判断
                if avg_change > 2:
                    timing_result['market_sentiment'] = 'bullish'
                    timing_result['recommended_position'] = 0.7
                    timing_result['signals'].append('大盘强势上涨，可考虑加仓')
                elif avg_change < -2:
                    timing_result['market_sentiment'] = 'bearish'
                    timing_result['recommended_position'] = 0.3
                    timing_result['signals'].append('大盘下跌，建议减仓观望')
                else:
                    timing_result['market_sentiment'] = 'neutral'
                    timing_result['recommended_position'] = 0.5
                    timing_result['signals'].append('大盘震荡，保持平衡仓位')
            
            return timing_result
            
        except Exception as e:
            logger.error(f"市场择时分析失败: {e}")
            return {
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_sentiment': 'neutral',
                'recommended_position': 0.5,
                'signals': ['分析数据不足']
            }
    
    def generate_stock_recommendations(self, stocks_data, financial_data_dict=None, top_n=10):
        """生成股票推荐列表"""
        try:
            recommendations = []
            
            for stock in stocks_data:
                stock_code = stock.get('code', '')
                financial_data = financial_data_dict.get(stock_code) if financial_data_dict else None
                
                analysis = self.analyze_stock(stock, financial_data)
                if analysis and analysis['total_score'] > 0.4:  # 过滤低分股票
                    recommendations.append(analysis)
            
            # 按总分排序
            recommendations.sort(key=lambda x: x['total_score'], reverse=True)
            
            # 返回前N个推荐
            return recommendations[:top_n]
            
        except Exception as e:
            logger.error(f"生成推荐列表失败: {e}")
            return []
    
    def generate_portfolio_suggestion(self, recommended_stocks, market_timing):
        """生成投资组合建议"""
        try:
            portfolio = {
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_position': market_timing.get('recommended_position', 0.5),
                'allocation': [],
                'risk_level': 'medium',
                'suggestions': []
            }
            
            if not recommended_stocks:
                portfolio['suggestions'].append('暂无合适的投资标的')
                return portfolio
            
            # 根据推荐强度分配权重
            total_stocks = min(len(recommended_stocks), 10)  # 最多10只股票
            base_weight = 1.0 / total_stocks
            
            for i, stock in enumerate(recommended_stocks[:total_stocks]):
                # 根据评分调整权重
                score_multiplier = stock['total_score'] / 0.6  # 以0.6为基准
                weight = base_weight * score_multiplier
                
                portfolio['allocation'].append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'weight': round(weight, 3),
                    'score': stock['total_score'],
                    'recommendation': stock['recommendation']
                })
            
            # 标准化权重
            total_weight = sum(item['weight'] for item in portfolio['allocation'])
            if total_weight > 0:
                for item in portfolio['allocation']:
                    item['weight'] = round(item['weight'] / total_weight, 3)
            
            # 生成投资建议
            high_score_count = sum(1 for stock in recommended_stocks if stock['total_score'] > 0.7)
            if high_score_count >= 3:
                portfolio['risk_level'] = 'low'
                portfolio['suggestions'].append('发现多个优质标的，风险较低')
            elif high_score_count == 0:
                portfolio['risk_level'] = 'high'
                portfolio['suggestions'].append('当前推荐标的评分偏低，建议谨慎')
            
            portfolio['suggestions'].append(f'建议持仓比例: {int(portfolio["market_position"]*100)}%')
            
            return portfolio
            
        except Exception as e:
            logger.error(f"生成投资组合建议失败: {e}")
            return {
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_position': 0.5,
                'allocation': [],
                'risk_level': 'medium',
                'suggestions': ['生成投资组合失败']
            }

def main():
    """测试函数"""
    analyzer = StockAnalyzer()
    
    # 模拟股票数据
    test_stock = {
        'code': '000001',
        'name': '平安银行',
        'current_price': 12.50,
        'change_percent': -2.1,
        'pe_ratio': 5.2,
        'pb_ratio': 0.8,
        'market_cap': 241.2,
        'volume': 15420000
    }
    
    # 模拟财务数据
    test_financial = {
        'roe': 0.12,
        'debt_ratio': 0.35,
        'revenue_growth': 0.08,
        'profit_growth': 0.15
    }
    
    # 分析单只股票
    analysis = analyzer.analyze_stock(test_stock, test_financial)
    print("股票分析结果:")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()