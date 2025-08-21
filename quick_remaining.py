#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速补充处理剩余图片
"""

import os
import base64
import time
import requests
from pathlib import Path
import re

def get_remaining_files():
    """获取剩余未处理的图片文件"""
    
    # 已处理的文件（根据之前的结果）
    processed_numbers = list(range(68, 84))  # 68-83已处理
    
    # 所有文件编号
    all_numbers = list(range(68, 95))  # 68-94
    
    # 未处理的编号
    remaining_numbers = [n for n in all_numbers if n not in processed_numbers]
    
    # 构建文件路径
    notebook_dir = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook"
    remaining_files = []
    
    for num in remaining_numbers:
        # 查找对应的文件
        pattern = f"*_{num:02d}.jpg"
        files = list(Path(notebook_dir).glob(pattern))
        if files:
            remaining_files.append((num, str(files[0])))
    
    return sorted(remaining_files)

def extract_text(image_path, api_key):
    """提取文字"""
    
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = {
            "model": "qwen-vl-max-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "请准确识别图片中的所有手写文字内容，保持原有的换行和标点符号，不要添加任何解释或分析，只输出识别到的文字内容。"
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4096
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"[识别失败: HTTP {response.status_code}]"
            
    except Exception as e:
        return f"[识别失败: {str(e)}]"

def main():
    """快速处理剩余文件"""
    API_KEY = "sk-2eee3571d9954f5282586c576e33bfd5"
    
    # 获取剩余文件
    remaining_files = get_remaining_files()
    
    print(f"需要补充处理 {len(remaining_files)} 个文件:")
    for num, path in remaining_files:
        print(f"  第{num}页: {os.path.basename(path)}")
    
    print("\n开始快速处理...")
    print("=" * 50)
    
    # 处理并保存结果
    output_file = "剩余图片OCR结果.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 剩余图片OCR识别结果\n")
        f.write(f"# 处理时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for i, (num, image_path) in enumerate(remaining_files, 1):
            filename = os.path.basename(image_path)
            print(f"[{i}/{len(remaining_files)}] 处理第{num}页: {filename}")
            
            # 提取文字
            text = extract_text(image_path, API_KEY)
            
            # 写入文件
            f.write(f"## 第{num}页 - {filename}\n\n")
            f.write(f"{text}\n\n")
            f.write("-" * 80 + "\n\n")
            
            print(f"✓ 完成")
            time.sleep(2)
    
    print("=" * 50)
    print(f"✓ 剩余文件处理完成: {output_file}")

if __name__ == "__main__":
    main()