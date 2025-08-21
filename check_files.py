#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整处理所有图片文件 - 重新排序和检查
"""

import os
import re
from pathlib import Path

def check_all_files():
    """检查所有图片文件并排序"""
    
    notebook_dir = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook"
    image_dir = Path(notebook_dir)
    
    # 获取所有jpg文件
    image_files = list(image_dir.glob("*.jpg"))
    
    print(f"发现 {len(image_files)} 个jpg文件")
    
    # 按文件名中的数字排序
    def extract_number(filename):
        match = re.search(r'_(\d{2})\.jpg$', str(filename))
        return int(match.group(1)) if match else 999
    
    sorted_files = sorted(image_files, key=extract_number)
    
    print("\n完整文件列表（按顺序）：")
    print("=" * 60)
    
    for i, file_path in enumerate(sorted_files, 1):
        filename = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        number = extract_number(filename)
        print(f"{i:2d}. 第{number:2d}页: {filename} ({size:,} bytes)")
    
    return sorted_files

if __name__ == "__main__":
    files = check_all_files()
    print(f"\n总计: {len(files)} 个文件")