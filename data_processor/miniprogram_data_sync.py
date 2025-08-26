# 小程序数据同步器 - 将真实股票数据同步到小程序
import json
import os
import sys
from datetime import datetime
from typing import Dict, List
from stock_analysis_engine import StockAnalysisEngine
from real_time_stock_fetcher import RealTimeStockFetcher

class MiniprogramDataSync:
    """
    小程序数据同步器
    负责将真实股票数据格式化并导出到小程序可用的格式
    """
    
    def __init__(self):
        self.analysis_engine = StockAnalysisEngine()
        self.fetcher = RealTimeStockFetcher()
        self.output_dir = "../miniprogram"
        self.static_data_dir = "../static_data"
        
    def sync_stock_list(self, market: str = 'A', limit: int = 100) -> Dict:
        """同步股票列表数据"""
        print(f"正在同步{market}股票票列表...")
        
        try:
            if market == 'A':
                stocks = self.fetcher.get_all_a_stocks()
            elif market == 'HK':
                stocks = self.fetcher.get_all_hk_stocks()
            else:
                raise ValueError("不支持的市场类型")
            
            # 限制数量并排序（按市值排序）
            stocks = sorted(stocks[:limit*2], key=lambda x: x.get('market_cap', 0), reverse=True)[:limit]
            
            # 格式化数据
            formatted_data = {
                "total_count": len(stocks),
                "market": f"{market}股",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "stocks": []
            }
            
            for stock in stocks:
                # 简化分析（快速版本）
                try:
                    quick_analysis = self.analysis_engine.quick_analysis(stock['code'], market)
                    formatted_stock = {
                        **stock,
                        "laoliu_score": quick_analysis.get('laoliu_score', 50),
                        "investment_advice": quick_analysis.get('investment_advice', '待分析'),
                        "recommendation": quick_analysis.get('recommendation', 'hold'),
                        "analysis_points": quick_analysis.get('analysis_points', []),
                        "risk_warnings": quick_analysis.get('risk_warnings', []),
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    formatted_data["stocks"].append(formatted_stock)
                except Exception as e:
                    print(f"分析股票 {stock['code']} 失败: {e}")
                    # 使用原始数据
                    formatted_data["stocks"].append({
                        **stock,
                        "laoliu_score": 50,
                        "investment_advice": "待分析",
                        "recommendation": "hold",
                        "analysis_points": [],
                        "risk_warnings": [],
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return formatted_data
            
        except Exception as e:
            print(f"同步股票列表失败: {e}")
            return {"total_count": 0, "stocks": []}
    
    def sync_analysis_samples(self, codes: List[str], limit: int = 20) -> Dict:
        """同步详细分析样本数据"""
        print("正在同步详细分析样本...")
        
        analysis_results = []
        
        for code in codes[:limit]:
            try:
                print(f"正在分析股票: {code}")
                
                # 获取完整分析
                analysis = self.analysis_engine.comprehensive_analysis(code)
                
                if analysis:
                    analysis_results.append(analysis)
                    print(f"✓ {code} 分析完成")
                else:
                    print(f"✗ {code} 分析失败")
                
            except Exception as e:
                print(f"分析股票 {code} 出错: {e}")
                continue
        
        return {
            "total_count": len(analysis_results),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_results": analysis_results
        }
    
    def create_search_index(self, stocks: List[Dict]) -> Dict:
        """创建股票搜索索引"""
        search_index = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stocks": {}
        }
        
        for stock in stocks:
            code = stock['code']
            search_index["stocks"][code] = {
                "code": code,
                "name": stock['name'],
                "market": stock.get('market', 'A'),
                "industry": stock.get('industry', '未知'),
                "pinyin": self.get_pinyin(stock['name']),  # 需要实现拼音转换
                "keywords": [stock['name'], code, stock.get('industry', '')]
            }
        
        return search_index
    
    def get_pinyin(self, text: str) -> str:
        """获取文字拼音简拼（简单实现）"""
        # 这里可以集成pypinyin库实现更完整的拼音转换
        return text  # 简单返回原文，实际项目中需要拼音库
    
    def export_to_files(self):
        """导出所有数据到文件"""
        print("开始导出数据到小程序...")
        
        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.static_data_dir, exist_ok=True)
        
        try:
            # 1. 同步A股数据
            print("1. 同步A股数据...")
            a_stocks = self.sync_stock_list('A', 50)
            
            with open(f"{self.output_dir}/stocks_a.json", 'w', encoding='utf-8') as f:
                json.dump(a_stocks, f, ensure_ascii=False, indent=2)
            
            with open(f"{self.static_data_dir}/stocks_a.json", 'w', encoding='utf-8') as f:
                json.dump(a_stocks, f, ensure_ascii=False, indent=2)
            
            print(f"✓ A股数据导出完成: {len(a_stocks['stocks'])}只")
            
            # 2. 同步港股数据
            print("2. 同步港股数据...")
            hk_stocks = self.sync_stock_list('HK', 30)
            
            with open(f"{self.output_dir}/stocks_hk.json", 'w', encoding='utf-8') as f:
                json.dump(hk_stocks, f, ensure_ascii=False, indent=2)
            
            with open(f"{self.static_data_dir}/stocks_hk.json", 'w', encoding='utf-8') as f:
                json.dump(hk_stocks, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 港股数据导出完成: {len(hk_stocks['stocks'])}只")
            
            # 3. 同步详细分析数据（精选股票）
            print("3. 同步详细分析数据...")
            selected_codes = [
                '000651',  # 格力电器
                '000333',  # 美的集团
                '600519',  # 贵州茅台
                '000858',  # 五粮液
                '600036',  # 招商银行
                '000001',  # 平安银行
                '01398',   # 工商银行(H)
                '00700',   # 腾讯控股
                '00941',   # 中国移动
                '002415'   # 海康威视
            ]
            
            analysis_data = self.sync_analysis_samples(selected_codes, 10)
            
            with open(f"{self.output_dir}/analysis_samples.json", 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
                
            with open(f"{self.static_data_dir}/analysis_samples.json", 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 详细分析数据导出完成: {len(analysis_data['analysis_results'])}只")
            
            # 4. 创建搜索索引
            print("4. 创建搜索索引...")
            all_stocks = a_stocks['stocks'] + hk_stocks['stocks']
            search_index = self.create_search_index(all_stocks)
            
            with open(f"{self.output_dir}/stock_search_index.json", 'w', encoding='utf-8') as f:
                json.dump(search_index, f, ensure_ascii=False, indent=2)
            
            with open(f"{self.static_data_dir}/stock_search_index.json", 'w', encoding='utf-8') as f:
                json.dump(search_index, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 搜索索引创建完成: {len(search_index['stocks'])}只股票")
            
            # 5. 生成摘要信息
            summary = {
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "market_status": {
                    "a_stocks_count": len(a_stocks['stocks']),
                    "hk_stocks_count": len(hk_stocks['stocks']),
                    "analysis_count": len(analysis_data['analysis_results']),
                    "total_stocks": len(all_stocks)
                },
                "data_sources": ["akshare", "实时API"],
                "next_update": "每日更新"
            }
            
            with open(f"{self.output_dir}/summary.json", 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
                
            with open(f"{self.static_data_dir}/summary.json", 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print("✓ 所有数据导出完成！")
            print(f"输出目录: {self.output_dir}")
            print(f"静态数据目录: {self.static_data_dir}")
            
            return True
            
        except Exception as e:
            print(f"导出数据失败: {e}")
            return False

def main():
    """主函数"""
    print("=== 小程序数据同步器 ===")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    syncer = MiniprogramDataSync()
    
    try:
        success = syncer.export_to_files()
        
        if success:
            print("\n🎉 数据同步完成！")
            print("请重启小程序开发工具以加载新数据")
        else:
            print("\n❌ 数据同步失败！")
            
    except Exception as e:
        print(f"\n❌ 同步过程出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
