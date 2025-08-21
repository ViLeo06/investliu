#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于现有进度生成中期完整文档
"""

import json
import time
import os

def load_progress_and_generate_doc():
    """基于进度文件生成中期文档"""
    
    progress_file = "ocr_progress_5.json"
    
    if not os.path.exists(progress_file):
        print(f"❌ 进度文件不存在: {progress_file}")
        return
    
    # 读取进度
    with open(progress_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"📊 当前进度: 已处理 {len(results)} 页")
    
    # 生成中期完整文档
    doc_file = "老刘投资笔记_中期完整文档1.txt"
    
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write("# 老刘投资笔记 - 中期完整文档1：原始OCR文字提取结果\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# 说明：基于当前处理进度的OCR识别结果\n")
        f.write(f"# 当前进度：{len(results)}/27页\n")
        f.write("# 处理方法：多重OCR模型比对验证\n\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"## 第{result['page_num']}页 - {result['filename']}\n")
            f.write(f"### 最佳识别方法: {result['best_method']}\n\n")
            
            # 提取核心文字（去除过度解析）
            best_text = result['best_text']
            if result['best_method'] == 'optimized-prompt' and '**原文识别如下：**' in best_text:
                # 提取原文部分
                parts = best_text.split('**原文识别如下：**')
                if len(parts) > 1:
                    raw_text = parts[1].split('---')[0].strip()
                    # 清理格式标记
                    raw_text = raw_text.replace('> ', '').replace('>', '').strip()
                    f.write(f"{raw_text}\n\n")
                else:
                    f.write(f"{best_text}\n\n")
            else:
                f.write(f"{best_text}\n\n")
            
            f.write("-" * 80 + "\n\n")
    
    print(f"✓ 中期文档已生成: {doc_file}")
    
    # 生成方法比对统计
    method_stats = {}
    for result in results:
        method = result['best_method']
        method_stats[method] = method_stats.get(method, 0) + 1
    
    print(f"\n📈 当前最佳方法统计:")
    for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method}: {count} 页 ({count/len(results)*100:.1f}%)")
    
    # 检查各方法识别质量
    print(f"\n🔍 识别质量分析:")
    for result in results:
        page = result['page_num']
        methods = result['results']
        print(f"  第{page}页:")
        for method, text in methods.items():
            length = len(text)
            status = "✓" if not text.startswith('[') else "✗"
            print(f"    {method}: {status} {length} 字符")

if __name__ == "__main__":
    load_progress_and_generate_doc()