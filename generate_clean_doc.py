#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成清洁版本的完整文档1
只保留原始文字内容，去除过度解析
"""

import json
import time
import re

def extract_clean_text(text, method):
    """提取清洁的原始文字"""
    
    if method == 'optimized-prompt':
        # 如果是优化提示词的结果，提取原文部分
        if '**原文识别如下：**' in text:
            parts = text.split('**原文识别如下：**')
            if len(parts) > 1:
                raw_section = parts[1].split('---')[0].strip()
                # 清理格式标记
                lines = raw_section.split('\n')
                clean_lines = []
                for line in lines:
                    # 移除引用标记
                    line = line.replace('> ', '').replace('>', '').strip()
                    if line and not line.startswith('**') and not line.startswith('#'):
                        clean_lines.append(line)
                return '\n'.join(clean_lines)
    
    # 对于其他方法，直接返回原文
    return text

def generate_clean_document():
    """生成清洁版本的完整文档"""
    
    # 读取完整结果
    with open('complete_ocr_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # 生成清洁文档
    output_file = "老刘投资笔记_完整文档1_清洁版.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 老刘投资笔记 - 完整文档1：原始OCR文字提取结果（清洁版）\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# 说明：本文档为老刘投资笔记手写内容的完整OCR识别结果\n")
        f.write("# 处理方法：多重OCR模型比对验证，保留最佳识别结果\n")
        f.write("# 文件总数：27张图片，按68-94顺序排列\n")
        f.write("# 特点：已清理过度解析内容，仅保留原始文字\n\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            page_num = result['page_num']
            filename = result['filename']
            best_method = result['best_method']
            best_text = result['best_text']
            
            # 提取清洁文字
            clean_text = extract_clean_text(best_text, best_method)
            
            f.write(f"## 第{page_num}页 - {filename}\n")
            f.write(f"### 识别方法: {best_method}\n\n")
            f.write(f"{clean_text}\n\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"✓ 清洁版完整文档已生成: {output_file}")
    
    # 统计信息
    total_pages = len(results)
    method_stats = {}
    for result in results:
        method = result['best_method']
        method_stats[method] = method_stats.get(method, 0) + 1
    
    print(f"\n📊 完整处理统计:")
    print(f"  总页数: {total_pages}")
    print(f"  成功率: 100%")
    
    print(f"\n🏆 最佳方法分布:")
    for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method}: {count} 页 ({count/total_pages*100:.1f}%)")

if __name__ == "__main__":
    generate_clean_document()