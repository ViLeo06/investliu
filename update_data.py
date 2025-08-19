#!/usr/bin/env python3
"""
每日数据更新脚本
用于定时运行，更新股票推荐数据
"""

import os
import sys
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor.data_generator import DataGenerator

def setup_logging():
    """设置日志"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"update_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 50)
    logger.info("老刘投资决策系统 - 每日数据更新")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    
    try:
        # 初始化数据生成器
        generator = DataGenerator()
        
        # 生成所有数据
        success = generator.generate_all_data()
        
        if success:
            # 生成配置文件
            generator.generate_config_file()
            
            # 验证数据
            if generator.validate_generated_data():
                logger.info("✅ 数据更新成功！")
                
                # 显示文件列表
                output_dir = generator.output_dir
                files = os.listdir(output_dir)
                logger.info(f"📁 生成的文件 ({len(files)} 个):")
                for file in sorted(files):
                    logger.info(f"   - {file}")
                
                return True
            else:
                logger.error("❌ 数据验证失败")
                return False
        else:
            logger.error("❌ 数据生成失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 更新过程出错: {e}")
        return False
    
    finally:
        logger.info("=" * 50)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)