"""
OCR笔记处理模块
处理老刘的手写投资笔记，将图像转换为文本
"""

import os
import sys
import json
import time
from datetime import datetime
from PIL import Image
import logging

# 导入OCR相关库
try:
    from aip import AipOcr
    BAIDU_AVAILABLE = True
except ImportError:
    BAIDU_AVAILABLE = False
    print("警告: 百度OCR SDK未安装，请运行: pip install baidu-aip")

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.ocr.v20181119 import ocr_client, models
    TENCENT_AVAILABLE = True
except ImportError:
    TENCENT_AVAILABLE = False
    print("警告: 腾讯云OCR SDK未安装，请运行: pip install tencentcloud-sdk-python")

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, config_path="config.py"):
        self.config = self._load_config(config_path)
        self.baidu_client = None
        self.tencent_client = None
        self._init_ocr_clients()
    
    def _load_config(self, config_path):
        """加载配置文件"""
        try:
            sys.path.append(os.path.dirname(config_path))
            import config
            return config
        except ImportError:
            logger.warning("配置文件未找到，使用示例配置")
            return None
    
    def _init_ocr_clients(self):
        """初始化OCR客户端"""
        if self.config and BAIDU_AVAILABLE:
            try:
                self.baidu_client = AipOcr(
                    self.config.BAIDU_OCR_APP_ID,
                    self.config.BAIDU_OCR_API_KEY,
                    self.config.BAIDU_OCR_SECRET_KEY
                )
                logger.info("百度OCR客户端初始化成功")
            except Exception as e:
                logger.error(f"百度OCR初始化失败: {e}")
        
        if self.config and TENCENT_AVAILABLE:
            try:
                cred = credential.Credential(
                    self.config.TENCENT_SECRET_ID,
                    self.config.TENCENT_SECRET_KEY
                )
                httpProfile = HttpProfile()
                httpProfile.endpoint = "ocr.tencentcloudapi.com"
                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                self.tencent_client = ocr_client.OcrClient(cred, self.config.TENCENT_REGION, clientProfile)
                logger.info("腾讯OCR客户端初始化成功")
            except Exception as e:
                logger.error(f"腾讯OCR初始化失败: {e}")
    
    def process_image_baidu(self, image_path):
        """使用百度OCR处理单张图片"""
        if not self.baidu_client:
            logger.error("百度OCR客户端未初始化")
            return None
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 使用高精度版本
            result = self.baidu_client.handwriting(image_data)
            
            if 'words_result' in result:
                text_lines = []
                for item in result['words_result']:
                    text_lines.append(item['words'])
                return '\n'.join(text_lines)
            else:
                logger.error(f"OCR识别失败: {result}")
                return None
                
        except Exception as e:
            logger.error(f"百度OCR处理失败 {image_path}: {e}")
            return None
    
    def process_image_tencent(self, image_path):
        """使用腾讯OCR处理单张图片"""
        if not self.tencent_client:
            logger.error("腾讯OCR客户端未初始化")
            return None
        
        try:
            with open(image_path, 'rb') as f:
                import base64
                image_data = base64.b64encode(f.read()).decode()
            
            req = models.HandwritingOCRRequest()
            req.ImageBase64 = image_data
            
            resp = self.tencent_client.HandwritingOCR(req)
            
            text_lines = []
            for item in resp.TextDetections:
                text_lines.append(item.DetectedText)
            
            return '\n'.join(text_lines)
            
        except Exception as e:
            logger.error(f"腾讯OCR处理失败 {image_path}: {e}")
            return None
    
    def process_folder(self, input_folder, output_folder, provider="baidu"):
        """批量处理文件夹中的图片"""
        if not os.path.exists(input_folder):
            logger.error(f"输入文件夹不存在: {input_folder}")
            return
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        image_files = [f for f in os.listdir(input_folder) 
                      if f.lower().endswith(supported_formats)]
        
        results = {}
        total_files = len(image_files)
        
        logger.info(f"开始处理 {total_files} 张图片...")
        
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_folder, filename)
            logger.info(f"处理 {i}/{total_files}: {filename}")
            
            # 选择OCR提供商
            if provider == "baidu":
                text = self.process_image_baidu(image_path)
            elif provider == "tencent":
                text = self.process_image_tencent(image_path)
            else:
                logger.error(f"不支持的OCR提供商: {provider}")
                continue
            
            if text:
                # 保存文本文件
                text_filename = os.path.splitext(filename)[0] + '.txt'
                text_path = os.path.join(output_folder, text_filename)
                
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                results[filename] = {
                    'status': 'success',
                    'text_length': len(text),
                    'output_file': text_filename
                }
                
                logger.info(f"成功处理: {filename} -> {text_filename}")
            else:
                results[filename] = {
                    'status': 'failed',
                    'error': 'OCR识别失败'
                }
                logger.error(f"处理失败: {filename}")
            
            # 添加延迟，避免API调用过频
            time.sleep(1)
        
        # 保存处理结果
        result_file = os.path.join(output_folder, 'ocr_results.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 生成汇总文本
        self._generate_summary(output_folder)
        
        logger.info(f"批量处理完成！结果保存在: {output_folder}")
        return results
    
    def _generate_summary(self, output_folder):
        """生成所有文本的汇总文件"""
        all_text = []
        text_files = [f for f in os.listdir(output_folder) if f.endswith('.txt')]
        
        for text_file in sorted(text_files):
            if text_file == 'summary.txt':
                continue
                
            text_path = os.path.join(output_folder, text_file)
            with open(text_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    all_text.append(f"=== {text_file} ===")
                    all_text.append(content)
                    all_text.append("")
        
        summary_path = os.path.join(output_folder, 'summary.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        logger.info(f"汇总文件已生成: {summary_path}")

def main():
    """主函数"""
    processor = OCRProcessor()
    
    # 设置输入输出路径
    input_folder = "notes/images"  # 放置老刘笔记图片的文件夹
    output_folder = "notes/processed"  # 处理后的文本文件夹
    
    # 创建示例文件夹
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    # 检查是否有图片文件
    if not os.listdir(input_folder):
        logger.info(f"请将老刘的笔记图片放入 {input_folder} 文件夹中")
        logger.info("支持的格式: jpg, jpeg, png, bmp, tiff")
        return
    
    # 开始批量处理
    results = processor.process_folder(input_folder, output_folder, provider="baidu")
    
    # 输出统计信息
    if results:
        success_count = sum(1 for r in results.values() if r['status'] == 'success')
        total_count = len(results)
        logger.info(f"处理完成: {success_count}/{total_count} 成功")

if __name__ == "__main__":
    main()