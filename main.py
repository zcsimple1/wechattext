"""
微信公众号AI文章自动生成与发布工具
主程序
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

from ai_generator import AIContentGenerator
from weixin_client import WeixinClient


def load_config(config_path: str = "config.json") -> dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"配置文件 {config_path} 不存在")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        sys.exit(1)


def generate_and_publish(category: str = None, max_words: int = None) -> bool:
    """
    生成并发布文章的主流程
    
    Args:
        category: 文章分类,默认使用配置文件中的设置
        max_words: 最大字数,默认使用配置文件中的设置
        
    Returns:
        是否成功
    """
    # 加载配置
    config = load_config()
    
    # 使用默认值或传入参数
    category = category or config['article']['category']
    max_words = max_words or config['article']['max_words']
    
    print(f"\n{'='*60}")
    print(f"微信公众号AI文章生成工具")
    print(f"{'='*60}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"分类: {category}")
    print(f"最大字数: {max_words}")
    print(f"AI提供商: {config['ai_provider']}")
    print(f"{'='*60}\n")
    
    # 步骤1: 使用AI生成文章内容
    print("步骤1: 正在使用AI生成文章内容...")
    ai_generator = AIContentGenerator(config)
    article_data = ai_generator.generate_article(category=category, max_words=max_words)
    
    if not article_data:
        print("❌ 生成文章失败!")
        return False
    
    print(f"✅ 文章生成成功!")
    print(f"标题: {article_data['title']}")
    print(f"内容长度: {len(article_data['content'])} 字\n")
    
    # 保存生成的文章到本地
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = output_dir / f"article_{date_str}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(article_data['raw_content'])
    print(f"文章已保存到: {output_file}\n")
    
    # 步骤2: 初始化微信客户端
    print("步骤2: 正在连接微信公众号API...")
    weixin_client = WeixinClient(
        appid=config['weixin']['appid'],
        secret=config['weixin']['secret']
    )
    
    # 步骤3: 获取access_token
    print("步骤3: 正在获取access_token...")
    access_token = weixin_client.get_access_token()
    if not access_token:
        print("❌ 获取access_token失败!")
        return False
    print(f"✅ access_token获取成功!\n")
    
    # 步骤4: 将Markdown转换为HTML
    print("步骤4: 正在转换文章格式...")
    html_content = weixin_client.markdown_to_html(article_data['raw_content'])
    print(f"✅ 格式转换完成!\n")
    
    # 步骤5: 创建微信公众号草稿
    print("步骤5: 正在创建草稿...")
    draft_data = {
        'title': article_data['title'],
        'author': 'AI助手',
        'digest': article_data['content'][:100].replace('\n', ' '),
        'content': html_content,
        'thumb_media_id': '',  # 需要先上传图片获取media_id
        'show_cover_pic': 0,   # 暂不显示封面
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }
    
    # 注意: 首次使用需要先上传封面图片获取thumb_media_id
    # 如果没有thumb_media_id,可以先设置为空字符串,但文章发布时需要封面
    
    media_id = weixin_client.add_draft(draft_data)
    
    if not media_id:
        print("❌ 创建草稿失败!")
        return False
    
    print(f"✅ 草稿创建成功!")
    print(f"草稿ID: {media_id}\n")
    
    # 步骤6: 查看草稿列表
    print("步骤6: 正在获取草稿列表...")
    drafts = weixin_client.get_drafts(offset=0, count=5, no_content=1)
    if drafts:
        print(f"✅ 当前草稿箱中有 {len(drafts)} 篇草稿:")
        for idx, draft in enumerate(drafts[:5], 1):
            print(f"  {idx}. {draft.get('content', {}).get('news_item', [{}])[0].get('title', '无标题')}")
    print()
    
    print(f"{'='*60}")
    print("🎉 任务完成!")
    print(f"{'='*60}")
    print("请在微信公众号后台查看并编辑草稿,确认无误后即可发布。")
    print("注意: 草稿默认没有封面图,需要在后台手动添加。")
    print(f"{'='*60}\n")
    
    return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信公众号AI文章生成工具')
    parser.add_argument('--category', '-c', type=str, help='文章分类,例如: AI科技')
    parser.add_argument('--words', '-w', type=int, help='最大字数,默认2000字')
    parser.add_argument('--config', type=str, default='config.json', help='配置文件路径')
    
    args = parser.parse_args()
    
    try:
        success = generate_and_publish(
            category=args.category,
            max_words=args.words
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
