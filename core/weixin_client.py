"""
微信公众号API客户端
实现获取access_token、获取草稿、创建草稿等功能
"""
import json
import requests
from typing import Dict, Optional, List


class WeixinClient:
    """微信公众号API客户端"""
    
    def __init__(self, appid: str, secret: str):
        """
        初始化微信客户端
        
        Args:
            appid: 微信公众号AppID
            secret: 微信公众号AppSecret
        """
        self.appid = appid
        self.secret = secret
        self.access_token = None
        self.base_url = "https://api.weixin.qq.com/cgi-bin"
    
    def get_access_token(self) -> Optional[str]:
        """
        获取微信公众号access_token
        
        Returns:
            access_token字符串,如果失败返回None
        """
        try:
            url = f"{self.base_url}/token"
            params = {
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'errcode' in result and result['errcode'] != 0:
                print(f"获取access_token失败: {result.get('errmsg', '未知错误')}")
                return None
            
            self.access_token = result.get('access_token')
            print(f"成功获取access_token: {self.access_token[:20]}...")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"请求access_token失败: {e}")
            return None
        except Exception as e:
            print(f"获取access_token时发生错误: {e}")
            return None
    
    def get_drafts(self, offset: int = 0, count: int = 20, no_content: int = 0) -> Optional[List]:
        """
        获取草稿箱列表
        
        Args:
            offset: 起始位置偏移量
            count: 获取的数量
            no_content: 1表示不返回content字段
            
        Returns:
            草稿列表,如果失败返回None
        """
        try:
            if not self.access_token:
                self.get_access_token()
                if not self.access_token:
                    return None
            
            url = f"{self.base_url}/draft/batchget?access_token={self.access_token}"
            data = {
                'offset': offset,
                'count': count,
                'no_content': no_content
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'errcode' in result and result['errcode'] != 0:
                print(f"获取草稿失败: {result.get('errmsg', '未知错误')}")
                return None
            
            return result.get('item', [])
            
        except requests.exceptions.RequestException as e:
            print(f"请求草稿列表失败: {e}")
            return None
        except Exception as e:
            print(f"获取草稿时发生错误: {e}")
            return None
    
    def add_draft(self, article_data: Dict) -> Optional[str]:
        """
        创建新草稿
        
        Args:
            article_data: 文章数据,格式为:
                {
                    "title": "文章标题",
                    "content": "文章内容(HTML格式)",
                    "digest": "摘要",
                    "author": "作者",
                    "thumb_media_id": "封面图片media_id"
                }
            
        Returns:
            media_id字符串,如果失败返回None
        """
        try:
            if not self.access_token:
                self.get_access_token()
                if not self.access_token:
                    return None
            
            url = f"{self.base_url}/draft/add?access_token={self.access_token}"
            
            # 构建符合微信公众号API要求的文章格式
            articles = [{
                "title": article_data.get('title', ''),
                "author": article_data.get('author', 'AI助手'),
                "digest": article_data.get('digest', ''),
                "content": article_data.get('content', ''),
                "content_source_url": article_data.get('content_source_url', ''),
                "thumb_media_id": article_data.get('thumb_media_id', ''),
                "show_cover_pic": 1 if article_data.get('show_cover_pic', False) else 0,
                "need_open_comment": article_data.get('need_open_comment', 0),
                "only_fans_can_comment": article_data.get('only_fans_can_comment', 0)
            }]
            
            payload = {
                "articles": articles
            }

            # 手动序列化JSON,确保中文不转义
            import json
            payload_str = json.dumps(payload, ensure_ascii=False)

            response = requests.post(url, data=payload_str.encode('utf-8'),
                                  headers={'Content-Type': 'application/json; charset=utf-8'},
                                  timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'errcode' in result and result['errcode'] != 0:
                print(f"创建草稿失败: {result.get('errmsg', '未知错误')}")
                return None
            
            media_id = result.get('media_id')
            print(f"成功创建草稿, media_id: {media_id}")
            return media_id
            
        except requests.exceptions.RequestException as e:
            print(f"请求创建草稿失败: {e}")
            return None
        except Exception as e:
            print(f"创建草稿时发生错误: {e}")
            return None
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """
        将Markdown转换为简单的HTML格式
        
        Args:
            markdown_text: Markdown格式文本
            
        Returns:
            HTML格式文本
        """
        # 简单的Markdown转HTML实现
        html = markdown_text
        
        # 转换标题
        html = html.replace('### ', '<h3>').replace('\n', '</h3>\n')
        html = html.replace('## ', '<h2>').replace('\n', '</h2>\n')
        html = html.replace('# ', '<h1>').replace('\n', '</h1>\n')
        
        # 转换加粗
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        
        # 转换列表
        html = html.replace('- ', '<li>')
        
        # 转换段落
        lines = html.split('\n')
        html_lines = []
        in_paragraph = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
            elif line.startswith('<') or line.startswith('</'):
                html_lines.append(line)
            else:
                if not in_paragraph:
                    html_lines.append('<p>')
                    in_paragraph = True
                html_lines.append(line)
        
        if in_paragraph:
            html_lines.append('</p>')
        
        return '\n'.join(html_lines)

    def add_material(self, image_path: str, media_type: str = 'thumb') -> Optional[str]:
        """
        上传永久素材到微信公众号

        Args:
            image_path: 图片文件路径
            media_type: 素材类型, thumb(封面图)、image(图片)、voice(语音)、video(视频)

        Returns:
            media_id字符串,如果失败返回None
        """
        try:
            if not self.access_token:
                self.get_access_token()
                if not self.access_token:
                    return None

            url = f"{self.base_url}/material/add_material?access_token={self.access_token}&type={media_type}"

            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)

            response.raise_for_status()
            result = response.json()

            if 'errcode' in result and result['errcode'] != 0:
                print(f"上传永久素材失败: {result.get('errmsg', '未知错误')}")
                return None

            media_id = result.get('media_id', '')
            print(f"成功上传永久素材, media_id: {media_id}")
            return media_id

        except FileNotFoundError:
            print(f"图片文件不存在: {image_path}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"上传永久素材请求失败: {e}")
            return None
        except Exception as e:
            print(f"上传永久素材时发生错误: {e}")
            return None
