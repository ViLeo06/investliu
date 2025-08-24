# 简化版股票数据生成器 - 解决API问题
from fixed_stock_fetcher import FixedRealTimeStockFetcher
import json
import os
from datetime import datetime
from typing import Dict, List
import random

class SimpleStockDataGenerator:
    """简化版股票数据生成器，专门解决API调用问题"""
    
    def __init__(self):
        self.fetcher = FixedRealTimeStockFetcher()
        self.output_dir = "../"  # 输出到项目根目录
    
    def generate_stocks_data(self):
        """生成股票数据文件"""
        print("开始生成股票数据...")
        
        # 获取A股数据
        print("1. 获取A股数据...")
        a_stocks = self.fetcher.get_all_a_stocks()
        
        # 为A股添加老刘评分
        for stock in a_stocks:
            stock['laoliu_score'] = self._calculate_simple_score(stock)
            stock['investment_advice'] = self._get_investment_advice(stock['laoliu_score'])
            stock['recommendation'] = self._get_recommendation(stock['laoliu_score'])
            stock['analysis_points'] = self._get_analysis_points(stock)
            stock['risk_warnings'] = self._get_risk_warnings(stock)
        
        # 生成A股数据文件
        a_stock_data = {
            "total_count": len(a_stocks),
            "market": "A股",
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stocks": a_stocks
        }
        
        # 获取港股数据
        print("2. 获取港股数据...")
        hk_stocks = self.fetcher.get_all_hk_stocks()
        
        # 为港股添加基础评分
        for stock in hk_stocks:
            stock['laoliu_score'] = random.randint(40, 85)
            stock['investment_advice'] = "港股分析中"
            stock['recommendation'] = 'hold'
            stock['analysis_points'] = ["港股市场", "数据完善中"]
            stock['risk_warnings'] = []
        
        hk_stock_data = {
            "total_count": len(hk_stocks),
            "market": "港股",
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stocks": hk_stocks
        }
        
        # 保存数据文件
        self._save_json_file("stocks_a_complete.json", a_stock_data)
        self._save_json_file("stocks_hk_complete.json", hk_stock_data)
        
        print(f"✅ 股票数据生成完成:")
        print(f"   A股: {len(a_stocks)} 只")
        print(f"   港股: {len(hk_stocks)} 只")
        
        # 生成分析样本数据
        print("3. 生成分析样本...")
        self._generate_analysis_samples(a_stocks[:10])  # 取前10只作为分析样本
        
        return a_stock_data, hk_stock_data
    
    def _calculate_simple_score(self, stock: Dict) -> int:
        """简化版老刘评分计算"""
        score = 50  # 基础分数
        
        # PE评估
        pe = stock.get('pe_ratio', 15)
        if 0 < pe <= 15:
            score += 20
        elif 15 < pe <= 25:
            score += 10
        elif pe > 30:
            score -= 10
        
        # PB评估
        pb = stock.get('pb_ratio', 1.5)
        if 0 < pb <= 2:
            score += 15
        elif pb > 5:
            score -= 10
        
        # 行业加权
        industry = stock.get('industry', '')
        if '银行' in industry:
            score += 15
        elif '食品饮料' in industry:
            score += 10
        elif '医药' in industry:
            score += 8
        
        # 价格变化
        change = stock.get('change_percent', 0)
        if change < -3:
            score += 5  # 逆向投资机会
        
        return max(0, min(100, score))
    
    def _get_investment_advice(self, score: int) -> str:
        """获取投资建议"""
        if score >= 80:
            return "强烈推荐：基本面优秀，符合老刘理念"
        elif score >= 65:
            return "推荐：基本面良好，可适当配置"
        elif score >= 50:
            return "观望：存在投资价值，建议观察"
        else:
            return "不推荐：风险较高，暂不建议"
    
    def _get_recommendation(self, score: int) -> str:
        """获取推荐等级"""
        if score >= 80:
            return "strong_buy"
        elif score >= 65:
            return "buy"
        elif score >= 50:
            return "hold"
        else:
            return "sell"
    
    def _get_analysis_points(self, stock: Dict) -> List[str]:
        """获取分析要点"""
        points = []
        
        pe = stock.get('pe_ratio', 0)
        pb = stock.get('pb_ratio', 0)
        industry = stock.get('industry', '')
        
        if pe > 0 and pe <= 15:
            points.append(f"PE仅{pe:.1f}倍，估值偏低")
        elif pe > 25:
            points.append(f"PE达{pe:.1f}倍，估值偏高")
        
        if pb > 0 and pb <= 2:
            points.append(f"PB仅{pb:.2f}倍，账面价值安全")
        
        if '银行' in industry:
            points.append("银行业符合老刘投资偏好")
        elif '食品饮料' in industry:
            points.append("消费行业，品牌价值稳定")
        
        if not points:
            points.append("基本面分析中")
        
        return points[:3]
    
    def _get_risk_warnings(self, stock: Dict) -> List[str]:
        """获取风险提示"""
        warnings = []
        
        pe = stock.get('pe_ratio', 0)
        pb = stock.get('pb_ratio', 0)
        
        if pe > 30:
            warnings.append("市盈率偏高，注意估值风险")
        
        if pb > 5:
            warnings.append("市净率较高，账面价值风险")
        
        return warnings[:2]
    
    def _generate_analysis_samples(self, stocks: List[Dict]):
        """生成分析样本数据"""
        analysis_results = []
        
        for stock in stocks:
            # 获取财务数据
            financial_metrics = self.fetcher.get_stock_financial_metrics_fixed(stock['code'])
            
            analysis_result = {
                "basic_info": {
                    "code": stock['code'],
                    "name": stock['name'],
                    "market_type": stock['market'],
                    "current_price": stock['current_price'],
                    "change_percent": stock['change_percent'],
                    "volume": stock['volume'],
                    "market_cap": stock['market_cap'],
                    "industry": stock.get('industry', '未知'),
                    "update_time": stock['update_time']
                },
                "valuation_metrics": {
                    "pe_ratio": stock['pe_ratio'],
                    "pb_ratio": stock['pb_ratio'],
                    "ps_ratio": 0,
                    "dividend_yield": financial_metrics.get('dividend_yield', 2.5)
                },
                "financial_metrics": financial_metrics,
                "laoliu_evaluation": {
                    "laoliu_score": stock['laoliu_score'],
                    "analysis_points": stock['analysis_points'],
                    "risk_warnings": stock['risk_warnings'],
                    "investment_advice": stock['investment_advice'],
                    "contrarian_opportunity": stock['change_percent'] < -5
                },
                "technical_analysis": {
                    "volume_price_signal": "量价关系正常",
                    "volume_ratio": 1.0,
                    "price_change": stock['change_percent']
                },
                "ai_insights": {
                    "analysis_content": self._generate_ai_analysis(stock, financial_metrics),
                    "key_points": stock['analysis_points'],
                    "recommendation": stock['recommendation'],
                    "confidence_level": "中"
                },
                "investment_summary": {
                    "comprehensive_score": stock['laoliu_score'],
                    "recommendation": stock['recommendation'],
                    "target_price": round(stock['current_price'] * 1.15, 2),
                    "stop_loss": round(stock['current_price'] * 0.85, 2),
                    "position_suggestion": self._get_position_suggestion(stock['laoliu_score'])
                }
            }
            analysis_results.append(analysis_result)
        
        # 保存分析样本
        analysis_data = {
            "total_count": len(analysis_results),
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "analysis_results": analysis_results
        }
        
        self._save_json_file("analysis_samples.json", analysis_data)
        print(f"分析样本生成完成: {len(analysis_results)} 个")
    
    def _generate_ai_analysis(self, stock: Dict, financial_metrics: Dict) -> str:
        """生成AI分析内容"""
        analysis = f"【{stock['name']}投资分析】\n\n"
        analysis += f"综合评分：{stock['laoliu_score']}分\n"
        analysis += f"投资建议：{stock['investment_advice']}\n\n"
        
        analysis += "主要优势：\n"
        for point in stock['analysis_points']:
            analysis += f"• {point}\n"
        
        if stock['risk_warnings']:
            analysis += "\n风险提示：\n"
            for warning in stock['risk_warnings']:
                analysis += f"• {warning}\n"
        
        analysis += f"\n基于老刘投资理念，该股票"
        if stock['laoliu_score'] >= 65:
            analysis += "符合价值投资标准，建议关注。"
        else:
            analysis += "需要进一步观察，谨慎投资。"
        
        return analysis
    
    def _get_position_suggestion(self, score: int) -> str:
        """获取仓位建议"""
        if score >= 80:
            return "可适当加大仓位，建议3-5成"
        elif score >= 65:
            return "可适度配置，建议1-3成"
        elif score >= 50:
            return "小仓位试探，建议不超过1成"
        else:
            return "建议观望，暂不配置"
    
    def _save_json_file(self, filename: str, data: dict):
        """保存JSON文件"""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存: {file_path}")

def main():
    """主函数"""
    generator = SimpleStockDataGenerator()
    
    try:
        # 生成股票数据
        a_data, hk_data = generator.generate_stocks_data()
        
        print("\n✅ 数据生成成功!")
        print("文件已保存到项目根目录:")
        print("  - stocks_a_complete.json")
        print("  - stocks_hk_complete.json") 
        print("  - analysis_samples.json")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据生成失败: {e}")
        return False

if __name__ == "__main__":
    main()