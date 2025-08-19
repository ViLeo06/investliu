"""
投资规则提取器
从OCR识别的文本中提取投资决策规则
"""

import re
import json
import jieba
import pandas as pd
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class InvestmentRuleExtractor:
    def __init__(self):
        self.stock_keywords = [
            '买入', '卖出', '持有', '观望', '减仓', '加仓', '止损',
            'PE', 'PB', 'ROE', 'ROA', '市盈率', '市净率', '净资产收益率',
            '营收', '利润', '现金流', '负债率', '毛利率', '净利率',
            '估值', '价值', '成长', '分红', '股息', '业绩', '财报'
        ]
        
        self.timing_keywords = [
            '大盘', '趋势', '牛市', '熊市', '震荡', '突破', '支撑', '压力',
            '均线', 'MACD', 'KDJ', 'RSI', '成交量', '换手率',
            '政策', '降准', '降息', '加息', '印花税'
        ]
        
        self.position_keywords = [
            '仓位', '满仓', '空仓', '半仓', '轻仓', '重仓', '分散', '集中',
            '风险', '止损', '止盈', '回撤', '波动'
        ]
    
    def extract_rules_from_text(self, text):
        """从文本中提取投资规则"""
        rules = {
            'selection_rules': [],    # 选股规则
            'timing_rules': [],       # 择时规则
            'position_rules': [],     # 仓位规则
            'risk_rules': [],         # 风险控制规则
            'insights': []            # 投资感悟
        }
        
        # 按段落处理
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # 提取选股规则
            if self._contains_keywords(paragraph, self.stock_keywords):
                rule = self._extract_selection_rule(paragraph)
                if rule:
                    rules['selection_rules'].append(rule)
            
            # 提取择时规则
            if self._contains_keywords(paragraph, self.timing_keywords):
                rule = self._extract_timing_rule(paragraph)
                if rule:
                    rules['timing_rules'].append(rule)
            
            # 提取仓位规则
            if self._contains_keywords(paragraph, self.position_keywords):
                rule = self._extract_position_rule(paragraph)
                if rule:
                    rules['position_rules'].append(rule)
            
            # 提取投资感悟
            if self._is_insight(paragraph):
                rules['insights'].append({
                    'content': paragraph,
                    'type': 'experience',
                    'confidence': 0.7
                })
        
        return rules
    
    def _contains_keywords(self, text, keywords):
        """检查文本是否包含关键词"""
        return any(keyword in text for keyword in keywords)
    
    def _extract_selection_rule(self, text):
        """提取选股规则"""
        rule = {
            'type': 'selection',
            'content': text,
            'conditions': [],
            'action': '',
            'confidence': 0.5
        }
        
        # 提取数值条件
        pe_match = re.search(r'PE[<>≤≥]?(\d+)', text)
        if pe_match:
            rule['conditions'].append({
                'indicator': 'PE',
                'operator': self._extract_operator(text, 'PE'),
                'value': float(pe_match.group(1))
            })
            rule['confidence'] += 0.2
        
        pb_match = re.search(r'PB[<>≤≥]?(\d+\.?\d*)', text)
        if pb_match:
            rule['conditions'].append({
                'indicator': 'PB',
                'operator': self._extract_operator(text, 'PB'),
                'value': float(pb_match.group(1))
            })
            rule['confidence'] += 0.2
        
        roe_match = re.search(r'ROE[>≥]?(\d+\.?\d*)%?', text)
        if roe_match:
            rule['conditions'].append({
                'indicator': 'ROE',
                'operator': self._extract_operator(text, 'ROE'),
                'value': float(roe_match.group(1)) / 100 if '%' in text else float(roe_match.group(1))
            })
            rule['confidence'] += 0.2
        
        # 提取行动
        if '买入' in text:
            rule['action'] = 'buy'
        elif '卖出' in text:
            rule['action'] = 'sell'
        elif '观望' in text:
            rule['action'] = 'hold'
        
        return rule if rule['conditions'] or rule['action'] else None
    
    def _extract_timing_rule(self, text):
        """提取择时规则"""
        rule = {
            'type': 'timing',
            'content': text,
            'signal': '',
            'action': '',
            'confidence': 0.5
        }
        
        # 识别技术指标信号
        if 'MACD' in text:
            if '金叉' in text or '向上' in text:
                rule['signal'] = 'macd_bullish'
                rule['action'] = 'buy'
            elif '死叉' in text or '向下' in text:
                rule['signal'] = 'macd_bearish'
                rule['action'] = 'sell'
            rule['confidence'] += 0.2
        
        if '突破' in text:
            rule['signal'] = 'breakout'
            rule['action'] = 'buy'
            rule['confidence'] += 0.2
        
        if '跌破' in text:
            rule['signal'] = 'breakdown'
            rule['action'] = 'sell'
            rule['confidence'] += 0.2
        
        # 识别市场情绪
        if '恐慌' in text:
            rule['signal'] = 'panic'
            rule['action'] = 'buy'  # 恐慌时买入
        elif '贪婪' in text:
            rule['signal'] = 'greed'
            rule['action'] = 'sell'  # 贪婪时卖出
        
        return rule if rule['signal'] else None
    
    def _extract_position_rule(self, text):
        """提取仓位规则"""
        rule = {
            'type': 'position',
            'content': text,
            'condition': '',
            'position': 0,
            'confidence': 0.5
        }
        
        # 提取仓位比例
        position_match = re.search(r'(\d+)成仓', text)
        if position_match:
            rule['position'] = float(position_match.group(1)) / 10
            rule['confidence'] += 0.3
        
        half_position_words = ['半仓', '5成', '50%']
        if any(word in text for word in half_position_words):
            rule['position'] = 0.5
            rule['confidence'] += 0.2
        
        # 提取条件
        if '牛市' in text:
            rule['condition'] = 'bull_market'
        elif '熊市' in text:
            rule['condition'] = 'bear_market'
        elif '震荡' in text:
            rule['condition'] = 'sideways_market'
        
        return rule if rule['position'] > 0 else None
    
    def _extract_operator(self, text, indicator):
        """提取操作符"""
        indicator_pos = text.find(indicator)
        if indicator_pos == -1:
            return '='
        
        # 查看指标后面的字符
        after_indicator = text[indicator_pos + len(indicator):indicator_pos + len(indicator) + 5]
        
        if '<' in after_indicator or '小于' in after_indicator:
            return '<'
        elif '>' in after_indicator or '大于' in after_indicator:
            return '>'
        elif '≤' in after_indicator or '不超过' in after_indicator:
            return '<='
        elif '≥' in after_indicator or '不少于' in after_indicator:
            return '>='
        else:
            return '='
    
    def _is_insight(self, text):
        """判断是否为投资感悟"""
        insight_keywords = [
            '经验', '教训', '感悟', '心得', '体会', '反思',
            '重要', '关键', '核心', '本质', '原则'
        ]
        return any(keyword in text for keyword in insight_keywords)
    
    def process_notes_folder(self, notes_folder):
        """处理笔记文件夹，提取所有规则"""
        import os
        
        all_rules = {
            'selection_rules': [],
            'timing_rules': [],
            'position_rules': [],
            'risk_rules': [],
            'insights': []
        }
        
        # 读取汇总文件
        summary_file = os.path.join(notes_folder, 'summary.txt')
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            rules = self.extract_rules_from_text(text)
            
            # 合并规则
            for category in all_rules:
                all_rules[category].extend(rules.get(category, []))
        
        # 去重和排序
        all_rules = self._deduplicate_rules(all_rules)
        
        # 保存提取的规则
        output_file = os.path.join(notes_folder, 'extracted_rules.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_rules, f, ensure_ascii=False, indent=2)
        
        logger.info(f"规则提取完成，保存到: {output_file}")
        return all_rules
    
    def _deduplicate_rules(self, rules):
        """去重和排序规则"""
        for category in rules:
            # 按置信度降序排序
            rules[category] = sorted(rules[category], 
                                   key=lambda x: x.get('confidence', 0), 
                                   reverse=True)
            
            # 简单去重（基于内容相似度）
            unique_rules = []
            for rule in rules[category]:
                is_duplicate = False
                for existing_rule in unique_rules:
                    if self._is_similar_rule(rule, existing_rule):
                        is_duplicate = True
                        break
                if not is_duplicate:
                    unique_rules.append(rule)
            
            rules[category] = unique_rules
        
        return rules
    
    def _is_similar_rule(self, rule1, rule2):
        """判断两个规则是否相似"""
        content1 = rule1.get('content', '')
        content2 = rule2.get('content', '')
        
        # 简单的相似度判断
        if len(content1) == 0 or len(content2) == 0:
            return False
        
        common_chars = set(content1) & set(content2)
        similarity = len(common_chars) / max(len(set(content1)), len(set(content2)))
        
        return similarity > 0.7

def main():
    """主函数"""
    extractor = InvestmentRuleExtractor()
    
    # 处理笔记文件夹
    notes_folder = "notes/processed"
    
    if not os.path.exists(notes_folder):
        logger.error(f"笔记文件夹不存在: {notes_folder}")
        logger.info("请先运行OCR处理脚本")
        return
    
    # 提取规则
    rules = extractor.process_notes_folder(notes_folder)
    
    # 输出统计信息
    for category, rule_list in rules.items():
        logger.info(f"{category}: {len(rule_list)} 条规则")

if __name__ == "__main__":
    import os
    main()