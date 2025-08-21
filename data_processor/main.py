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

class DataGenerator:
    def __init__(self):
        """初始化数据生成器"""
        self.fetcher = StockDataFetcher()
        self.analyzer = StockAnalyzer()
        self.rule_extractor = RuleExtractor()
        
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
            print("📈 正在获取股票数据...")
            a_stocks = self.fetcher.fetch_a_stocks()
            hk_stocks = self.fetcher.fetch_hk_stocks()
            market_data = self.fetcher.fetch_market_data()
            
            # 2. 分析股票
            print("🔍 正在分析股票...")
            analyzed_a_stocks = self.analyzer.analyze_stocks(a_stocks, market_type='A')
            analyzed_hk_stocks = self.analyzer.analyze_stocks(hk_stocks, market_type='HK')
            
            # 3. 生成推荐
            print("⭐ 正在生成推荐...")
            a_recommendations = self.analyzer.generate_recommendations(analyzed_a_stocks)
            hk_recommendations = self.analyzer.generate_recommendations(analyzed_hk_stocks)
            
            # 4. 市场择时分析
            print("⏰ 正在分析市场择时...")
            timing_analysis = self.analyzer.analyze_market_timing(market_data, analyzed_a_stocks)
            
            # 5. 生成汇总数据
            print("📊 正在生成汇总数据...")
            summary_data = self.generate_summary(a_recommendations, hk_recommendations, timing_analysis)
            
            # 6. 生成配置数据
            print("⚙️ 正在生成配置数据...")
            config_data = self.generate_config()
            
            # 7. 保存所有数据
            print("💾 正在保存数据文件...")
            self.save_data(summary_data, a_recommendations, hk_recommendations, timing_analysis, config_data)
            
            print("=" * 60)
            print("✅ 数据生成完成！")
            print(f"📁 文件保存位置: {self.output_dir}")
            print(f"📈 A股推荐: {len(a_recommendations['stocks'])}只")
            print(f"🌏 港股推荐: {len(hk_recommendations['stocks'])}只")
            print(f"⏰ 更新时间: {summary_data['update_time']}")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ 数据生成失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_summary(self, a_recommendations: Dict, hk_recommendations: Dict, timing_analysis: Dict) -> Dict:
        """生成汇总数据"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取推荐数量
        a_count = len(a_recommendations.get('stocks', []))
        hk_count = len(hk_recommendations.get('stocks', []))
        total_count = a_count + hk_count
        
        # 获取顶级推荐（前3只）
        top_a_stocks = sorted(
            a_recommendations.get('stocks', []), 
            key=lambda x: x.get('total_score', 0), 
            reverse=True
        )[:3]
        
        top_hk_stocks = sorted(
            hk_recommendations.get('stocks', []), 
            key=lambda x: x.get('total_score', 0), 
            reverse=True
        )[:2]
        
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
        
        for filename, data in files_to_save:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存: {filename}")

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_all_data()