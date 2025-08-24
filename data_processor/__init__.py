"""
数据处理模块初始化文件
"""

from .ocr_processor import OCRProcessor
from .rule_extractor import RuleExtractor
from .stock_data_fetcher import StockDataFetcher
from .stock_analyzer import StockAnalyzer
from .data_generator import DataGenerator

__version__ = "1.0.0"
__author__ = "老刘投资决策系统"

__all__ = [
    'OCRProcessor',
    'RuleExtractor', 
    'StockDataFetcher',
    'StockAnalyzer',
    'DataGenerator'
]