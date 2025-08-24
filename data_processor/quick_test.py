# 快速测试实时数据获取和小程序数据结构
from real_time_stock_fetcher import RealTimeStockFetcher
from stock_analysis_engine import StockAnalysisEngine
import json
from datetime import datetime

def quick_test():
    print("开始快速测试实时数据获取...")
    
    # 初始化组件
    fetcher = RealTimeStockFetcher()
    analyzer = StockAnalysisEngine()
    
    # 测试搜索功能
    print("\n1. 测试股票搜索...")
    search_results = fetcher.search_stocks("平安", "A")
    print(f"搜索'平安'的结果: {len(search_results)} 只股票")
    
    if search_results:
        for i, stock in enumerate(search_results[:3]):
            print(f"  {i+1}. {stock['name']} ({stock['code']}) - ¥{stock['current_price']} ({stock['change_percent']:+.1f}%)")
    
    # 测试详细分析
    print("\n2. 测试股票分析...")
    test_stock = "000001"  # 平安银行
    try:
        analysis_result = analyzer.comprehensive_analysis(test_stock, "A")
        print(f"分析 {test_stock} 成功:")
        print(f"  股票名称: {analysis_result['stock_info']['name']}")
        print(f"  当前价格: ¥{analysis_result['stock_info']['current_price']}")
        print(f"  老刘评分: {analysis_result['laoliu_evaluation']['laoliu_score']}")
        print(f"  投资建议: {analysis_result['laoliu_evaluation']['investment_advice']}")
        
        # 生成小程序格式数据
        miniprogram_data = {
            "basic_info": {
                "code": analysis_result['stock_info']['code'],
                "name": analysis_result['stock_info']['name'],
                "current_price": analysis_result['stock_info']['current_price'],
                "change_percent": analysis_result['stock_info']['change_percent'],
                "industry": analysis_result['stock_info']['industry'],
                "update_time": analysis_result['stock_info']['update_time']
            },
            "laoliu_evaluation": {
                "laoliu_score": analysis_result['laoliu_evaluation']['laoliu_score'],
                "investment_advice": analysis_result['laoliu_evaluation']['investment_advice'],
                "analysis_points": analysis_result['laoliu_evaluation']['analysis_points'][:3]
            },
            "investment_summary": {
                "recommendation": analysis_result['investment_recommendation'],
                "comprehensive_score": analysis_result['comprehensive_score']
            }
        }
        
        # 保存测试数据供小程序使用
        with open('test_analysis_data.json', 'w', encoding='utf-8') as f:
            json.dump([miniprogram_data], f, ensure_ascii=False, indent=2)
        
        print(f"  测试数据已保存到 test_analysis_data.json")
        
    except Exception as e:
        print(f"分析失败: {e}")
    
    # 测试市场数据概览
    print("\n3. 测试市场概览...")
    a_stocks_sample = fetcher.get_all_a_stocks()[:10]  # 获取前10只作为样本
    
    if a_stocks_sample:
        rising_count = len([s for s in a_stocks_sample if s['change_percent'] > 0])
        avg_change = sum([s['change_percent'] for s in a_stocks_sample]) / len(a_stocks_sample)
        
        print(f"  样本股票数: {len(a_stocks_sample)}")
        print(f"  上涨股票: {rising_count} 只")
        print(f"  平均涨跌: {avg_change:+.2f}%")
        
        # 生成市场概览数据
        market_overview = {
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sample_stats": {
                "total_sample": len(a_stocks_sample),
                "rising_count": rising_count,
                "average_change": round(avg_change, 2)
            },
            "top_stocks": [{
                "code": stock['code'],
                "name": stock['name'],
                "price": stock['current_price'],
                "change": stock['change_percent']
            } for stock in a_stocks_sample[:5]]
        }
        
        with open('market_overview_test.json', 'w', encoding='utf-8') as f:
            json.dump(market_overview, f, ensure_ascii=False, indent=2)
        
        print(f"  市场概览数据已保存到 market_overview_test.json")
    
    print("\n✓ 快速测试完成!")
    print("生成的文件:")
    print("  - test_analysis_data.json (股票分析测试数据)")
    print("  - market_overview_test.json (市场概览测试数据)")

if __name__ == "__main__":
    quick_test()