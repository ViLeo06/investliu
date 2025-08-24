# 股票分析API服务
from stock_analysis_engine import StockAnalysisEngine
import json
from datetime import datetime
import os

class StockAnalysisAPI:
    """为小程序提供股票分析数据的API服务"""
    
    def __init__(self):
        self.analyzer = StockAnalysisEngine()
        self.output_dir = "analysis_results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def analyze_single_stock(self, stock_code: str, market: str = 'A') -> dict:
        """分析单只股票并生成JSON数据"""
        try:
            # 执行综合分析
            analysis_result = self.analyzer.comprehensive_analysis(stock_code, market)
            
            # 为小程序优化数据结构
            optimized_result = self._optimize_for_miniprogram(analysis_result)
            
            # 保存到JSON文件
            output_file = os.path.join(self.output_dir, f"{stock_code}_{market.lower()}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(optimized_result, f, ensure_ascii=False, indent=2)
            
            print(f"分析 {stock_code} 分析数据生成成功: {output_file}")
            return optimized_result
            
        except Exception as e:
            print(f"分析 {stock_code} 失败: {e}")
            return self._generate_error_response(stock_code, str(e))
    
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
                "dividend_yield": raw_data['financial_metrics']['dividend_yield']
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
            },
            
            # 元数据
            "metadata": {
                "analysis_time": raw_data['analysis_time'],
                "data_sources": raw_data['data_sources'],
                "version": raw_data['version'],
                "cache_duration": 3600,  # 1小时缓存
                "searchable_content": self._generate_searchable_content(raw_data)
            }
        }
    
    def _extract_key_points(self, ai_analysis: str) -> list:
        """从AI分析中提取关键点"""
        try:
            # 简单的关键点提取逻辑
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
    
    def _generate_searchable_content(self, data: dict) -> str:
        """生成可搜索的内容"""
        searchable_parts = [
            data['stock_info']['name'],
            data['stock_info']['code'], 
            data['stock_info']['industry'],
            data['laoliu_evaluation']['investment_advice']
        ]
        
        # 添加分析要点
        searchable_parts.extend(data['laoliu_evaluation']['analysis_points'])
        
        return ' '.join(filter(None, searchable_parts))
    
    def _generate_error_response(self, stock_code: str, error_msg: str) -> dict:
        """生成错误响应"""
        return {
            "error": True,
            "error_message": error_msg,
            "stock_code": stock_code,
            "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def batch_analyze(self, stock_list: list) -> dict:
        """批量分析股票"""
        results = {}
        success_count = 0
        
        for stock_info in stock_list:
            stock_code = stock_info['code']
            market = stock_info.get('market', 'A')
            
            try:
                result = self.analyze_single_stock(stock_code, market)
                if not result.get('error'):
                    success_count += 1
                results[stock_code] = result
            except Exception as e:
                results[stock_code] = self._generate_error_response(stock_code, str(e))
        
        return {
            "total": len(stock_list),
            "success": success_count,
            "failed": len(stock_list) - success_count,
            "results": results,
            "batch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_analysis_data():
    """生成分析数据供小程序使用"""
    api = StockAnalysisAPI()
    
    # 测试股票列表
    test_stocks = [
        {'code': '000001', 'market': 'A'},  # 平安银行
        {'code': '600036', 'market': 'A'},  # 招商银行  
        {'code': '000858', 'market': 'A'},  # 五粮液
        {'code': '600519', 'market': 'A'},  # 贵州茅台
        {'code': '000002', 'market': 'A'},  # 万科A
        {'code': '01398', 'market': 'HK'}, # 工商银行H股
    ]
    
    print("开始批量生成股票分析数据...")
    batch_result = api.batch_analyze(test_stocks)
    
    print(f"批量分析完成:")
    print(f"   总数: {batch_result['total']}")
    print(f"   成功: {batch_result['success']}")  
    print(f"   失败: {batch_result['failed']}")
    
    # 生成汇总文件供小程序使用
    summary_file = os.path.join(api.output_dir, "analysis_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(batch_result, f, ensure_ascii=False, indent=2)
    
    print(f"汇总数据已保存: {summary_file}")

if __name__ == "__main__":
    generate_analysis_data()