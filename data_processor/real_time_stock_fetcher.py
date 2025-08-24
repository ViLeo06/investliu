# 实时股票数据获取引擎 - 支持A股和港股
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class RealTimeStockFetcher:
    """
    实时股票数据获取引擎
    集成akshare等免费API，支持A股和港股全量数据
    """
    
    def __init__(self):
        self.cache = {}  # 简单缓存机制
        self.cache_duration = 300  # 5分钟缓存
        self.retry_attempts = 3
        
    def get_all_a_stocks(self) -> List[Dict]:
        """获取所有A股股票列表"""
        cache_key = "all_a_stocks"
        
        # 检查缓存
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            print("正在获取A股股票列表...")
            
            # 使用akshare获取A股票列表
            stock_list = ak.stock_zh_a_spot_em()
            
            # 数据清理和格式化
            formatted_stocks = []
            for _, row in stock_list.iterrows():
                try:
                    stock_info = {
                        'code': str(row['代码']),
                        'name': str(row['名称']),
                        'market': 'A',
                        'current_price': float(row['最新价']) if pd.notna(row['最新价']) else 0.0,
                        'change_percent': float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0.0,
                        'volume': int(row['成交量']) if pd.notna(row['成交量']) else 0,
                        'market_cap': float(row['总市值']) if pd.notna(row['总市值']) else 0.0,
                        'pe_ratio': float(row['市盈率-动态']) if pd.notna(row['市盈率-动态']) else 0.0,
                        'pb_ratio': float(row['市净率']) if pd.notna(row['市净率']) else 0.0,
                        'turnover_rate': float(row['换手率']) if pd.notna(row['换手率']) else 0.0,
                        'amplitude': float(row['振幅']) if pd.notna(row['振幅']) else 0.0,
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # 过滤无效数据
                    if stock_info['current_price'] > 0:
                        formatted_stocks.append(stock_info)
                        
                except Exception as e:
                    continue  # 跳过有问题的单行数据
            
            # 更新缓存
            self._update_cache(cache_key, formatted_stocks)
            
            print(f"成功获取 {len(formatted_stocks)} 只A股数据")
            return formatted_stocks
            
        except Exception as e:
            print(f"获取A股列表失败: {e}")
            return self._get_mock_a_stocks()
    
    def get_all_hk_stocks(self) -> List[Dict]:
        """获取所有港股股票列表"""
        cache_key = "all_hk_stocks"
        
        # 检查缓存
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            print("正在获取港股股票列表...")
            
            # 使用akshare获取港股列表
            hk_list = ak.stock_hk_spot()
            
            formatted_stocks = []
            for _, row in hk_list.iterrows():
                try:
                    stock_info = {
                        'code': str(row['symbol']),
                        'name': str(row['name']),
                        'market': 'HK',
                        'current_price': float(row['lasttrade']) if pd.notna(row['lasttrade']) else 0.0,
                        'change_percent': float(row['changepercent']) if pd.notna(row['changepercent']) else 0.0,
                        'volume': int(row['volume']) if pd.notna(row['volume']) else 0,
                        'market_cap': 0.0,  # 港股市值需要单独计算
                        'pe_ratio': 0.0,
                        'pb_ratio': 0.0,
                        'turnover_rate': 0.0,
                        'amplitude': 0.0,
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if stock_info['current_price'] > 0:
                        formatted_stocks.append(stock_info)
                        
                except Exception as e:
                    continue
            
            # 更新缓存
            self._update_cache(cache_key, formatted_stocks)
            
            print(f"成功获取 {len(formatted_stocks)} 只港股数据")
            return formatted_stocks
            
        except Exception as e:
            print(f"获取港股列表失败: {e}")
            return self._get_mock_hk_stocks()
    
    def get_stock_detail(self, stock_code: str, market: str = 'A') -> Optional[Dict]:
        """获取单只股票详细信息"""
        cache_key = f"stock_detail_{stock_code}_{market}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            if market.upper() == 'A':
                return self._get_a_stock_detail(stock_code)
            else:
                return self._get_hk_stock_detail(stock_code)
        except Exception as e:
            print(f"获取股票 {stock_code} 详细信息失败: {e}")
            return None
    
    def _get_a_stock_detail(self, stock_code: str) -> Optional[Dict]:
        """获取A股详细信息"""
        try:
            # 获取实时数据
            realtime_data = ak.stock_zh_a_spot_em()
            stock_data = realtime_data[realtime_data['代码'] == stock_code]
            
            if stock_data.empty:
                return None
            
            row = stock_data.iloc[0]
            
            # 获取财务数据
            financial_data = self._get_financial_data(stock_code)
            
            # 获取历史数据用于技术分析
            history_data = self._get_history_data(stock_code)
            
            stock_info = {
                'code': stock_code,
                'name': str(row['名称']),
                'market': 'A',
                'current_price': float(row['最新价']),
                'change_percent': float(row['涨跌幅']),
                'change_amount': float(row['涨跌额']),
                'volume': int(row['成交量']),
                'turnover': float(row['成交额']),
                'market_cap': float(row['总市值']),
                'circulation_cap': float(row['流通市值']),
                'pe_ratio': float(row['市盈率-动态']),
                'pb_ratio': float(row['市净率']),
                'turnover_rate': float(row['换手率']),
                'amplitude': float(row['振幅']),
                'highest': float(row['最高']),
                'lowest': float(row['最低']),
                'open_price': float(row['今开']),
                'close_yesterday': float(row['昨收']),
                'financial_metrics': financial_data,
                'technical_indicators': self._calculate_technical_indicators(history_data),
                'industry': self._get_stock_industry(stock_code),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 更新缓存
            cache_key = f"stock_detail_{stock_code}_A"
            self._update_cache(cache_key, stock_info)
            
            return stock_info
            
        except Exception as e:
            print(f"获取A股 {stock_code} 详细信息失败: {e}")
            return None
    
    def _get_hk_stock_detail(self, stock_code: str) -> Optional[Dict]:
        """获取港股详细信息"""
        try:
            hk_data = ak.stock_hk_spot()
            stock_data = hk_data[hk_data['symbol'] == stock_code]
            
            if stock_data.empty:
                return None
            
            row = stock_data.iloc[0]
            
            stock_info = {
                'code': stock_code,
                'name': str(row['name']),
                'market': 'HK',
                'current_price': float(row['lasttrade']),
                'change_percent': float(row['changepercent']),
                'volume': int(row['volume']),
                'pe_ratio': 0.0,  # 港股PE需要额外获取
                'pb_ratio': 0.0,
                'market_cap': 0.0,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            cache_key = f"stock_detail_{stock_code}_HK"
            self._update_cache(cache_key, stock_info)
            
            return stock_info
            
        except Exception as e:
            print(f"获取港股 {stock_code} 详细信息失败: {e}")
            return None
    
    def _get_financial_data(self, stock_code: str) -> Dict:
        """获取财务指标数据"""
        try:
            # 获取财务指标
            financial = ak.stock_financial_em(symbol=stock_code)
            if not financial.empty:
                latest = financial.iloc[0]
                return {
                    'roe': float(latest.get('净资产收益率', 0)),
                    'roa': float(latest.get('总资产收益率', 0)),
                    'debt_ratio': float(latest.get('资产负债率', 0)) / 100,
                    'current_ratio': float(latest.get('流动比率', 0)),
                    'gross_margin': float(latest.get('销售毛利率', 0)),
                    'net_margin': float(latest.get('销售净利率', 0)),
                    'revenue_growth': float(latest.get('营业总收入同比增长', 0)),
                    'profit_growth': float(latest.get('净利润同比增长', 0)),
                    'report_date': str(latest.get('报告期', ''))
                }
        except Exception as e:
            print(f"获取 {stock_code} 财务数据失败: {e}")
        
        # 返回默认值
        return {
            'roe': 0, 'roa': 0, 'debt_ratio': 0, 'current_ratio': 0,
            'gross_margin': 0, 'net_margin': 0, 'revenue_growth': 0,
            'profit_growth': 0, 'report_date': ''
        }
    
    def _get_history_data(self, stock_code: str, days: int = 30) -> pd.DataFrame:
        """获取历史数据"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            history = ak.stock_zh_a_hist(
                symbol=stock_code,
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d'),
                adjust="qfq"
            )
            return history
        except Exception as e:
            print(f"获取 {stock_code} 历史数据失败: {e}")
            return pd.DataFrame()
    
    def _calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """计算技术指标"""
        if df.empty or len(df) < 20:
            return {}
        
        try:
            # 计算移动平均线
            df['ma5'] = df['收盘'].rolling(window=5).mean()
            df['ma10'] = df['收盘'].rolling(window=10).mean()
            df['ma20'] = df['收盘'].rolling(window=20).mean()
            
            # 计算RSI
            delta = df['收盘'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # 计算MACD
            exp1 = df['收盘'].ewm(span=12).mean()
            exp2 = df['收盘'].ewm(span=26).mean()
            df['macd'] = exp1 - exp2
            df['signal'] = df['macd'].ewm(span=9).mean()
            
            latest = df.iloc[-1]
            
            return {
                'ma5': float(latest.get('ma5', 0)),
                'ma10': float(latest.get('ma10', 0)),
                'ma20': float(latest.get('ma20', 0)),
                'rsi': float(latest.get('rsi', 50)),
                'macd': float(latest.get('macd', 0)),
                'signal': float(latest.get('signal', 0)),
                'volume_trend': self._analyze_volume_trend(df)
            }
            
        except Exception as e:
            print(f"计算技术指标失败: {e}")
            return {}
    
    def _analyze_volume_trend(self, df: pd.DataFrame) -> str:
        """分析成交量趋势"""
        if len(df) < 5:
            return "数据不足"
        
        try:
            recent_volume = df['成交量'].tail(5).mean()
            previous_volume = df['成交量'].iloc[-10:-5].mean()
            
            if recent_volume > previous_volume * 1.5:
                return "放量"
            elif recent_volume < previous_volume * 0.5:
                return "缩量"
            else:
                return "正常"
        except:
            return "正常"
    
    def _get_stock_industry(self, stock_code: str) -> str:
        """获取股票所属行业"""
        try:
            industry_data = ak.stock_individual_info_em(symbol=stock_code)
            if isinstance(industry_data, dict) and '行业' in industry_data:
                return str(industry_data['行业'])
        except:
            pass
        return "未知"
    
    def search_stocks(self, query: str, market: str = 'ALL') -> List[Dict]:
        """搜索股票"""
        all_stocks = []
        
        if market.upper() in ['A', 'ALL']:
            all_stocks.extend(self.get_all_a_stocks())
        
        if market.upper() in ['HK', 'ALL']:
            all_stocks.extend(self.get_all_hk_stocks())
        
        if not query:
            return all_stocks[:100]  # 返回前100只
        
        query = query.upper().strip()
        filtered_stocks = []
        
        for stock in all_stocks:
            # 搜索股票代码、名称
            if (query in stock['code'].upper() or 
                query in stock['name'].upper()):
                filtered_stocks.append(stock)
        
        return filtered_stocks[:50]  # 最多返回50个搜索结果
    
    def _is_cache_valid(self, key: str) -> bool:
        """检查缓存是否有效"""
        if key not in self.cache:
            return False
        
        cache_time = self.cache[key]['timestamp']
        return (datetime.now().timestamp() - cache_time) < self.cache_duration
    
    def _update_cache(self, key: str, data: any):
        """更新缓存"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now().timestamp()
        }
    
    def _get_mock_a_stocks(self) -> List[Dict]:
        """获取模拟A股数据（作为备用）"""
        return [
            {
                'code': '000001', 'name': '平安银行', 'market': 'A',
                'current_price': 12.85, 'change_percent': -0.8, 'volume': 5234567,
                'market_cap': 24785432100, 'pe_ratio': 5.2, 'pb_ratio': 0.78,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'code': '600036', 'name': '招商银行', 'market': 'A', 
                'current_price': 43.12, 'change_percent': 1.2, 'volume': 2253764,
                'market_cap': 627191697440, 'pe_ratio': 6.1, 'pb_ratio': 1.05,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'code': '000858', 'name': '五粮液', 'market': 'A',
                'current_price': 152.30, 'change_percent': 2.1, 'volume': 1580000,
                'market_cap': 987456000000, 'pe_ratio': 18.5, 'pb_ratio': 4.2,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
    
    def _get_mock_hk_stocks(self) -> List[Dict]:
        """获取模拟港股数据（作为备用）"""
        return [
            {
                'code': '00700', 'name': '腾讯控股', 'market': 'HK',
                'current_price': 398.60, 'change_percent': -1.2, 'volume': 15678900,
                'market_cap': 0, 'pe_ratio': 0, 'pb_ratio': 0,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'code': '01398', 'name': '工商银行', 'market': 'HK',
                'current_price': 5.96, 'change_percent': 0.34, 'volume': 25467890,
                'market_cap': 0, 'pe_ratio': 0, 'pb_ratio': 0,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

def test_real_time_fetcher():
    """测试实时数据获取功能"""
    fetcher = RealTimeStockFetcher()
    
    print("测试A股数据获取...")
    a_stocks = fetcher.get_all_a_stocks()
    print(f"A股数据: {len(a_stocks)} 只")
    if a_stocks:
        print(f"示例: {a_stocks[0]['name']} ({a_stocks[0]['code']}) - ¥{a_stocks[0]['current_price']}")
    
    print("\n测试港股数据获取...")
    hk_stocks = fetcher.get_all_hk_stocks()
    print(f"港股数据: {len(hk_stocks)} 只")
    if hk_stocks:
        print(f"示例: {hk_stocks[0]['name']} ({hk_stocks[0]['code']}) - HK${hk_stocks[0]['current_price']}")
    
    print("\n测试股票搜索...")
    search_results = fetcher.search_stocks("平安")
    print(f"搜索'平安': {len(search_results)} 个结果")
    
    print("\n测试股票详细信息...")
    detail = fetcher.get_stock_detail("000001", "A")
    if detail:
        print(f"详细信息: {detail['name']} - 当前价格: ¥{detail['current_price']}")

if __name__ == "__main__":
    test_real_time_fetcher()