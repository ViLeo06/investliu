#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老刘投资笔记结构化分析器
从OCR结果中提取结构化投资信息，生成文档2
"""

import re
import json
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class InvestmentNote:
    """投资笔记结构化数据"""
    page_number: int
    source_file: str
    raw_text: str
    
    # 投资观点和策略
    investment_views: List[str]
    investment_strategies: List[str]
    
    # 股票标的信息
    mentioned_stocks: List[str]
    stock_codes: List[str]
    
    # 市场判断
    market_analysis: List[str]
    timing_advice: List[str]
    
    # 财务和估值相关
    financial_metrics: List[str]
    valuation_methods: List[str]
    
    # 投资金句和名言
    key_quotes: List[str]
    
    # 技术分析要素
    technical_analysis: List[str]
    
    # 风险提示
    risk_warnings: List[str]

class InvestmentAnalyzer:
    """投资笔记分析器"""
    
    def __init__(self):
        # 定义关键词模式
        self.patterns = {
            # 投资策略关键词
            'strategies': [
                r'跟着游资', r'跟着热点', r'跟着龙头', r'人弃我取', r'人取我弃',
                r'价值投资', r'成长投资', r'逆向投资', r'趋势投资', r'分散投资',
                r'长期持有', r'分批买入', r'定投', r'波段操作'
            ],
            
            # 股票和公司名称
            'stocks': [
                r'A股', r'港股', r'美股', r'[A-Z]{2,4}', r'\d{6}',
                r'京东', r'阿里', r'腾讯', r'茅台', r'比亚迪', r'宁德时代',
                r'房地产', r'游戏', r'数据', r'科技', r'制造业'
            ],
            
            # 财务指标
            'financial': [
                r'PE', r'PB', r'ROE', r'ROA', r'净利润', r'营收', r'负债率',
                r'毛利率', r'市盈率', r'市净率', r'股息率', r'市值', r'估值'
            ],
            
            # 市场判断
            'market': [
                r'牛市', r'熊市', r'震荡', r'调整', r'反弹', r'上涨', r'下跌',
                r'底部', r'顶部', r'突破', r'支撑', r'阻力', r'趋势'
            ],
            
            # 技术分析
            'technical': [
                r'量价关系', r'放量', r'缩量', r'涨停', r'跌停',
                r'支撑位', r'阻力位', r'均线', r'K线', r'MACD', r'KDJ'
            ],
            
            # 风险提示
            'risks': [
                r'风险', r'亏损', r'套牢', r'爆仓', r'杠杆', r'债务',
                r'泡沫', r'崩盘', r'暴跌', r'黑天鹅'
            ]
        }
        
        # 投资名言模式
        self.quote_patterns = [
            r'"[^"]*"',  # 双引号包围的内容
            r'"[^"]*"',  # 中文双引号包围的内容
            r'.*——.*',    # 含有"——"的名言
            r'.*巴菲特.*', r'.*格雷厄姆.*', r'.*芒格.*'  # 投资大师相关
        ]

    def extract_key_quotes(self, text: str) -> List[str]:
        """提取投资金句和名言"""
        quotes = []
        
        for pattern in self.quote_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            quotes.extend(matches)
        
        # 清理和去重
        cleaned_quotes = []
        for quote in quotes:
            quote = quote.strip()
            if len(quote) > 5 and quote not in cleaned_quotes:
                cleaned_quotes.append(quote)
        
        return cleaned_quotes

    def extract_by_keywords(self, text: str, keyword_type: str) -> List[str]:
        """基于关键词提取相关内容"""
        if keyword_type not in self.patterns:
            return []
        
        results = []
        patterns = self.patterns[keyword_type]
        
        for pattern in patterns:
            matches = re.findall(f'[^。！？]*{pattern}[^。！？]*', text, re.IGNORECASE)
            results.extend(matches)
        
        # 清理和去重
        cleaned_results = []
        for result in results:
            result = result.strip('，。！？ \n\t')
            if len(result) > 3 and result not in cleaned_results:
                cleaned_results.append(result)
        
        return cleaned_results

    def analyze_page(self, page_num: int, filename: str, text: str) -> InvestmentNote:
        """分析单页内容"""
        
        note = InvestmentNote(
            page_number=page_num,
            source_file=filename,
            raw_text=text,
            investment_views=[],
            investment_strategies=[],
            mentioned_stocks=[],
            stock_codes=[],
            market_analysis=[],
            timing_advice=[],
            financial_metrics=[],
            valuation_methods=[],
            key_quotes=[],
            technical_analysis=[],
            risk_warnings=[]
        )
        
        # 提取各类信息
        note.key_quotes = self.extract_key_quotes(text)
        note.investment_strategies = self.extract_by_keywords(text, 'strategies')
        note.mentioned_stocks = self.extract_by_keywords(text, 'stocks')
        note.financial_metrics = self.extract_by_keywords(text, 'financial')
        note.market_analysis = self.extract_by_keywords(text, 'market')
        note.technical_analysis = self.extract_by_keywords(text, 'technical')
        note.risk_warnings = self.extract_by_keywords(text, 'risks')
        
        # 提取投资观点（包含"投资"、"买"、"卖"等关键词的句子）
        investment_patterns = [r'[^。！？]*投资[^。！？]*', r'[^。！？]*买入[^。！？]*', 
                             r'[^。！？]*卖出[^。！？]*', r'[^。！？]*持有[^。！？]*']
        for pattern in investment_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            note.investment_views.extend([m.strip() for m in matches if len(m.strip()) > 5])
        
        # 提取择时建议（包含"时机"、"时候"等关键词的句子）
        timing_patterns = [r'[^。！？]*时机[^。！？]*', r'[^。！？]*时候[^。！？]*', 
                          r'[^。！？]*机会[^。！？]*']
        for pattern in timing_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            note.timing_advice.extend([m.strip() for m in matches if len(m.strip()) > 5])
        
        return note

    def analyze_full_document(self, ocr_file: str) -> List[InvestmentNote]:
        """分析完整OCR文档"""
        
        print(f"开始分析OCR文档: {ocr_file}")
        
        with open(ocr_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按页面分割
        pages = re.split(r'## 第(\d+)页 - ([^\n]+)', content)
        
        notes = []
        
        # 处理每一页（跳过头部信息）
        for i in range(1, len(pages), 3):  # 每3个元素组成一页：页码、文件名、内容
            if i+2 < len(pages):
                page_num = int(pages[i])
                filename = pages[i+1].strip()
                text = pages[i+2].strip()
                
                if text and not text.startswith('--'):
                    note = self.analyze_page(page_num, filename, text)
                    notes.append(note)
                    print(f"✓ 分析完成第{page_num}页: {filename}")
        
        return notes

    def generate_structured_document(self, notes: List[InvestmentNote], output_file: str):
        """生成结构化文档"""
        
        print(f"生成结构化文档: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # 文档头部
            f.write("# 老刘投资笔记 - 文档2：结构化投资信息提取\n")
            f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# 说明：本文档为老刘投资笔记的结构化分析结果\n\n")
            f.write("=" * 80 + "\n\n")
            
            # 汇总统计
            f.write("## 📊 内容统计汇总\n\n")
            
            all_quotes = []
            all_strategies = []
            all_stocks = []
            all_financial = []
            all_technical = []
            all_risks = []
            
            for note in notes:
                all_quotes.extend(note.key_quotes)
                all_strategies.extend(note.investment_strategies)
                all_stocks.extend(note.mentioned_stocks)
                all_financial.extend(note.financial_metrics)
                all_technical.extend(note.technical_analysis)
                all_risks.extend(note.risk_warnings)
            
            f.write(f"- **总页数**: {len(notes)}\n")
            f.write(f"- **投资金句**: {len(set(all_quotes))}\n")
            f.write(f"- **投资策略**: {len(set(all_strategies))}\n") 
            f.write(f"- **提及股票**: {len(set(all_stocks))}\n")
            f.write(f"- **财务指标**: {len(set(all_financial))}\n")
            f.write(f"- **技术分析**: {len(set(all_technical))}\n")
            f.write(f"- **风险提示**: {len(set(all_risks))}\n\n")
            
            # 核心投资金句汇总
            f.write("## 💎 核心投资金句汇总\n\n")
            unique_quotes = list(set(all_quotes))
            for i, quote in enumerate(unique_quotes, 1):
                f.write(f"{i}. {quote}\n")
            f.write("\n" + "-" * 80 + "\n\n")
            
            # 投资策略汇总
            f.write("## 📈 投资策略汇总\n\n")
            unique_strategies = list(set(all_strategies))
            for i, strategy in enumerate(unique_strategies, 1):
                f.write(f"{i}. {strategy}\n")
            f.write("\n" + "-" * 80 + "\n\n")
            
            # 按页详细分析
            f.write("## 📄 分页详细分析\n\n")
            
            for note in notes:
                f.write(f"### 第{note.page_number}页 - {note.source_file}\n\n")
                
                if note.key_quotes:
                    f.write("**🎯 投资金句**\n")
                    for quote in note.key_quotes:
                        f.write(f"- {quote}\n")
                    f.write("\n")
                
                if note.investment_views:
                    f.write("**💭 投资观点**\n")
                    for view in note.investment_views:
                        f.write(f"- {view}\n")
                    f.write("\n")
                
                if note.investment_strategies:
                    f.write("**📊 投资策略**\n")
                    for strategy in note.investment_strategies:
                        f.write(f"- {strategy}\n")
                    f.write("\n")
                
                if note.mentioned_stocks:
                    f.write("**🏢 相关股票**\n")
                    for stock in note.mentioned_stocks:
                        f.write(f"- {stock}\n")
                    f.write("\n")
                
                if note.financial_metrics:
                    f.write("**💰 财务指标**\n")
                    for metric in note.financial_metrics:
                        f.write(f"- {metric}\n")
                    f.write("\n")
                
                if note.technical_analysis:
                    f.write("**📉 技术分析**\n")
                    for tech in note.technical_analysis:
                        f.write(f"- {tech}\n")
                    f.write("\n")
                
                if note.market_analysis:
                    f.write("**🌍 市场判断**\n")
                    for market in note.market_analysis:
                        f.write(f"- {market}\n")
                    f.write("\n")
                
                if note.timing_advice:
                    f.write("**⏰ 择时建议**\n")
                    for timing in note.timing_advice:
                        f.write(f"- {timing}\n")
                    f.write("\n")
                
                if note.risk_warnings:
                    f.write("**⚠️ 风险提示**\n")
                    for risk in note.risk_warnings:
                        f.write(f"- {risk}\n")
                    f.write("\n")
                
                f.write("-" * 80 + "\n\n")
        
        print(f"✓ 结构化文档生成完成: {output_file}")

def main():
    """主函数"""
    
    # 输入输出文件路径
    OCR_FILE = "/mnt/c/Users/M2814/.cursor/investliu/老刘投资笔记_文档1_原始OCR提取.txt"
    OUTPUT_FILE = "/mnt/c/Users/M2814/.cursor/investliu/老刘投资笔记_文档2_结构化信息.txt"
    
    analyzer = InvestmentAnalyzer()
    
    try:
        # 分析OCR文档
        notes = analyzer.analyze_full_document(OCR_FILE)
        
        # 生成结构化文档
        analyzer.generate_structured_document(notes, OUTPUT_FILE)
        
        print(f"\n📋 处理完成!")
        print(f"   - 分析页数: {len(notes)}")
        print(f"   - 输出文档: {OUTPUT_FILE}")
        
    except FileNotFoundError as e:
        print(f"❌ 文件不存在: {e}")
        print("请先运行OCR处理和文件合并")
    except Exception as e:
        print(f"❌ 处理出错: {e}")

if __name__ == "__main__":
    main()