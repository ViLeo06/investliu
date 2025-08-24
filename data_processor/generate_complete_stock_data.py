# 生成完整的股票数据 - A股和港股全量数据
from real_time_stock_fetcher import RealTimeStockFetcher
from stock_analysis_engine import StockAnalysisEngine
import json
import os
from datetime import datetime
from typing import Dict, List
import pandas as pd

class CompleteStockDataGenerator:
    """生成完整的股票数据，包括A股和港股所有股票"""
    
    def __init__(self):
        self.fetcher = RealTimeStockFetcher()
        self.analyzer = StockAnalysisEngine()
        self.output_dir = "complete_stock_data"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_all_stocks_data(self):
        """生成所有股票的基础数据"""
        print("开始生成完整股票数据...")
        
        # 获取A股数据
        print("正在获取A股数据...")
        a_stocks = self.fetcher.get_all_a_stocks()
        
        # 获取港股数据
        print("正在获取港股数据...")
        hk_stocks = self.fetcher.get_all_hk_stocks()
        
        # 生成A股数据文件
        a_stock_data = {
            "total_count": len(a_stocks),
            "market": "A股",
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stocks": []
        }
        
        for stock in a_stocks:
            # 计算老刘评分
            try:
                financial_metrics = self.analyzer.get_financial_metrics(stock['code'])
                laoliu_eval = self.analyzer.calculate_laoliu_score(stock, financial_metrics)
                
                stock_data = {
                    **stock,
                    "laoliu_score": laoliu_eval['laoliu_score'],
                    "investment_advice": laoliu_eval['investment_advice'],
                    "analysis_points": laoliu_eval['analysis_points'][:3],  # 只保留前3个要点
                    "risk_warnings": laoliu_eval['risk_warnings'][:2],      # 只保留前2个风险
                    "roe": financial_metrics.get('roe', 0),
                    "debt_ratio": financial_metrics.get('debt_ratio', 0),
                    "revenue_growth": financial_metrics.get('revenue_growth', 0)
                }
                a_stock_data["stocks"].append(stock_data)
                
            except Exception as e:
                print(f"分析股票 {stock['code']} 失败: {e}")
                # 添加基础数据
                a_stock_data["stocks"].append({
                    **stock,
                    "laoliu_score": 0,
                    "investment_advice": "数据获取中",
                    "analysis_points": [],
                    "risk_warnings": [],
                    "roe": 0,
                    "debt_ratio": 0,
                    "revenue_growth": 0
                })
        
        # 生成港股数据文件
        hk_stock_data = {
            "total_count": len(hk_stocks),
            "market": "港股",
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stocks": hk_stocks  # 港股暂时不进行深度分析
        }
        
        # 保存数据文件
        self._save_json_data("stocks_a_complete.json", a_stock_data)
        self._save_json_data("stocks_hk_complete.json", hk_stock_data)
        
        # 生成汇总数据
        summary_data = {
            "total_stocks": len(a_stocks) + len(hk_stocks),
            "a_stocks_count": len(a_stocks),
            "hk_stocks_count": len(hk_stocks),
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "top_a_stocks": self._get_top_stocks(a_stock_data["stocks"], 20),
            "market_overview": {
                "average_pe": self._calculate_average_pe(a_stocks),
                "rising_count": len([s for s in a_stocks if s['change_percent'] > 0]),
                "falling_count": len([s for s in a_stocks if s['change_percent'] < 0]),
                "total_market_cap": sum([s.get('market_cap', 0) for s in a_stocks])
            }
        }
        
        self._save_json_data("complete_summary.json", summary_data)
        
        print("完整股票数据生成完成!")
        print(f"   A股: {len(a_stocks)} 只")
        print(f"   港股: {len(hk_stocks)} 只")
        print(f"   总计: {len(a_stocks) + len(hk_stocks)} 只")
        
        return summary_data
    
    def generate_analysis_samples(self, sample_count: int = 50):
        """生成分析样本数据"""
        print(f"生成 {sample_count} 个股票分析样本...")
        
        # 获取A股数据
        a_stocks = self.fetcher.get_all_a_stocks()
        
        # 选择样本股票（按市值排序取前面的）
        sorted_stocks = sorted(a_stocks, key=lambda x: x.get('market_cap', 0), reverse=True)
        sample_stocks = sorted_stocks[:sample_count]
        
        analysis_results = []
        
        for i, stock in enumerate(sample_stocks):
            try:
                print(f"正在分析 {i+1}/{sample_count}: {stock['name']} ({stock['code']})")
                
                # 进行完整分析
                analysis_result = self.analyzer.comprehensive_analysis(stock['code'], 'A')
                
                # 优化数据结构供小程序使用
                optimized_result = self._optimize_for_miniprogram(analysis_result)
                analysis_results.append(optimized_result)
                
            except Exception as e:
                print(f"分析 {stock['code']} 失败: {e}")
                continue
        
        # 保存分析样本
        analysis_data = {
            "total_count": len(analysis_results),
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "analysis_results": analysis_results
        }
        
        self._save_json_data("analysis_samples.json", analysis_data)
        
        # 同时保存到小程序目录
        miniprogram_path = "../miniprogram/temp_analysis_samples.json"
        try:
            with open(miniprogram_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        except:
            pass  # 如果路径不存在就跳过
        
        print(f"分析样本生成完成: {len(analysis_results)} 个样本")
        
        return analysis_data
    
    def _optimize_for_miniprogram(self, raw_data: dict) -> dict:
        """优化数据结构以适应小程序使用"""
        return {
            # 基本信息
            "basic_info": {
                "code": raw_data['stock_info']['code'],
                "name": raw_data['stock_info']['name'],
                "market_type": raw_data['stock_info']['market_type'],
                "current_price": raw_data['stock_info']['current_price'],
                "change_percent": raw_data['stock_info']['change_percent'],
                "volume": raw_data['stock_info']['volume'],
                "market_cap": raw_data['stock_info']['market_cap'],
                "industry": raw_data['stock_info']['industry'],
                "update_time": raw_data['stock_info']['update_time']
            },
            
            # 估值指标
            "valuation_metrics": {
                "pe_ratio": raw_data['stock_info']['pe_ratio'],
                "pb_ratio": raw_data['stock_info']['pb_ratio'],
                "ps_ratio": raw_data['financial_metrics'].get('ps_ratio', 0),
                "dividend_yield": raw_data['financial_metrics'].get('dividend_yield', 0)
            },
            
            # 财务指标
            "financial_metrics": {
                "roe": raw_data['financial_metrics']['roe'],
                "roa": raw_data['financial_metrics']['roa'],
                "debt_ratio": raw_data['financial_metrics']['debt_ratio'],
                "current_ratio": raw_data['financial_metrics']['current_ratio'],
                "gross_margin": raw_data['financial_metrics']['gross_margin'],
                "net_margin": raw_data['financial_metrics']['net_margin'],
                "revenue_growth": raw_data['financial_metrics']['revenue_growth'],
                "profit_growth": raw_data['financial_metrics']['profit_growth'],
                "report_date": raw_data['financial_metrics']['report_date']
            },
            
            # 老刘投资评估
            "laoliu_evaluation": {
                "laoliu_score": raw_data['laoliu_evaluation']['laoliu_score'],
                "analysis_points": raw_data['laoliu_evaluation']['analysis_points'],
                "risk_warnings": raw_data['laoliu_evaluation']['risk_warnings'],
                "investment_advice": raw_data['laoliu_evaluation']['investment_advice'],
                "contrarian_opportunity": raw_data['laoliu_evaluation']['contrarian_opportunity']
            },
            
            # 技术分析
            "technical_analysis": {
                "volume_price_signal": raw_data['volume_price_analysis']['signal'],
                "volume_ratio": raw_data['volume_price_analysis'].get('volume_ratio', 1.0),
                "price_change": raw_data['volume_price_analysis'].get('price_change', 0)
            },
            
            # AI智能分析
            "ai_insights": {
                "analysis_content": raw_data['ai_analysis'],
                "key_points": self._extract_key_points(raw_data['ai_analysis']),
                "recommendation": raw_data['investment_recommendation'],
                "confidence_level": self._calculate_confidence_level(raw_data['comprehensive_score'])
            },
            
            # 投资建议
            "investment_summary": {
                "comprehensive_score": raw_data['comprehensive_score'],
                "recommendation": raw_data['investment_recommendation'],
                "target_price": self._calculate_target_price(raw_data),
                "stop_loss": self._calculate_stop_loss(raw_data),
                "position_suggestion": self._get_position_suggestion(raw_data['comprehensive_score'])
            }
        }
    
    def _get_top_stocks(self, stocks: List[Dict], count: int) -> List[Dict]:
        """获取评分最高的股票"""
        sorted_stocks = sorted(stocks, key=lambda x: x.get('laoliu_score', 0), reverse=True)
        return sorted_stocks[:count]
    
    def _calculate_average_pe(self, stocks: List[Dict]) -> float:
        """计算平均市盈率"""
        valid_pe = [s['pe_ratio'] for s in stocks if s.get('pe_ratio', 0) > 0]
        return round(sum(valid_pe) / len(valid_pe), 2) if valid_pe else 0
    
    def _extract_key_points(self, ai_analysis: str) -> list:
        """从AI分析中提取关键点"""
        try:
            lines = ai_analysis.split('\n')
            key_points = []
            
            for line in lines:
                line = line.strip()
                if line and ('•' in line or '1.' in line or '2.' in line or '3.' in line or '4.' in line):
                    clean_line = line.replace('•', '').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').strip()
                    if clean_line:
                        key_points.append(clean_line)
            
            return key_points[:5]  # 最多返回5个关键点
        except:
            return ["AI分析内容解析中"]
    
    def _calculate_confidence_level(self, score: int) -> str:
        """计算分析置信度"""
        if score >= 80:
            return "高"
        elif score >= 60:
            return "中"
        else:
            return "低"
    
    def _calculate_target_price(self, data: dict) -> float:
        """计算目标价格"""
        current_price = data['stock_info']['current_price']
        score = data['comprehensive_score']
        
        if score >= 80:
            return round(current_price * 1.25, 2)  # 25%上涨空间
        elif score >= 60:
            return round(current_price * 1.15, 2)  # 15%上涨空间
        else:
            return round(current_price * 1.05, 2)  # 5%上涨空间
    
    def _calculate_stop_loss(self, data: dict) -> float:
        """计算止损价格"""
        current_price = data['stock_info']['current_price']
        return round(current_price * 0.85, 2)  # 15%止损
    
    def _get_position_suggestion(self, score: int) -> str:
        """获取仓位建议"""
        if score >= 80:
            return "可适当加大仓位，建议3-5成"
        elif score >= 60:
            return "可适度配置，建议1-3成"
        elif score >= 40:
            return "小仓位试探，建议不超过1成"
        else:
            return "建议观望，暂不配置"
    
    def _save_json_data(self, filename: str, data: dict):
        """保存JSON数据"""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存: {file_path}")
    
    def generate_market_timing(self):
        """生成市场择时数据"""
        # 获取A股数据进行市场分析
        a_stocks = self.fetcher.get_all_a_stocks()
        
        if not a_stocks:
            return None
        
        # 计算市场指标
        rising_count = len([s for s in a_stocks if s['change_percent'] > 0])
        total_count = len(a_stocks)
        rising_ratio = rising_count / total_count if total_count > 0 else 0
        
        # 计算平均涨跌幅
        avg_change = sum([s['change_percent'] for s in a_stocks]) / total_count
        
        # 市场情绪判断
        if rising_ratio > 0.6 and avg_change > 1:
            market_phase = "牛市"
            position_suggestion = 0.8
            sentiment_score = 0.8
        elif rising_ratio > 0.4 and avg_change > -0.5:
            market_phase = "震荡市"
            position_suggestion = 0.6
            sentiment_score = 0.55
        else:
            market_phase = "熊市"
            position_suggestion = 0.3
            sentiment_score = 0.3
        
        market_timing = {
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "market_phase": market_phase,
            "position_suggestion": position_suggestion,
            "sentiment_score": sentiment_score,
            "market_stats": {
                "total_stocks": total_count,
                "rising_count": rising_count,
                "falling_count": total_count - rising_count,
                "rising_ratio": round(rising_ratio, 3),
                "average_change": round(avg_change, 2)
            },
            "recommendations": [
                f"按老刘'人弃我取'理念，当前可适度加仓到{int(position_suggestion*10)}成",
                "重点配置银行(估值低ROE稳定)、食品饮料(消费龙头)",
                "严格遵循'败于原价，死于抄底，终于杠杆'风控原则"
            ]
        }
        
        self._save_json_data("market_timing.json", market_timing)
        return market_timing

def main():
    """主函数"""
    generator = CompleteStockDataGenerator()
    
    print("开始生成完整股票数据...")
    
    # 1. 生成所有股票基础数据
    summary = generator.generate_all_stocks_data()
    
    # 2. 生成分析样本
    analysis_data = generator.generate_analysis_samples(30)  # 生成30个分析样本
    
    # 3. 生成市场择时数据
    market_timing = generator.generate_market_timing()
    
    print("\n数据生成完成汇总:")
    print(f"   总股票数: {summary['total_stocks']}")
    print(f"   A股: {summary['a_stocks_count']}")
    print(f"   港股: {summary['hk_stocks_count']}")
    print(f"   分析样本: {analysis_data['total_count']}")
    print(f"   市场阶段: {market_timing['market_phase'] if market_timing else '未知'}")
    print(f"   建议仓位: {market_timing['position_suggestion']*100 if market_timing else 0}%")

if __name__ == "__main__":
    main()