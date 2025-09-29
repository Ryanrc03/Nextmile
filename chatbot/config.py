#!/usr/bin/env python3
"""
Configuration file for Resume RAG System
"""

# Model Configuration
MODEL_CONFIG = {
    "base_url": "https://api-inference.modelscope.cn/v1",
    "api_key": "ms-74b8eedd-5f76-419a-a513-f421399093da",
    "model_name": "deepseek-ai/DeepSeek-V3.1",
    "temperature": 0.7,
    "max_tokens": 2000
}

# RAG Configuration
RAG_CONFIG = {
    "similarity_top_k": 5,
    "keyword_weight": 0.6,
    "exact_match_weight": 0.3,
    "length_bonus_weight": 0.1,
    "min_score_threshold": 0.1
}

# Default Excel file path
DEFAULT_EXCEL_PATH = "Rongcheng_Li_Resume_Data.xlsx"

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# API Configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_origins": ["*"],
    "cors_credentials": True,
    "cors_methods": ["*"],
    "cors_headers": ["*"]
}