#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并OCR结果文件，生成完整的文档1
"""

import os
import time

def merge_ocr_files():
    """合并OCR处理结果"""
    
    batch1_file = "/mnt/c/Users/M2814/.cursor/investliu/laoliu_notes_ocr_batch1.txt"
    complete_file = "/mnt/c/Users/M2814/.cursor/investliu/laoliu_notes_ocr_complete.txt"
    output_file = "/mnt/c/Users/M2814/.cursor/investliu/老刘投资笔记_文档1_原始OCR提取.txt"
    
    print("开始合并OCR处理结果...")
    
    with open(output_file, 'w', encoding='utf-8') as outf:
        # 写入文档头部
        outf.write("# 老刘投资笔记 - 文档1：原始OCR文字提取结果\n")
        outf.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        outf.write("# 说明：本文档为老刘投资笔记手写内容的OCR识别原始结果\n")
        outf.write("# 处理模型：阿里云 qwen-vl-max-latest\n")
        outf.write("# 文件顺序：按微信图片文件名末尾数字68-94排序\n\n")
        outf.write("=" * 80 + "\n\n")
        
        # 读取并合并batch1文件（跳过头部）
        if os.path.exists(batch1_file):
            print(f"合并文件1: {batch1_file}")
            with open(batch1_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 跳过头部元数据，从第一个##开始
                lines = content.split('\n')
                start_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('## 第1页'):
                        start_index = i
                        break
                
                merged_content = '\n'.join(lines[start_index:])
                outf.write(merged_content)
                outf.write("\n\n")
        
        # 读取并合并complete文件（跳过头部）
        if os.path.exists(complete_file):
            print(f"合并文件2: {complete_file}")
            with open(complete_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 跳过头部元数据，从第一个##开始
                lines = content.split('\n')
                start_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('## 第6页'):
                        start_index = i
                        break
                
                merged_content = '\n'.join(lines[start_index:])
                outf.write(merged_content)
    
    print(f"✓ 合并完成！文档1已保存到: {output_file}")
    return output_file

def main():
    merge_ocr_files()

if __name__ == "__main__":
    main()