"""
股票数据获取模块
从免费API获取A股和港股数据
"""

import requests
import json
import time
import re
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StockDataFetcher:
    def __init__(self):
        self.sina_base_url = "https://hq.sinajs.cn/list="
        self.eastmoney_base_url = "https://push2.eastmoney.com/api/qt/clist/get"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_basic_info(self, stock_code):
        """获取单只股票基本信息"""
        try:
            # 处理股票代码格式
            sina_code = self._convert_to_sina_code(stock_code)
            url = f"{self.sina_base_url}{sina_code}"
            
            response = self.session.get(url, timeout=10)
            response.encoding = 'gbk'
            
            if response.status_code == 200:
                return self._parse_sina_data(response.text, stock_code)
            else:
                logger.error(f"获取股票数据失败: {stock_code}, 状态码: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"获取股票数据异常: {stock_code}, {e}")
            return None
    
    def get_stock_list_a(self, page=1, size=100):
        """获取A股股票列表"""
        try:
            params = {
                'pn': page,
                'pz': size,
                'po': '1',
                'np': '1',
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': '2',
                'invt': '2',
                'fid': 'f3',
                'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',  # A股主板、创业板、科创板
                'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            }
            
            response = self.session.get(self.eastmoney_base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_eastmoney_list(data)
            else:
                logger.error(f"获取A股列表失败, 状态码: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取A股列表异常: {e}")
            return []
    
    def get_stock_list_hk(self, page=1, size=100):
        """获取港股股票列表"""
        try:
            params = {
                'pn': page,
                'pz': size,
                'po': '1',
                'np': '1',
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': '2',
                'invt': '2',
                'fid': 'f3',
                'fs': 'm:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2',  # 港股
                'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            }
            
            response = self.session.get(self.eastmoney_base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_eastmoney_list(data)
            else:
                logger.error(f"获取港股列表失败, 状态码: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取港股列表异常: {e}")
            return []
    
    def get_market_index(self):
        """获取主要市场指数"""
        indices = {
            'sh000001': '上证指数',
            'sz399001': '深证成指', 
            'sz399006': '创业板指',
            'hkHSI': '恒生指数'
        }
        
        results = {}
        
        for code, name in indices.items():
            try:
                data = self.get_stock_basic_info(code)
                if data:
                    results[code] = {
                        'name': name,
                        'current_price': data.get('current_price'),
                        'change_percent': data.get('change_percent'),
                        'volume': data.get('volume'),
                        'update_time': data.get('update_time')
                    }
                time.sleep(0.5)  # 避免请求过频
            except Exception as e:
                logger.error(f"获取指数数据失败: {code}, {e}")
        
        return results
    
    def _convert_to_sina_code(self, stock_code):
        """转换为新浪财经的股票代码格式"""
        if stock_code.startswith('6'):
            return f"sh{stock_code}"
        elif stock_code.startswith(('0', '3')):
            return f"sz{stock_code}"
        elif stock_code.startswith('00') and len(stock_code) == 5:
            return f"hk{stock_code}"
        elif stock_code in ['sh000001', 'sz399001', 'sz399006']:
            return stock_code
        elif stock_code == 'hkHSI':
            return 'hkHSI'
        else:
            return stock_code
    
    def _parse_sina_data(self, text, original_code):
        """解析新浪财经数据"""
        try:
            # 提取数据部分
            pattern = r'var hq_str_.*?="(.*?)";'
            match = re.search(pattern, text)
            
            if not match:
                return None
            
            data_str = match.group(1)
            if not data_str:
                return None
            
            fields = data_str.split(',')
            
            if len(fields) < 10:
                return None
            
            # 判断是否为指数
            if original_code in ['sh000001', 'sz399001', 'sz399006', 'hkHSI']:
                return self._parse_index_data(fields, original_code)
            else:
                return self._parse_stock_data(fields, original_code)
                
        except Exception as e:
            logger.error(f"解析新浪数据失败: {original_code}, {e}")
            return None
    
    def _parse_stock_data(self, fields, stock_code):
        """解析股票数据"""
        try:
            current_price = float(fields[3]) if fields[3] else 0
            prev_close = float(fields[2]) if fields[2] else 0
            
            change = current_price - prev_close if current_price and prev_close else 0
            change_percent = (change / prev_close * 100) if prev_close else 0
            
            return {
                'code': stock_code,
                'name': fields[0],
                'current_price': current_price,
                'prev_close': prev_close,
                'open_price': float(fields[1]) if fields[1] else 0,
                'high_price': float(fields[4]) if fields[4] else 0,
                'low_price': float(fields[5]) if fields[5] else 0,
                'change': change,
                'change_percent': change_percent,
                'volume': int(fields[8]) if fields[8] else 0,
                'turnover': float(fields[9]) if fields[9] else 0,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'date': fields[30] if len(fields) > 30 else '',
                'time': fields[31] if len(fields) > 31 else ''
            }
        except Exception as e:
            logger.error(f"解析股票数据失败: {stock_code}, {e}")
            return None
    
    def _parse_index_data(self, fields, index_code):
        """解析指数数据"""
        try:
            current_price = float(fields[1]) if fields[1] else 0
            prev_close = float(fields[2]) if fields[2] else 0
            
            change = current_price - prev_close if current_price and prev_close else 0
            change_percent = (change / prev_close * 100) if prev_close else 0
            
            return {
                'code': index_code,
                'name': fields[0],
                'current_price': current_price,
                'prev_close': prev_close,
                'open_price': float(fields[1]) if fields[1] else 0,
                'high_price': float(fields[4]) if len(fields) > 4 and fields[4] else 0,
                'low_price': float(fields[5]) if len(fields) > 5 and fields[5] else 0,
                'change': change,
                'change_percent': change_percent,
                'volume': int(fields[8]) if len(fields) > 8 and fields[8] else 0,
                'turnover': float(fields[9]) if len(fields) > 9 and fields[9] else 0,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"解析指数数据失败: {index_code}, {e}")
            return None
    
    def _parse_eastmoney_list(self, data):
        """解析东方财富股票列表数据"""
        try:
            if not data or 'data' not in data or not data['data']:
                return []
            
            diff_data = data['data'].get('diff', [])
            stocks = []
            
            for item in diff_data:
                try:
                    stock = {
                        'code': item.get('f12', ''),  # 股票代码
                        'name': item.get('f14', ''),  # 股票名称
                        'current_price': item.get('f2', 0) / 100 if item.get('f2') else 0,  # 当前价
                        'change_percent': item.get('f3', 0) / 100 if item.get('f3') else 0,  # 涨跌幅
                        'change': item.get('f4', 0) / 100 if item.get('f4') else 0,  # 涨跌额
                        'volume': item.get('f5', 0),  # 成交量
                        'turnover': item.get('f6', 0) / 100 if item.get('f6') else 0,  # 成交额
                        'high_price': item.get('f15', 0) / 100 if item.get('f15') else 0,  # 最高价
                        'low_price': item.get('f16', 0) / 100 if item.get('f16') else 0,  # 最低价
                        'open_price': item.get('f17', 0) / 100 if item.get('f17') else 0,  # 开盘价
                        'prev_close': item.get('f18', 0) / 100 if item.get('f18') else 0,  # 昨收价
                        'pe_ratio': item.get('f9', 0) / 100 if item.get('f9') else 0,  # 市盈率
                        'pb_ratio': item.get('f23', 0) / 100 if item.get('f23') else 0,  # 市净率
                        'market_cap': item.get('f20', 0) / 10000 if item.get('f20') else 0,  # 总市值(万元转亿元)
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if stock['code'] and stock['name']:
                        stocks.append(stock)
                        
                except Exception as e:
                    logger.error(f"解析单只股票数据失败: {e}")
                    continue
            
            return stocks
            
        except Exception as e:
            logger.error(f"解析东方财富数据失败: {e}")
            return []
    
    def batch_get_stocks(self, stock_codes, batch_size=20):
        """批量获取股票数据"""
        results = []
        
        for i in range(0, len(stock_codes), batch_size):
            batch = stock_codes[i:i + batch_size]
            logger.info(f"获取第 {i//batch_size + 1} 批股票数据: {len(batch)} 只")
            
            for code in batch:
                data = self.get_stock_basic_info(code)
                if data:
                    results.append(data)
                time.sleep(0.2)  # 避免请求过频
            
            time.sleep(1)  # 批次间延迟
        
        return results
    
    def get_financial_ratios(self, stock_code):
        """获取股票财务指标（模拟数据，实际需要付费API）"""
        # 这里返回模拟的财务数据，实际应用中需要接入付费的财务数据API
        import random
        
        return {
            'code': stock_code,
            'pe_ratio': round(random.uniform(5, 50), 2),
            'pb_ratio': round(random.uniform(0.5, 10), 2),
            'roe': round(random.uniform(0.05, 0.30), 4),
            'debt_ratio': round(random.uniform(0.1, 0.8), 4),
            'revenue_growth': round(random.uniform(-0.2, 0.5), 4),
            'profit_growth': round(random.uniform(-0.3, 1.0), 4),
            'gross_margin': round(random.uniform(0.1, 0.6), 4),
            'net_margin': round(random.uniform(0.02, 0.30), 4),
            'update_time': datetime.now().strftime('%Y-%m-%d')
        }

def main():
    """测试函数"""
    fetcher = StockDataFetcher()
    
    # 测试获取指数数据
    logger.info("获取市场指数...")
    indices = fetcher.get_market_index()
    print("市场指数:", json.dumps(indices, ensure_ascii=False, indent=2))
    
    # 测试获取A股列表
    logger.info("获取A股列表...")
    a_stocks = fetcher.get_stock_list_a(page=1, size=10)
    print(f"A股数据: {len(a_stocks)} 只")
    if a_stocks:
        print("A股示例:", json.dumps(a_stocks[0], ensure_ascii=False, indent=2))
    
    # 测试获取港股列表
    logger.info("获取港股列表...")
    hk_stocks = fetcher.get_stock_list_hk(page=1, size=10)
    print(f"港股数据: {len(hk_stocks)} 只")
    if hk_stocks:
        print("港股示例:", json.dumps(hk_stocks[0], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()