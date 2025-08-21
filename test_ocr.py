#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试qwen-vl-max OCR功能
"""

import os
import base64
import json
import requests

def test_single_image():
    """测试单个图片的OCR识别"""
    
    # 配置
    API_KEY = "sk-2eee3571d9954f5282586c576e33bfd5"
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    IMAGE_PATH = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook/微信图片_20250820223018_68.jpg"
    
    # 编码图片
    with open(IMAGE_PATH, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 构建请求
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
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
    
    print("发送API请求...")
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        extracted_text = result['choices'][0]['message']['content'].strip()
        print("\n✓ OCR识别结果:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)
        
        # 保存结果
        with open('test_ocr_result.txt', 'w', encoding='utf-8') as f:
            f.write(f"# 测试OCR结果 - {os.path.basename(IMAGE_PATH)}\n\n")
            f.write(extracted_text)
        
        print(f"\n结果已保存到: test_ocr_result.txt")
        
    else:
        print(f"❌ API调用失败:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

if __name__ == "__main__":
    test_single_image()