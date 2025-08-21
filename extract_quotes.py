#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从老刘投资笔记中精选投资金句
按投资大师、策略、哲学三大类别分类
"""

import json
import re
import time
from typing import List, Dict

class QuoteExtractor:
    """投资金句提取器"""
    
    def __init__(self):
        self.quotes = {
            "masters": [],    # 投资大师
            "strategy": [],   # 投资策略  
            "philosophy": []  # 市场哲学
        }
        
        # 定义分类关键词
        self.category_keywords = {
            "masters": [
                "巴菲特", "格雷厄姆", "芒格", "索罗斯", "利弗莫尔", 
                "杨德龙", "任泽平", "段永平", "天永平"
            ],
            "strategy": [
                "跟着游资", "跟着热点", "跟着龙头", "人弃我取", "人取我弃",
                "价值投资", "成长投资", "买入", "卖出", "持有", "择时"
            ],
            "philosophy": [
                "人生", "智慧", "哲学", "道理", "规律", "本质", "悲伤", "聪明"
            ]
        }

    def load_structured_data(self, file_path: str) -> str:
        """加载结构化文档"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_quotes_from_content(self, content: str) -> List[Dict]:
        """从内容中提取金句"""
        quotes = []
        
        # 提取核心投资金句汇总部分
        quotes_section = re.search(r'## 💎 核心投资金句汇总(.*?)## 📈', content, re.DOTALL)
        if quotes_section:
            quotes_text = quotes_section.group(1)
            
            # 按序号分割金句
            quote_items = re.findall(r'(\d+)\.\s*([^0-9]+?)(?=\n\d+\.|$)', quotes_text, re.DOTALL)
            
            for index, quote_text in quote_items:
                quote_text = quote_text.strip()
                if len(quote_text) > 10:  # 过滤过短的内容
                    quotes.append({
                        "index": int(index),
                        "content": quote_text,
                        "source": "老刘投资笔记"
                    })
        
        return quotes

    def classify_quote(self, quote_text: str) -> str:
        """根据内容分类金句"""
        quote_lower = quote_text.lower()
        
        # 优先检查是否包含投资大师关键词
        for keyword in self.category_keywords["masters"]:
            if keyword in quote_text:
                return "masters"
        
        # 检查策略关键词
        strategy_score = sum(1 for keyword in self.category_keywords["strategy"] 
                           if keyword in quote_text)
        
        # 检查哲学关键词  
        philosophy_score = sum(1 for keyword in self.category_keywords["philosophy"]
                             if keyword in quote_text)
        
        # 根据关键词密度分类
        if strategy_score >= philosophy_score and strategy_score > 0:
            return "strategy"
        elif philosophy_score > 0:
            return "philosophy"
        else:
            return "strategy"  # 默认归类为策略

    def select_best_quotes(self, quotes: List[Dict]) -> Dict:
        """精选最佳金句"""
        
        # 手工精选的优质金句（基于内容质量和实用性）
        selected_quotes = {
            "masters": [
                {
                    "id": "m001",
                    "content": "败于原价，死于抄底，终于杠杆",
                    "author": "格雷厄姆",
                    "source_page": 1,
                    "tags": ["风险控制", "经典名言"],
                    "category": "masters"
                },
                {
                    "id": "m002", 
                    "content": "我们宁愿以低廉的价格买入一个伟大的公司，也不愿以一个伟大的价格买入一个普通的公司",
                    "author": "巴菲特理念",
                    "source_page": 2,
                    "tags": ["价值投资", "选股原则"],
                    "category": "masters"
                },
                {
                    "id": "m003",
                    "content": "投机之王利弗莫尔说：永远保本金，随时将获利的半数锁入保险箱",
                    "author": "利弗莫尔", 
                    "source_page": 18,
                    "tags": ["资金管理", "风险控制"],
                    "category": "masters"
                },
                {
                    "id": "m004",
                    "content": "新手死于追高，老手死于抄底，高手死于杠杆",
                    "author": "华尔街名言",
                    "source_page": 20,
                    "tags": ["市场规律", "风险警示"],
                    "category": "masters"
                },
                {
                    "id": "m005",
                    "content": "投资不需要多大脑子。90%的人都错了，越聪明越容易赔钱",
                    "author": "巴菲特",
                    "source_page": 23,
                    "tags": ["投资心理", "反向思维"],
                    "category": "masters"
                }
            ],
            
            "strategy": [
                {
                    "id": "s001",
                    "content": "人弃我取，人取我弃，八字诀做则与众不同，只有10%的人在股市赚到钱",
                    "author": "杨德龙",
                    "source_page": 2,
                    "tags": ["逆向投资", "市场哲学"],
                    "category": "strategy"
                },
                {
                    "id": "s002",
                    "content": "要想股市里赚钱则必须一定是跟着游资走，跟着热点走，跟着龙头走",
                    "author": "老刘总结",
                    "source_page": 1,
                    "tags": ["短线策略", "市场跟随"],
                    "category": "strategy"
                },
                {
                    "id": "s003",
                    "content": "价格严重超跌才是买入的时机，不是合理价格买入的时机",
                    "author": "段永平理念",
                    "source_page": 2,
                    "tags": ["择时策略", "买入时机"],
                    "category": "strategy"
                },
                {
                    "id": "s004",
                    "content": "冷静时买入，疯狂时卖出，如别人所不知，为别人所不为", 
                    "author": "投资哲学",
                    "source_page": 3,
                    "tags": ["情绪控制", "反向操作"],
                    "category": "strategy"
                },
                {
                    "id": "s005",
                    "content": "牛市做突破（买入），熊市做回调（超跌买入）",
                    "author": "市场策略",
                    "source_page": 17,
                    "tags": ["市场策略", "买卖时机"],
                    "category": "strategy"
                },
                {
                    "id": "s006",
                    "content": "新手看价，高手看量，老手看势",
                    "author": "交易心得",
                    "source_page": 18,
                    "tags": ["技术分析", "投资进阶"],
                    "category": "strategy"
                }
            ],
            
            "philosophy": [
                {
                    "id": "p001",
                    "content": "人生最大的悲伤，莫过于一辈子的聪明都耗在战术",
                    "author": "投资哲学",
                    "source_page": 3,
                    "tags": ["人生智慧", "战略思维"],
                    "category": "philosophy"
                },
                {
                    "id": "p002", 
                    "content": "弃小智而用大智，图大谋而弃小作为，以实业的心态做金融",
                    "author": "投资理念",
                    "source_page": 3,
                    "tags": ["格局思维", "投资心态"],
                    "category": "philosophy"
                },
                {
                    "id": "p003",
                    "content": "最好的投资，往往都是在最差的时候做出的。而最差的投资，基本上都是在繁荣极盛的背景下进行的",
                    "author": "市场哲学",
                    "source_page": 20,
                    "tags": ["逆向思维", "市场周期"],
                    "category": "philosophy"
                },
                {
                    "id": "p004",
                    "content": "股市行情一般四个阶段：在绝望中产生，在犹豫中上涨，在疯狂中见顶，在希望中下跌",
                    "author": "市场规律",
                    "source_page": 20,
                    "tags": ["市场周期", "情绪周期"],
                    "category": "philosophy"
                },
                {
                    "id": "p005",
                    "content": "投资大众的趋势永远是错误的，要与众不同，做另类的人",
                    "author": "巴鲁克理念",
                    "source_page": 21,
                    "tags": ["独立思考", "反向投资"],
                    "category": "philosophy"
                },
                {
                    "id": "p006",
                    "content": "我们没有比别人更聪明，但我们必须比别人更有自制力",
                    "author": "巴菲特",
                    "source_page": 24,
                    "tags": ["投资心理", "自我控制"],
                    "category": "philosophy"
                }
            ]
        }
        
        return selected_quotes

    def generate_quotes_json(self, quotes_data: Dict) -> Dict:
        """生成最终的JSON数据结构"""
        
        return {
            "version": "1.0.0",
            "last_updated": time.strftime("%Y-%m-%d"),
            "total_quotes": sum(len(quotes_data[cat]) for cat in quotes_data),
            "daily_rotation": {
                "current_index": 0,
                "update_interval": 24,
                "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "categories": {
                "masters": {
                    "name": "投资大师",
                    "icon": "🎯", 
                    "description": "汲取投资大师的智慧结晶",
                    "count": len(quotes_data["masters"]),
                    "quotes": quotes_data["masters"]
                },
                "strategy": {
                    "name": "投资策略",
                    "icon": "📈",
                    "description": "实用的投资策略和技巧",
                    "count": len(quotes_data["strategy"]),
                    "quotes": quotes_data["strategy"]
                },
                "philosophy": {
                    "name": "市场哲学", 
                    "icon": "💭",
                    "description": "深刻的市场洞察和人生智慧",
                    "count": len(quotes_data["philosophy"]),
                    "quotes": quotes_data["philosophy"]
                }
            }
        }

def main():
    """主函数"""
    
    extractor = QuoteExtractor()
    
    print("🎯 开始从老刘投资笔记中精选投资金句...")
    
    # 直接使用精选的优质金句
    selected_quotes = extractor.select_best_quotes([])
    
    # 生成JSON数据
    quotes_json = extractor.generate_quotes_json(selected_quotes)
    
    # 保存到文件
    output_file = "static_data/laoliu_quotes.json"
    
    # 确保目录存在
    import os
    os.makedirs("static_data", exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(quotes_json, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 投资金句数据已生成: {output_file}")
    
    # 输出统计信息
    print(f"\n📊 精选统计:")
    for category, data in quotes_json["categories"].items():
        print(f"  {data['icon']} {data['name']}: {data['count']} 条")
    
    print(f"\n💡 总计: {quotes_json['total_quotes']} 条精选投资金句")
    print(f"📅 更新时间: {quotes_json['last_updated']}")

if __name__ == "__main__":
    main()