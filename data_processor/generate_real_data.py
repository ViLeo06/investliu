#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实股票数据生成器 - 从网络实时抓取数据并生成JSON文件
集成多个数据源：akshare、新浪财经、腾讯财经、东方财富
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入现有模块
from real_time_stock_fetcher import RealTimeStockFetcher
from stock_analyzer import StockAnalyzer
from laoliu_analyzer import LaoLiuAnalyzer

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealDataGenerator:
    """真实数据生成器"""
    
    def __init__(self):
        self.fetcher = RealTimeStockFetcher()
        self.analyzer = StockAnalyzer()
        self.laoliu_analyzer = LaoLiuAnalyzer()
        
        # 输出目录
        self.output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logger.info(f"数据输出目录: {self.output_dir}")
    
    def generate_real_a_stocks_data(self, limit: int = 5000) -> Dict:
        """生成真实A股数据"""
        logger.info("开始获取真实A股数据...")
        
        try:
            # 获取A股实时数据
            raw_stocks = self.fetcher.get_all_a_stocks()
            
            if not raw_stocks:
                logger.error("未能获取到A股数据，使用备用数据")
                return self._generate_fallback_a_data()
            
            logger.info(f"获取到 {len(raw_stocks)} 只A股原始数据")
            
            # 限制数量以提高性能
            if limit and len(raw_stocks) > limit:
                raw_stocks = raw_stocks[:limit]
                logger.info(f"限制处理数量为 {limit} 只")
            
            # 分析股票数据
            analyzed_stocks = []
            total_stocks = len(raw_stocks)
            
            for i, stock in enumerate(raw_stocks):
                try:
                    # 使用老刘分析器增强数据
                    enhanced_stock = self._enhance_stock_data(stock)
                    analyzed_stocks.append(enhanced_stock)
                    
                    # 进度显示
                    if (i + 1) % 100 == 0:
                        logger.info(f"已处理 {i + 1}/{total_stocks} 只股票")
                        
                except Exception as e:
                    logger.warning(f"处理股票 {stock.get('code', 'unknown')} 失败: {e}")
                    continue
            
            # 生成最终数据结构
            result = {
                "total_count": len(analyzed_stocks),
                "market": "A股",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_source": "实时抓取",
                "api_sources": ["akshare", "sina", "tencent"],
                "stocks": analyzed_stocks
            }
            
            logger.info(f"成功生成 {len(analyzed_stocks)} 只A股分析数据")
            return result
            
        except Exception as e:
            logger.error(f"生成A股数据失败: {e}")
            return self._generate_fallback_a_data()
    
    def generate_real_hk_stocks_data(self, limit: int = 2000) -> Dict:
        """生成真实港股数据"""
        logger.info("开始获取真实港股数据...")
        
        try:
            # 获取港股实时数据
            raw_stocks = self.fetcher.get_all_hk_stocks()
            
            if not raw_stocks:
                logger.error("未能获取到港股数据，使用备用数据")
                return self._generate_fallback_hk_data()
            
            logger.info(f"获取到 {len(raw_stocks)} 只港股原始数据")
            
            if limit and len(raw_stocks) > limit:
                raw_stocks = raw_stocks[:limit]
            
            # 分析港股数据
            analyzed_stocks = []
            
            for i, stock in enumerate(raw_stocks):
                try:
                    enhanced_stock = self._enhance_stock_data(stock, market='HK')
                    analyzed_stocks.append(enhanced_stock)
                    
                    if (i + 1) % 50 == 0:
                        logger.info(f"已处理 {i + 1}/{len(raw_stocks)} 只港股")
                        
                except Exception as e:
                    logger.warning(f"处理港股 {stock.get('code', 'unknown')} 失败: {e}")
                    continue
            
            result = {
                "total_count": len(analyzed_stocks),
                "market": "港股",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_source": "实时抓取",
                "api_sources": ["akshare", "hk_apis"],
                "stocks": analyzed_stocks
            }
            
            logger.info(f"成功生成 {len(analyzed_stocks)} 只港股分析数据")
            return result
            
        except Exception as e:
            logger.error(f"生成港股数据失败: {e}")
            return self._generate_fallback_hk_data()
    
    def _enhance_stock_data(self, stock: Dict, market: str = 'A') -> Dict:
        """使用老刘投资理念增强股票数据"""
        try:
            # 基础数据
            enhanced = stock.copy()
            
            # 计算老刘评分
            if market == 'A':
                # 获取更详细的财务数据
                detailed_data = self.fetcher.get_stock_detail(stock['code'], 'A')
                if detailed_data and 'financial_metrics' in detailed_data:
                    financial_metrics = detailed_data['financial_metrics']
                else:
                    financial_metrics = self._estimate_financial_metrics(stock)
                
                # 使用老刘分析器计算评分
                laoliu_analysis = self.laoliu_analyzer.analyze_stock_laoliu_style({
                    **stock,
                    'financial_metrics': financial_metrics
                })
                
                enhanced.update(laoliu_analysis)
            else:
                # 港股简化处理
                enhanced.update({
                    'laoliu_score': self._calculate_simple_hk_score(stock),
                    'investment_advice': self._get_simple_investment_advice(stock),
                    'recommendation': self._get_recommendation_level(stock),
                    'analysis_points': [f"港股 {stock['name']} 基本面分析"],
                    'risk_warnings': []
                })
            
            return enhanced
            
        except Exception as e:
            logger.warning(f"增强数据失败 {stock.get('code', 'unknown')}: {e}")
            # 返回基础数据
            return {
                **stock,
                'laoliu_score': 50,
                'investment_advice': '数据处理中',
                'recommendation': 'hold',
                'analysis_points': [],
                'risk_warnings': []
            }
    
    def _estimate_financial_metrics(self, stock: Dict) -> Dict:
        """估算财务指标（当无法获取真实财务数据时）"""
        pe_ratio = stock.get('pe_ratio', 0)
        pb_ratio = stock.get('pb_ratio', 0)
        
        # 基于市盈率和市净率估算ROE
        if pe_ratio > 0 and pb_ratio > 0:
            estimated_roe = (1 / pb_ratio) / (pe_ratio / 100) * 100
            estimated_roe = min(max(estimated_roe, 0), 50)  # 限制在合理范围
        else:
            estimated_roe = 10  # 默认值
        
        return {
            'roe': round(estimated_roe, 2),
            'roa': round(estimated_roe * 0.6, 2),
            'debt_ratio': 0.4,  # 默认负债率
            'current_ratio': 2.0,
            'gross_margin': 25.0,
            'net_margin': 8.0,
            'revenue_growth': 10.0,
            'profit_growth': 12.0,
            'report_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _calculate_simple_hk_score(self, stock: Dict) -> int:
        """计算港股简化评分"""
        score = 50  # 基础分
        
        # 价格变动评分
        change_percent = stock.get('change_percent', 0)
        if change_percent > 5:
            score += 10
        elif change_percent > 0:
            score += 5
        elif change_percent < -5:
            score -= 10
        
        # 成交量评分
        volume = stock.get('volume', 0)
        if volume > 1000000:
            score += 10
        elif volume > 100000:
            score += 5
        
        return max(0, min(100, score))
    
    def _get_simple_investment_advice(self, stock: Dict) -> str:
        """获取简单投资建议"""
        change_percent = stock.get('change_percent', 0)
        
        if change_percent > 3:
            return "短期表现较好，可关注"
        elif change_percent < -3:
            return "价格调整中，谨慎观望"
        else:
            return "价格相对稳定，持续关注"
    
    def _get_recommendation_level(self, stock: Dict) -> str:
        """获取推荐等级"""
        change_percent = stock.get('change_percent', 0)
        volume = stock.get('volume', 0)
        
        if change_percent > 5 and volume > 1000000:
            return 'buy'
        elif change_percent > 2:
            return 'hold'
        elif change_percent < -5:
            return 'sell'
        else:
            return 'hold'
    
    def generate_market_timing_data(self) -> Dict:
        """生成市场择时数据"""
        logger.info("生成市场择时数据...")
        
        try:
            # 获取市场综合数据进行分析
            sample_stocks = self.fetcher.get_all_a_stocks()[:100]  # 取前100只作为市场样本
            
            if sample_stocks:
                # 分析市场情绪
                rise_count = sum(1 for stock in sample_stocks if stock.get('change_percent', 0) > 0)
                rise_ratio = rise_count / len(sample_stocks)
                
                avg_change = sum(stock.get('change_percent', 0) for stock in sample_stocks) / len(sample_stocks)
                avg_pe = sum(stock.get('pe_ratio', 0) for stock in sample_stocks if stock.get('pe_ratio', 0) > 0) / max(1, len([s for s in sample_stocks if s.get('pe_ratio', 0) > 0]))
                
                # 判断市场阶段
                if rise_ratio > 0.7:
                    market_phase = "牛市中期"
                    position_suggestion = 0.8
                elif rise_ratio > 0.5:
                    market_phase = "震荡上升"
                    position_suggestion = 0.6
                elif rise_ratio > 0.3:
                    market_phase = "震荡市"
                    position_suggestion = 0.5
                else:
                    market_phase = "调整期"
                    position_suggestion = 0.3
                
                recommendations = [
                    f"当前市场{int(rise_ratio*100)}%的股票上涨，市场情绪{'乐观' if rise_ratio > 0.5 else '谨慎'}",
                    f"平均涨跌幅{avg_change:.2f}%，市场{'活跃' if abs(avg_change) > 1 else '相对平稳'}",
                    f"建议仓位{int(position_suggestion*100)}%，{'积极' if position_suggestion > 0.6 else '谨慎' if position_suggestion < 0.4 else '平衡'}配置",
                    "严格遵循老刘理念：败于原价，死于抄底，终于杠杆"
                ]
            else:
                # 默认数据
                market_phase = "数据更新中"
                position_suggestion = 0.5
                rise_ratio = 0.5
                recommendations = ["市场数据更新中，请稍后查看"]
            
            return {
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "market_phase": market_phase,
                "position_suggestion": position_suggestion,
                "sentiment_score": rise_ratio,
                "recommendations": recommendations,
                "timing_signals": [
                    {
                        "name": "技术面",
                        "signal": "positive" if rise_ratio > 0.6 else "neutral" if rise_ratio > 0.4 else "negative",
                        "score": rise_ratio,
                        "description": f"市场上涨股票比例{int(rise_ratio*100)}%"
                    },
                    {
                        "name": "情绪面", 
                        "signal": "positive" if avg_change > 1 else "neutral" if avg_change > -1 else "negative",
                        "score": max(0, min(1, (avg_change + 5) / 10)),
                        "description": f"平均涨跌幅{avg_change:.2f}%"
                    }
                ],
                "laoliu_wisdom": "人弃我取，在别人恐惧时贪婪，在别人贪婪时恐惧"
            }
            
        except Exception as e:
            logger.error(f"生成市场择时数据失败: {e}")
            return self._get_default_timing_data()
    
    def _get_default_timing_data(self) -> Dict:
        """获取默认择时数据"""
        return {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market_phase": "震荡市",
            "position_suggestion": 0.5,
            "sentiment_score": 0.5,
            "recommendations": [
                "市场数据获取中，建议谨慎操作",
                "保持合理仓位，关注优质个股",
                "严格遵循风控原则"
            ],
            "timing_signals": [],
            "laoliu_wisdom": "败于原价，死于抄底，终于杠杆"
        }
    
    def _generate_fallback_a_data(self) -> Dict:
        """生成A股备用数据"""
        logger.info("使用A股备用数据")
        return {
            "total_count": 0,
            "market": "A股",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "备用数据",
            "api_sources": [],
            "stocks": [],
            "error": "无法获取实时数据，请检查网络连接"
        }
    
    def _generate_fallback_hk_data(self) -> Dict:
        """生成港股备用数据"""
        logger.info("使用港股备用数据")
        return {
            "total_count": 0,
            "market": "港股",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "备用数据",
            "api_sources": [],
            "stocks": [],
            "error": "无法获取实时数据，请检查网络连接"
        }
    
    def save_all_data(self):
        """生成并保存所有数据文件"""
        logger.info("开始生成所有真实股票数据...")
        
        # 生成A股数据
        logger.info("=" * 60)
        a_stocks_data = self.generate_real_a_stocks_data(1000)  # 限制1000只以提高速度
        a_stocks_file = os.path.join(self.output_dir, 'stocks_a.json')
        with open(a_stocks_file, 'w', encoding='utf-8') as f:
            json.dump(a_stocks_data, f, ensure_ascii=False, indent=2)
        logger.info(f"A股数据已保存到: {a_stocks_file}")
        
        # 生成港股数据
        logger.info("=" * 60)
        hk_stocks_data = self.generate_real_hk_stocks_data(500)  # 限制500只
        hk_stocks_file = os.path.join(self.output_dir, 'stocks_hk.json')
        with open(hk_stocks_file, 'w', encoding='utf-8') as f:
            json.dump(hk_stocks_data, f, ensure_ascii=False, indent=2)
        logger.info(f"港股数据已保存到: {hk_stocks_file}")
        
        # 生成市场择时数据
        logger.info("=" * 60)
        timing_data = self.generate_market_timing_data()
        timing_file = os.path.join(self.output_dir, 'market_timing.json')
        with open(timing_file, 'w', encoding='utf-8') as f:
            json.dump(timing_data, f, ensure_ascii=False, indent=2)
        logger.info(f"市场择时数据已保存到: {timing_file}")
        
        # 生成汇总数据
        summary_data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_stocks": a_stocks_data['total_count'] + hk_stocks_data['total_count'],
            "a_stocks_count": a_stocks_data['total_count'],
            "hk_stocks_count": hk_stocks_data['total_count'],
            "markets": {
                "a_stocks": {
                    "total": a_stocks_data['total_count'],
                    "data_source": a_stocks_data.get('data_source', 'unknown')
                },
                "hk_stocks": {
                    "total": hk_stocks_data['total_count'],
                    "data_source": hk_stocks_data.get('data_source', 'unknown')
                }
            },
            "market_timing": timing_data.get('market_phase', 'unknown'),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        summary_file = os.path.join(self.output_dir, 'summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        logger.info(f"汇总数据已保存到: {summary_file}")
        
        logger.info("=" * 60)
        logger.info("🎉 所有真实数据生成完成！")
        logger.info(f"📊 A股: {a_stocks_data['total_count']} 只")
        logger.info(f"📊 港股: {hk_stocks_data['total_count']} 只")
        logger.info(f"📊 总计: {summary_data['total_stocks']} 只股票")
        logger.info("=" * 60)

def main():
    """主函数"""
    try:
        generator = RealDataGenerator()
        generator.save_all_data()
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.error(f"数据生成失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()