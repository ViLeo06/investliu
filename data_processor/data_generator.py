"""
主数据生成器
整合所有模块，生成静态JSON数据文件
"""

import os
import sys
import json
import logging
from datetime import datetime
import time

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processor.stock_data_fetcher import StockDataFetcher
from data_processor.stock_analyzer import StockAnalyzer

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataGenerator:
    def __init__(self, output_dir="static_data"):
        self.output_dir = output_dir
        self.fetcher = StockDataFetcher()
        self.analyzer = StockAnalyzer()
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_all_data(self):
        """生成所有静态数据文件"""
        try:
            logger.info("开始生成静态数据文件...")
            
            # 1. 获取市场指数数据
            logger.info("获取市场指数数据...")
            market_indices = self.fetcher.get_market_index()
            self._save_json(market_indices, 'market_indices.json')
            
            # 2. 分析市场择时
            logger.info("分析市场择时...")
            market_timing = self.analyzer.analyze_market_timing(market_indices)
            self._save_json(market_timing, 'market_timing.json')
            
            # 3. 获取A股数据
            logger.info("获取A股数据...")
            a_stocks = self._get_stock_data_batch('A', pages=3)
            
            # 4. 分析A股推荐
            logger.info("分析A股推荐...")
            a_recommendations = self.analyzer.generate_stock_recommendations(a_stocks, top_n=20)
            self._save_json(a_recommendations, 'stocks_a_recommendations.json')
            
            # 5. 获取港股数据
            logger.info("获取港股数据...")
            hk_stocks = self._get_stock_data_batch('HK', pages=2)
            
            # 6. 分析港股推荐
            logger.info("分析港股推荐...")
            hk_recommendations = self.analyzer.generate_stock_recommendations(hk_stocks, top_n=15)
            self._save_json(hk_recommendations, 'stocks_hk_recommendations.json')
            
            # 7. 生成投资组合建议
            logger.info("生成投资组合建议...")
            all_recommendations = a_recommendations + hk_recommendations
            portfolio = self.analyzer.generate_portfolio_suggestion(all_recommendations, market_timing)
            self._save_json(portfolio, 'portfolio_suggestion.json')
            
            # 8. 生成汇总数据
            logger.info("生成汇总数据...")
            summary = self._generate_summary(market_timing, a_recommendations, hk_recommendations, portfolio)
            self._save_json(summary, 'summary.json')
            
            # 9. 生成完整的股票列表（分页）
            self._generate_stock_lists(a_stocks, hk_stocks)
            
            logger.info("所有数据文件生成完成！")
            return True
            
        except Exception as e:
            logger.error(f"生成数据文件失败: {e}")
            return False
    
    def _get_stock_data_batch(self, market_type, pages=3):
        """批量获取股票数据"""
        all_stocks = []
        
        for page in range(1, pages + 1):
            try:
                logger.info(f"获取{market_type}股第{page}页数据...")
                
                if market_type == 'A':
                    stocks = self.fetcher.get_stock_list_a(page=page, size=100)
                elif market_type == 'HK':
                    stocks = self.fetcher.get_stock_list_hk(page=page, size=100)
                else:
                    continue
                
                if stocks:
                    all_stocks.extend(stocks)
                    logger.info(f"获取到{len(stocks)}只股票")
                
                time.sleep(1)  # 避免请求过频
                
            except Exception as e:
                logger.error(f"获取{market_type}股第{page}页失败: {e}")
                continue
        
        logger.info(f"{market_type}股总计获取: {len(all_stocks)} 只")
        return all_stocks
    
    def _generate_summary(self, market_timing, a_recommendations, hk_recommendations, portfolio):
        """生成汇总数据"""
        return {
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'market_status': {
                'sentiment': market_timing.get('market_sentiment', 'neutral'),
                'recommended_position': market_timing.get('recommended_position', 0.5),
                'main_signals': market_timing.get('signals', [])[:3]
            },
            'recommendations_count': {
                'a_stocks': len(a_recommendations),
                'hk_stocks': len(hk_recommendations),
                'total': len(a_recommendations) + len(hk_recommendations)
            },
            'top_picks': {
                'a_stocks': a_recommendations[:5] if a_recommendations else [],
                'hk_stocks': hk_recommendations[:5] if hk_recommendations else []
            },
            'portfolio_risk': portfolio.get('risk_level', 'medium'),
            'investment_suggestions': portfolio.get('suggestions', [])[:3],
            'version': '1.0'
        }
    
    def _generate_stock_lists(self, a_stocks, hk_stocks):
        """生成完整的股票列表（分页）"""
        # A股列表分页
        self._paginate_and_save(a_stocks, 'stocks_a_page', page_size=50)
        
        # 港股列表分页  
        self._paginate_and_save(hk_stocks, 'stocks_hk_page', page_size=50)
        
        # 生成分页索引
        a_pages = (len(a_stocks) + 49) // 50  # 向上取整
        hk_pages = (len(hk_stocks) + 49) // 50
        
        pagination_info = {
            'a_stocks': {
                'total_count': len(a_stocks),
                'total_pages': a_pages,
                'page_size': 50
            },
            'hk_stocks': {
                'total_count': len(hk_stocks),
                'total_pages': hk_pages,
                'page_size': 50
            },
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self._save_json(pagination_info, 'pagination_info.json')
    
    def _paginate_and_save(self, stocks, filename_prefix, page_size=50):
        """分页保存股票列表"""
        for i in range(0, len(stocks), page_size):
            page_num = i // page_size + 1
            page_stocks = stocks[i:i + page_size]
            
            filename = f"{filename_prefix}_{page_num}.json"
            self._save_json(page_stocks, filename)
    
    def _save_json(self, data, filename):
        """保存JSON文件"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"保存文件: {filepath}")
        except Exception as e:
            logger.error(f"保存文件失败 {filename}: {e}")
    
    def generate_config_file(self):
        """生成配置文件"""
        config = {
            'api_endpoints': {
                'base_url': 'https://your-username.github.io/investliu',
                'summary': '/static_data/summary.json',
                'market_timing': '/static_data/market_timing.json',
                'a_stocks_recommendations': '/static_data/stocks_a_recommendations.json',
                'hk_stocks_recommendations': '/static_data/stocks_hk_recommendations.json',
                'portfolio': '/static_data/portfolio_suggestion.json',
                'pagination': '/static_data/pagination_info.json'
            },
            'update_frequency': '24h',
            'cache_duration': '1h',
            'version': '1.0',
            'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self._save_json(config, 'config.json')
        
        # 同时生成一个适合小程序的简化配置
        miniprogram_config = {
            'baseUrl': config['api_endpoints']['base_url'],
            'endpoints': config['api_endpoints'],
            'updateTime': config['generated_time']
        }
        
        self._save_json(miniprogram_config, 'miniprogram_config.json')
    
    def validate_generated_data(self):
        """验证生成的数据文件"""
        required_files = [
            'summary.json',
            'market_timing.json', 
            'stocks_a_recommendations.json',
            'stocks_hk_recommendations.json',
            'portfolio_suggestion.json',
            'config.json'
        ]
        
        missing_files = []
        valid_files = []
        
        for filename in required_files:
            filepath = os.path.join(self.output_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        json.load(f)  # 验证JSON格式
                    valid_files.append(filename)
                except json.JSONDecodeError:
                    logger.error(f"JSON格式错误: {filename}")
                    missing_files.append(filename)
            else:
                missing_files.append(filename)
        
        logger.info(f"验证完成 - 有效文件: {len(valid_files)}, 缺失文件: {len(missing_files)}")
        
        if missing_files:
            logger.warning(f"缺失文件: {missing_files}")
            return False
        
        return True

def main():
    """主函数"""
    generator = DataGenerator()
    
    logger.info("=== 老刘投资决策系统 - 数据生成器 ===")
    
    # 生成所有数据
    success = generator.generate_all_data()
    
    if success:
        # 生成配置文件
        generator.generate_config_file()
        
        # 验证数据
        if generator.validate_generated_data():
            logger.info("✅ 数据生成完成且验证通过！")
            logger.info(f"📁 输出目录: {os.path.abspath(generator.output_dir)}")
            logger.info("🚀 可以部署到GitHub Pages了")
        else:
            logger.error("❌ 数据验证失败")
    else:
        logger.error("❌ 数据生成失败")

if __name__ == "__main__":
    main()