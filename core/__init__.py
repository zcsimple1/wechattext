"""
核心模块
包含AI生成器和微信客户端
"""
from .ai_generator import AIContentGenerator
from .weixin_client import WeixinClient

__all__ = ['AIContentGenerator', 'WeixinClient']
