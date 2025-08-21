#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据获取器 - 从免费API获取股票数据
"""

import requests
import json
import random
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class StockDataFetcher:
    def __init__(self):
        """初始化数据获取器"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # A股股票池 - 老刘偏好的优质股票
        self.a_stock_pool = [
            ('000001', '平安银行'), ('600036', '招商银行'), ('600000', '浦发银行'),
            ('000002', '万科A'), ('600519', '贵州茅台'), ('000858', '五粮液'),
            ('600276', '恒瑞医药'), ('000661', '长春高新'), ('300015', '爱尔眼科'),
            ('000858', '五粮液'), ('002415', '海康威视'), ('300059', '东方财富'),
            ('600887', '伊利股份'), ('000895', '双汇发展'), ('600690', '海尔智家'),
            ('002304', '洋河股份'), ('600809', '山西汾酒')
        ]
        
        # 港股股票池
        self.hk_stock_pool = [
            ('00700', '腾讯控股'), ('00941', '中国移动'), ('01299', '友邦保险'),
            ('00175', '吉利汽车'), ('01093', '石药集团'), ('03690', '美团'),
            ('00883', '中国海洋石油'), ('02318', '中国平安'), ('01398', '工商银行'),
            ('03988', '中国银行')
        ]
        
        print(f"股票数据获取器初始化完成")
    
    def fetch_a_stocks(self) -> List[Dict]:
        """获取A股数据"""
        print("正在获取A股数据...")
        stocks = []
        
        for code, name in self.a_stock_pool:
            try:
                # 模拟从新浪财经API获取数据
                stock_data = self._fetch_stock_basic_info(code, name, 'A')
                if stock_data:
                    stocks.append(stock_data)
                    print(f"✅ 已获取: {name}({code})")
                
                # 避免请求过快
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ 获取{name}({code})数据失败: {str(e)}")
                continue
        
        print(f"A股数据获取完成，共{len(stocks)}只")
        return stocks
    
    def fetch_hk_stocks(self) -> List[Dict]:
        """获取港股数据"""
        print("正在获取港股数据...")
        stocks = []
        
        for code, name in self.hk_stock_pool:
            try:
                stock_data = self._fetch_stock_basic_info(code, name, 'HK')
                if stock_data:
                    stocks.append(stock_data)
                    print(f"✅ 已获取: {name}({code})")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ 获取{name}({code})数据失败: {str(e)}")
                continue
        
        print(f"港股数据获取完成，共{len(stocks)}只")
        return stocks
    
    def fetch_market_data(self) -> Dict:
        """获取大盘数据"""
        print("正在获取市场数据...")
        
        # 模拟市场数据
        market_data = {
            'shanghai_index': {
                'value': random.uniform(2950, 3100),
                'change': random.uniform(-1.5, 1.5),
                'volume': random.randint(200000000000, 400000000000)
            },
            'szse_index': {
                'value': random.uniform(9500, 10500),
                'change': random.uniform(-1.5, 1.5),
                'volume': random.randint(250000000000, 450000000000)
            },
            'hsi_index': {
                'value': random.uniform(16000, 18000),
                'change': random.uniform(-1.5, 1.5),
                'volume': random.randint(80000000000, 150000000000)
            }
        }
        
        print("✅ 市场数据获取完成")
        return market_data
    
    def _fetch_stock_basic_info(self, code: str, name: str, market_type: str) -> Optional[Dict]:
        """获取股票基本信息（模拟数据）"""
        try:
            # 模拟真实股票数据
            base_price = random.uniform(8, 200) if market_type == 'A' else random.uniform(5, 500)
            
            stock_info = {
                'code': code,
                'name': name,
                'market_type': market_type,
                'current_price': round(base_price, 2),
                'change_percent': round(random.uniform(-3, 3), 2),
                'volume': random.randint(1000000, 100000000),
                'market_cap': int(base_price * random.randint(100000000, 10000000000)),
                'pe_ratio': round(random.uniform(5, 35), 1),
                'pb_ratio': round(random.uniform(0.5, 8), 2),
                'ps_ratio': round(random.uniform(0.8, 15), 1),
                'roe': round(random.uniform(3, 30), 1),
                'roa': round(random.uniform(1, 20), 1),
                'debt_ratio': round(random.uniform(0.1, 0.9), 2),
                'dividend_yield': round(random.uniform(0.5, 6), 1),
                'industry': self._get_industry_by_name(name),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return stock_info
            
        except Exception as e:
            print(f"获取{name}基本信息失败: {str(e)}")
            return None
    
    def _get_industry_by_name(self, name: str) -> str:
        """根据股票名称推断行业"""
        industry_map = {
            '银行': ['平安银行', '招商银行', '浦发银行', '工商银行', '中国银行'],
            '房地产': ['万科A'],
            '食品饮料': ['贵州茅台', '五粮液', '洋河股份', '山西汾酒', '伊利股份', '双汇发展'],
            '医药': ['恒瑞医药', '长春高新', '爱尔眼科', '石药集团'],
            '科技': ['海康威视', '东方财富'],
            '家电': ['海尔智家'],
            '互联网科技': ['腾讯控股', '美团'],
            '电信运营': ['中国移动'],
            '保险': ['友邦保险', '中国平安'],
            '汽车': ['吉利汽车'],
            '能源': ['中国海洋石油']
        }
        
        for industry, stocks in industry_map.items():
            if any(stock in name for stock in stocks):
                return industry
        
        return '其他'

    def _simulate_api_delay(self):
        """模拟API请求延迟"""
        time.sleep(random.uniform(0.05, 0.2))