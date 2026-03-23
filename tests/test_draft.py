"""
测试创建微信公众号草稿(跳过AI生成步骤)
"""
import sys
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from core.weixin_client import WeixinClient
import json


def test_create_draft():
    """测试创建草稿"""

    # 微信公众号配置
    appid = "wx6c09393281a97c88"
    secret = "4afe55d503ee9f8070fc641e0b110b97"

    # 初始化微信客户端
    print("步骤1: 初始化微信客户端...")
    weixin_client = WeixinClient(appid, secret)
    print("✅ 初始化成功\n")

    # 获取access_token
    print("步骤2: 获取access_token...")
    access_token = weixin_client.get_access_token()
    if not access_token:
        print("❌ 获取access_token失败!")
        return False
    print(f"✅ access_token: {access_token[:20]}...\n")

    # 上传封面图
    thumb_media_id = ''
    print("步骤3: 上传封面图...")
    try:
        # 创建一个简单的符合微信要求的封面图(2.35:1比例,最小900*383像素)
        try:
            from PIL import Image, ImageDraw, ImageFont
            import tempfile

            # 创建900*383像素的图片
            img = Image.new('RGB', (900, 383), color='#3498db')
            draw = ImageDraw.Draw(img)

            # 绘制文字
            text = "AI Technology"
            # 计算文字居中位置
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((900 - text_width) / 2, (383 - text_height) / 2)
            draw.text(position, text, fill='white', font=font)

            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
                img.save(f, format='JPEG', quality=95)
                temp_image_path = f.name

            # 上传图片到微信素材库(作为永久素材)
            thumb_media_id = weixin_client.add_material(temp_image_path, media_type='thumb')
            import os
            os.unlink(temp_image_path)

            if not thumb_media_id:
                print("⚠️ 上传封面图失败,使用空thumb_media_id继续...")
                thumb_media_id = ''
            else:
                print(f"✅ 封面图上传成功, media_id: {thumb_media_id}")
        except ImportError:
            print("⚠️ PIL未安装,跳过封面图上传...")
            thumb_media_id = ''
    except Exception as e:
        print(f"⚠️ 上传封面图时出错: {e}")
        thumb_media_id = ''
    print()

    # 测试文章内容
    article_data = {
        'title': 'AI技术发展趋势分析',
        'author': 'AI助手',
        'digest': '本文分析AI技术发展趋势',
        'content': '''<section style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif;">
<h2>AI技术发展趋势分析</h2>

<p>随着人工智能技术的快速发展,我们正迎来一个全新的AI时代。本文将深入分析当前AI领域的主要发展趋势。</p>

<h3>1. 大语言模型的突破</h3>

<p>大语言模型在推理能力、多轮对话准确性等方面取得了显著进展。</p>

<h3>2. 多模态AI的兴起</h3>

<p>多模态AI能够同时处理文本、图像、音频等多种数据类型。</p>

<h3>3. 边缘AI的普及</h3>

<p>AI模型开始在手机、汽车、智能家居等终端设备上运行。</p>

<h3>4. AI+行业深度融合</h3>

<p>AI技术与各行各业深度融合,推动产业数字化转型。</p>

<h3>5. 负责任的AI</h3>

<p>如何确保AI的安全性、公平性和可解释性成为重要议题。</p>

<h2>总结</h2>

<p>人工智能技术正在以前所未有的速度发展,我们期待在未来看到更多创新突破。</p>
</section>''',
        'thumb_media_id': thumb_media_id,  # 使用上传的图片media_id
        'show_cover_pic': 1 if thumb_media_id else 0,
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }

    print("="*60)
    print("测试创建微信公众号草稿")
    print("="*60)
    print(f"AppID: {appid}")
    print(f"文章标题: {article_data['title']}")
    print("="*60 + "\n")

    # 查看现有草稿
    print("步骤4: 查看现有草稿...")
    drafts = weixin_client.get_drafts(offset=0, count=5, no_content=1)
    if drafts:
        print(f"✅ 当前草稿箱中有 {len(drafts)} 篇草稿:")
        for idx, draft in enumerate(drafts, 1):
            title = draft.get('content', {}).get('news_item', [{}])[0].get('title', '无标题')
            # 解码Unicode转义字符
            if '\\u' in title:
                title = title.encode().decode('unicode-escape')
            print(f"  {idx}. {title}")
    else:
        print("当前草稿箱为空")
    print()

    # 创建草稿
    print("步骤5: 创建新草稿...")
    media_id = weixin_client.add_draft(article_data)
    if not media_id:
        print("❌ 创建草稿失败!")
        return False
    print(f"✅ 草稿创建成功!")
    print(f"草稿ID: {media_id}\n")

    # 再次查看草稿列表
    print("步骤6: 查看更新后的草稿列表...")
    drafts = weixin_client.get_drafts(offset=0, count=5, no_content=1)
    if drafts:
        print(f"✅ 当前草稿箱中有 {len(drafts)} 篇草稿:")
        for idx, draft in enumerate(drafts, 1):
            title = draft.get('content', {}).get('news_item', [{}])[0].get('title', '无标题')
            # 解码Unicode转义字符
            if '\\u' in title:
                title = title.encode().decode('unicode-escape')
            print(f"  {idx}. {title}")

    print("\n" + "="*60)
    print("✅ 测试完成!")
    print("请登录微信公众号后台查看草稿箱")
    print("="*60)

    return True


if __name__ == '__main__':
    test_create_draft()
