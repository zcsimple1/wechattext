"""
AI内容生成模块
支持元宝和豆包API
"""
import json
import requests
from datetime import datetime
from typing import Dict, Optional


class AIContentGenerator:
    """AI内容生成器"""
    
    def __init__(self, config: Dict):
        """
        初始化AI内容生成器
        
        Args:
            config: 配置字典,包含AI提供商信息和API密钥
        """
        self.config = config
        self.ai_provider = config.get('ai_provider', 'doubao')
        
        if self.ai_provider == 'doubao':
            self.api_key = config['doubao']['api_key']
            self.model = config['doubao']['model']
            self.api_url = config['doubao']['api_url']
        elif self.ai_provider == 'yuanbao':
            self.api_key = config['yuanbao']['api_key']
            self.model = config['yuanbao']['model']
            self.api_url = config['yuanbao']['api_url']
        else:
            raise ValueError(f"不支持的AI提供商: {self.ai_provider}")
    
    def _generate_prompt(self, category: str, max_words: int) -> str:
        """
        生成AI提示词
        
        Args:
            category: 文章分类
            max_words: 最大字数
            
        Returns:
            提示词字符串
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        prompt = f"""请为一篇关于【{category}】热点文章撰写内容。

要求：
1. 文章发布日期：{today}
2. 主题：结合当前{today}的{category}热点话题
3. 字数：控制在{max_words}字以内
4. 内容要求：
   - 开头要有吸引人的标题和引言
   - 内容要有深度分析，包含案例或数据支持
   - 语言风格专业但不晦涩，适合大众阅读
   - 结尾要有总结和展望
5. 格式：使用Markdown格式，包含适当的标题层级

请直接输出文章内容，不要有额外的解释或说明。"""
        
        return prompt
    
    def generate_article(self, category: str = "AI科技", max_words: int = 2000) -> Optional[Dict]:
        """
        生成文章内容
        
        Args:
            category: 文章分类,默认为"AI科技"
            max_words: 最大字数,默认为2000字
            
        Returns:
            包含title和content的字典,如果失败返回None
        """
        try:
            prompt = self._generate_prompt(category, max_words)
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': '你是一个专业的科技文章撰写专家,擅长撰写深度、有趣的科技热点文章。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': max_words * 2  # token数约为字数的2倍
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # 提取生成的内容
            content = result['choices'][0]['message']['content'].strip()
            
            # 从内容中提取标题(第一行)
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip()
            article_content = '\n'.join(lines[1:]).strip()
            
            return {
                'title': title,
                'content': article_content,
                'raw_content': content,
                'category': category,
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            
        except requests.exceptions.RequestException as e:
            print(f"AI API请求失败: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"解析AI响应失败: {e}")
            return None
        except Exception as e:
            print(f"生成文章时发生错误: {e}")
            return None
