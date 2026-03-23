"""
测试AI生成文章功能(模拟模式)
"""
import sys
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from core.ai_generator import AIContentGenerator
import json


def test_ai_generation():
    """测试AI文章生成"""

    # 加载配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("="*60)
    print("测试AI文章生成功能")
    print("="*60)
    print(f"AI提供商: {config['ai_provider']}")
    print(f"模型: {config['doubao']['model']}")
    print("="*60 + "\n")

    # 检查API密钥是否配置
    api_key = config['doubao']['api_key']
    if api_key == 'YOUR_DOUBAO_API_KEY':
        print("⚠️ 豆包API密钥未配置")
        print("请先在config.json中配置豆包API密钥")
        print("\n或者使用模拟数据测试...")

        # 模拟AI返回数据
        mock_article = {
            'title': '2025年AI技术发展十大趋势',
            'content': '''# 2025年AI技术发展十大趋势

随着2025年的到来,人工智能技术继续以前所未有的速度发展。本文将深入分析本年度AI领域最重要的十大发展趋势。

## 1. 大语言模型的持续进化

GPT-5、Claude-4等新一代大语言模型预计将在2025年发布,它们将在推理能力、上下文理解和多任务处理方面实现重大突破。

## 2. 多模态AI的普及

AI将能够同时处理文本、图像、音频和视频数据,实现真正的跨模态理解和生成。

## 3. AI与物理世界的融合

机器人技术、自动驾驶和智能硬件将更加依赖AI决策,实现与物理世界的深度交互。

## 4. 边缘AI的崛起

AI模型将更多地运行在终端设备上,减少延迟并保护用户隐私。

## 5. AI代理的成熟

能够自主执行复杂任务的AI代理将成为主流,彻底改变人机交互方式。

## 6. AI编程的普及

AI辅助编程工具将使更多人能够参与软件开发,降低技术门槛。

## 7. AI在科学研究的突破

AI将在蛋白质折叠、新材料发现等领域发挥关键作用。

## 8. AI伦理与监管的完善

各国将建立更完善的AI监管框架,确保技术发展符合人类价值观。

## 9. AI与生物技术的融合

AI在药物研发、基因编辑等领域将带来革命性变化。

## 10. 民主化AI工具

更多开源AI工具和平台将涌现,让AI技术触手可及。

## 总结

2025年将是AI技术发展的关键一年,我们期待看到更多创新突破,同时也要关注技术带来的社会影响。''',
            'raw_content': '''# 2025年AI技术发展十大趋势

随着2025年的到来,人工智能技术继续以前所未有的速度发展。本文将深入分析本年度AI领域最重要的十大发展趋势。

## 1. 大语言模型的持续进化

GPT-5、Claude-4等新一代大语言模型预计将在2025年发布,它们将在推理能力、上下文理解和多任务处理方面实现重大突破。

## 2. 多模态AI的普及

AI将能够同时处理文本、图像、音频和视频数据,实现真正的跨模态理解和生成。

## 3. AI与物理世界的融合

机器人技术、自动驾驶和智能硬件将更加依赖AI决策,实现与物理世界的深度交互。

## 4. 边缘AI的崛起

AI模型将更多地运行在终端设备上,减少延迟并保护用户隐私。

## 5. AI代理的成熟

能够自主执行复杂任务的AI代理将成为主流,彻底改变人机交互方式。

## 6. AI编程的普及

AI辅助编程工具将使更多人能够参与软件开发,降低技术门槛。

## 7. AI在科学研究的突破

AI将在蛋白质折叠、新材料发现等领域发挥关键作用。

## 8. AI伦理与监管的完善

各国将建立更完善的AI监管框架,确保技术发展符合人类价值观。

## 9. AI与生物技术的融合

AI在药物研发、基因编辑等领域将带来革命性变化。

## 10. 民主化AI工具

更多开源AI工具和平台将涌现,让AI技术触手可及。

## 总结

2025年将是AI技术发展的关键一年,我们期待看到更多创新突破,同时也要关注技术带来的社会影响。''',
            'category': 'AI科技',
            'date': '2025-03-06'
        }

        print("✅ 使用模拟数据成功!")
        print(f"\n标题: {mock_article['title']}")
        print(f"分类: {mock_article['category']}")
        print(f"字数: {len(mock_article['content'])} 字")
        print(f"\n内容预览:")
        print(mock_article['content'][:200] + "...")

        return mock_article

    # 如果API密钥已配置,尝试调用真实API
    try:
        ai_generator = AIContentGenerator(config)
        print("正在调用AI API生成文章...\n")
        article = ai_generator.generate_article(
            category=config['article']['category'],
            max_words=config['article']['max_words']
        )

        if article:
            print("✅ AI文章生成成功!")
            print(f"\n标题: {article['title']}")
            print(f"分类: {article['category']}")
            print(f"字数: {len(article['content'])} 字")
            print(f"\n内容预览:")
            print(article['content'][:200] + "...")
            return article
        else:
            print("❌ AI文章生成失败!")
            return None

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    test_ai_generation()
