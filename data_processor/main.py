#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老刘投资决策系统 - 主数据生成器
基于老刘投资经验和规则，生成股票推荐数据
"""

import json
import datetime
import os
import sys
from typing import Dict, List, Any

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_data_fetcher import StockDataFetcher
from stock_analyzer import StockAnalyzer
from rule_extractor import RuleExtractor
from laoliu_analyzer import LaoLiuAnalyzer

class DataGenerator:
    def __init__(self):
        """初始化数据生成器"""
        self.fetcher = StockDataFetcher()
        self.analyzer = StockAnalyzer()
        self.rule_extractor = RuleExtractor()
        self.laoliu_analyzer = LaoLiuAnalyzer()  # 新增老刘分析器
        
        # 输出目录
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static_data')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        print(f"数据生成器初始化完成，输出目录: {self.output_dir}")
    
    def generate_all_data(self):
        """生成所有数据文件"""
        print("=" * 60)
        print("开始生成老刘投资决策数据")
        print("=" * 60)
        
        try:
            # 1. 获取股票数据
            print("正在获取股票数据...")
            a_stocks = self.fetcher.fetch_a_stocks()
            hk_stocks = self.fetcher.fetch_hk_stocks()
            market_data = self.fetcher.fetch_market_data()
            
            # 2. 分析股票（集成老刘理念）
            print("正在分析股票...")
            analyzed_a_stocks = self.analyzer.analyze_stocks(a_stocks, market_type='A')
            analyzed_hk_stocks = self.analyzer.analyze_stocks(hk_stocks, market_type='HK')
            
            # 使用老刘分析器进行深度分析
            print("正在进行老刘风格分析...")
            laoliu_a_analysis = [self.laoliu_analyzer.analyze_stock_laoliu_style(stock) for stock in analyzed_a_stocks]
            laoliu_hk_analysis = [self.laoliu_analyzer.analyze_stock_laoliu_style(stock) for stock in analyzed_hk_stocks]
            
            # 合并分析结果
            for i, stock in enumerate(analyzed_a_stocks):
                stock.update(laoliu_a_analysis[i])
            for i, stock in enumerate(analyzed_hk_stocks):
                stock.update(laoliu_hk_analysis[i])
            
            # 3. 生成推荐（基于老刘标准）
            print("正在生成推荐...")
            a_recommendations = self.generate_laoliu_recommendations(analyzed_a_stocks, 'A')
            hk_recommendations = self.generate_laoliu_recommendations(analyzed_hk_stocks, 'HK')
            
            # 4. 市场择时分析（融入老刘逆向思维）
            print("正在分析市场择时...")
            timing_analysis = self.generate_enhanced_timing_analysis(market_data, analyzed_a_stocks, analyzed_hk_stocks)
            
            # 5. 生成汇总数据
            print("正在生成汇总数据...")
            summary_data = self.generate_summary(a_recommendations, hk_recommendations, timing_analysis)
            
            # 6. 生成配置数据
            print("正在生成配置数据...")
            config_data = self.generate_config()
            
            # 7. 保存所有数据
            print("正在保存数据文件...")
            self.save_data(summary_data, a_recommendations, hk_recommendations, timing_analysis, config_data)
            
            print("=" * 60)
            print("数据生成完成！")
            print(f"文件保存位置: {self.output_dir}")
            print(f"A股推荐: {len(a_recommendations['stocks'])}只")
            print(f"港股推荐: {len(hk_recommendations['stocks'])}只")
            print(f"更新时间: {summary_data['update_time']}")
            print("=" * 60)
            
        except Exception as e:
            print(f"数据生成失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_summary(self, a_recommendations: Dict, hk_recommendations: Dict, timing_analysis: Dict) -> Dict:
        """生成汇总数据"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取推荐数量
        a_stocks_list = a_recommendations.get('stocks', [])
        hk_stocks_list = hk_recommendations.get('stocks', [])
        a_count = len(a_stocks_list)
        hk_count = len(hk_stocks_list)
        total_count = a_count + hk_count
        
        # 获取顶级推荐（前5只A股，前3只港股）
        top_a_stocks = sorted(
            a_stocks_list, 
            key=lambda x: x.get('laoliu_score', x.get('total_score', 0) * 100), 
            reverse=True
        )[:5]
        
        top_hk_stocks = sorted(
            hk_stocks_list, 
            key=lambda x: x.get('laoliu_score', x.get('total_score', 0) * 100), 
            reverse=True
        )[:3]
        
        # 生成投资建议
        investment_suggestions = self.rule_extractor.generate_investment_suggestions(
            timing_analysis, a_recommendations, hk_recommendations
        )
        
        return {
            "update_time": current_time,
            "market_status": timing_analysis.get('market_status', {}),
            "recommendations_count": {
                "a_stocks": a_count,
                "hk_stocks": hk_count,
                "total": total_count
            },
            "top_picks": {
                "a_stocks": top_a_stocks,
                "hk_stocks": top_hk_stocks
            },
            "portfolio_risk": self.analyzer.assess_portfolio_risk(top_a_stocks + top_hk_stocks),
            "investment_suggestions": investment_suggestions
        }
    
    def generate_config(self) -> Dict:
        """生成配置数据"""
        return {
            "version": "1.0.0",
            "app_name": "老刘投资决策",
            "update_frequency": "daily",
            "data_sources": [
                "新浪财经",
                "腾讯财经",
                "东方财富"
            ],
            "api_endpoints": {
                "summary": "/summary.json",
                "market_timing": "/market_timing.json",
                "stocks_a": "/stocks_a.json",
                "stocks_hk": "/stocks_hk.json"
            },
            "cache_duration": {
                "summary": 3600,
                "market_timing": 1800,
                "stocks": 3600
            },
            "risk_levels": {
                "low": {
                    "name": "保守型",
                    "max_position": 0.3,
                    "min_pe_filter": True,
                    "dividend_focus": True
                },
                "medium": {
                    "name": "平衡型",
                    "max_position": 0.6,
                    "min_pe_filter": False,
                    "dividend_focus": False
                },
                "high": {
                    "name": "激进型",
                    "max_position": 0.9,
                    "min_pe_filter": False,
                    "dividend_focus": False
                }
            },
            "disclaimer": "本系统基于历史数据和个人经验，仅供参考，不构成投资建议。投资有风险，入市需谨慎。",
            "contact": {
                "support": "noreply@example.com",
                "feedback": "feedback@example.com"
            }
        }
    
    def generate_laoliu_recommendations(self, stocks: List[Dict], market_type: str) -> Dict:
        """生成基于老刘理念的股票推荐"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 按老刘标准筛选股票
        qualified_stocks = self.laoliu_analyzer.screen_stocks_by_laoliu_criteria(
            stocks, min_roe=8, max_pe=30, min_score=40
        )
        
        # 取前20只作为推荐
        top_stocks = qualified_stocks[:20]
        
        return {
            "update_time": current_time,
            "market_type": market_type,
            "total_count": len(qualified_stocks),
            "analysis_method": "老刘投资理念 + 量价关系分析",
            "screening_criteria": {
                "philosophy": "败于原价，死于抄底，终于杠杆",
                "focus": "高ROE + 低估值 + 量价配合",
                "risk_control": "分批建仓，控制杠杆"
            },
            "stocks": top_stocks
        }
    
    def generate_enhanced_timing_analysis(self, market_data: Dict, a_stocks: List[Dict], hk_stocks: List[Dict]) -> Dict:
        """生成增强的市场择时分析"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 使用老刘分析器生成市场情绪分析
        all_stocks = a_stocks + hk_stocks
        market_sentiment = self.laoliu_analyzer.generate_market_sentiment_analysis(all_stocks)
        industry_rotation = self.laoliu_analyzer.get_industry_rotation_advice()
        
        return {
            "update_time": current_time,
            "market_phase": self._determine_market_phase(market_sentiment),
            "position_suggestion": self._calculate_position_suggestion(market_sentiment),
            "sentiment_score": market_sentiment.get("rise_ratio", 0.5),
            "timing_signals": [
                {
                    "name": "技术面",
                    "signal": "neutral" if market_sentiment["rise_ratio"] < 0.6 else "positive",
                    "score": market_sentiment["rise_ratio"],
                    "description": f"当前{int(market_sentiment['rise_ratio']*100)}%股票上涨"
                },
                {
                    "name": "估值面",
                    "signal": "positive" if market_sentiment["avg_pe"] < 20 else "neutral",
                    "score": max(0.3, (30 - market_sentiment["avg_pe"]) / 30),
                    "description": f"平均PE为{market_sentiment['avg_pe']}倍"
                },
                {
                    "name": "基本面",
                    "signal": "positive" if market_sentiment["avg_roe"] > 12 else "neutral",
                    "score": min(1.0, market_sentiment["avg_roe"] / 15),
                    "description": f"平均ROE为{market_sentiment['avg_roe']}%"
                },
                {
                    "name": "情绪面",
                    "signal": self._get_emotion_signal(market_sentiment["sentiment"]),
                    "score": self._get_emotion_score(market_sentiment["sentiment"]),
                    "description": f"市场情绪{market_sentiment['sentiment']}"
                }
            ],
            "market_status": {
                "sentiment": market_sentiment["sentiment"],
                "position_suggestion": self._calculate_position_suggestion(market_sentiment),
                "signals": self._generate_market_signals(market_sentiment, industry_rotation)
            },
            "recommendations": self._generate_timing_recommendations(market_sentiment, industry_rotation),
            "laoliu_wisdom": market_sentiment.get("laoliu_wisdom", ""),
            "opportunity_type": market_sentiment.get("opportunity_type", "")
        }
    
    def _determine_market_phase(self, market_sentiment: Dict) -> str:
        """判断市场阶段"""
        sentiment = market_sentiment.get("sentiment", "平衡")
        
        if "过度乐观" in sentiment:
            return "牛市顶部"
        elif "乐观" in sentiment:
            return "牛市中期"
        elif "过度悲观" in sentiment:
            return "熊市底部"
        elif "悲观" in sentiment:
            return "熊市中期"
        else:
            return "震荡市"
    
    def _calculate_position_suggestion(self, market_sentiment: Dict) -> float:
        """计算建议仓位"""
        rise_ratio = market_sentiment.get("rise_ratio", 0.5)
        avg_pe = market_sentiment.get("avg_pe", 20)
        avg_roe = market_sentiment.get("avg_roe", 10)
        
        # 基础仓位
        base_position = 0.5
        
        # 根据市场情绪调整
        if rise_ratio > 0.8:  # 过度乐观
            position = 0.2
        elif rise_ratio > 0.6:  # 乐观
            position = 0.4
        elif rise_ratio < 0.2:  # 过度悲观
            position = 0.8
        elif rise_ratio < 0.4:  # 悲观
            position = 0.7
        else:
            position = base_position
        
        return max(0.1, min(0.9, position))
    
    def _get_emotion_signal(self, sentiment: str) -> str:
        """获取情绪信号"""
        if "过度乐观" in sentiment:
            return "negative"
        elif "过度悲观" in sentiment:
            return "positive"
        else:
            return "neutral"
    
    def _get_emotion_score(self, sentiment: str) -> float:
        """获取情绪评分"""
        emotion_scores = {
            "过度乐观": 0.2,
            "乐观": 0.4,
            "平衡": 0.5,
            "悲观": 0.7,
            "过度悲观": 0.9
        }
        return emotion_scores.get(sentiment, 0.5)
    
    def _generate_market_signals(self, market_sentiment: Dict, industry_rotation: Dict) -> List[str]:
        """生成市场信号"""
        signals = []
        
        sentiment = market_sentiment.get("sentiment", "平衡")
        rise_ratio = market_sentiment.get("rise_ratio", 0.5)
        
        if rise_ratio > 0.7:
            signals.append(f"市场情绪{sentiment}，{int(rise_ratio*100)}%股票上涨")
        elif rise_ratio < 0.3:
            signals.append(f"市场情绪{sentiment}，仅{int(rise_ratio*100)}%股票上涨")
        else:
            signals.append(f"市场情绪{sentiment}，涨跌比例相对均衡")
        
        signals.append(f"平均PE为{market_sentiment['avg_pe']}倍，ROE为{market_sentiment['avg_roe']}%")
        
        # 添加热点行业信息
        hot_sectors = industry_rotation.get("current_hot_sectors", [])
        if hot_sectors:
            sector_names = [s["name"] for s in hot_sectors[:3]]
            signals.append(f"当前热点板块：{', '.join(sector_names)}")
        
        return signals
    
    def _generate_timing_recommendations(self, market_sentiment: Dict, industry_rotation: Dict) -> List[str]:
        """生成择时建议"""
        recommendations = []
        
        # 基础建议
        recommendations.append(market_sentiment.get("advice", ""))
        
        # 行业轮动建议
        hot_sectors = industry_rotation.get("current_hot_sectors", [])
        if hot_sectors:
            sector_list = ", ".join([f"{s['name']}({s['reason']})" for s in hot_sectors[:2]])
            recommendations.append(f"重点关注：{sector_list}")
        
        avoid_sectors = industry_rotation.get("avoid_sectors", [])
        if avoid_sectors:
            avoid_list = ", ".join([s["name"] for s in avoid_sectors])
            recommendations.append(f"谨慎对待：{avoid_list}")
        
        # 老刘风险控制提醒
        recommendations.append("严格控制风险：败于原价，死于抄底，终于杠杆")
        recommendations.append("分批建仓，设置止损，不追高不抄底")
        
        return recommendations
    
    def save_data(self, summary_data: Dict, a_recommendations: Dict, hk_recommendations: Dict, 
                  timing_analysis: Dict, config_data: Dict):
        """保存所有数据文件"""
        files_to_save = [
            ('summary.json', summary_data),
            ('stocks_a.json', a_recommendations),
            ('stocks_hk.json', hk_recommendations),
            ('market_timing.json', timing_analysis),
            ('miniprogram_config.json', config_data)
        ]
        
        # 保存到static_data目录
        for filename, data in files_to_save:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已保存: {filename}")
        
        # 同时复制到根目录以供GitHub Pages访问
        root_dir = os.path.dirname(os.path.dirname(__file__))
        print(f"同时复制文件到根目录: {root_dir}")
        
        for filename, data in files_to_save:
            root_filepath = os.path.join(root_dir, filename)
            with open(root_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已复制到根目录: {filename}")

if __name__ == "__main__":
    print("启动老刘投资决策数据生成器...")
    print("集成真实股票数据源...")
    print("支持多数据源自动切换...")
    generator = DataGenerator()
    generator.generate_all_data()