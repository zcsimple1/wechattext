"""
测试扣子(Coze) API调用
使用Webhook方式调用已发布的Bot
"""
import sys
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import json


# ==================== 配置区域 ====================
# 请替换为你的扣子配置
COZE_WEBHOOK_URL = "你的Webhook URL"  # 例如: https://api.coze.cn/v1/webhook/xxxxx
COZE_BEARER_TOKEN = "你的Bearer Token"  # 例如: Bearer pat_xxxxx

# 或者使用工作流方式
WORKFLOW_ID = "你的工作流ID"  # 例如: 7451xxxx
WORKFLOW_API_TOKEN = "你的API Token"  # 例如: pat_xxxxx
# =================================================


def test_coze_webhook():
    """测试Webhook方式调用"""

    if COZE_WEBHOOK_URL == "你的Webhook URL":
        print("⚠️ 请先配置 COZE_WEBHOOK_URL")
        print("\n使用说明:")
        print("1. 登录 https://www.coze.cn")
        print("2. 创建一个Bot并发布")
        print("3. 在Bot设置中添加Webhook触发器")
        print("4. 复制Webhook URL到这里")
        return None

    print("="*60)
    print("测试扣子(Coze) Webhook API")
    print("="*60)
    print(f"URL: {COZE_WEBHOOK_URL}")
    print("="*60 + "\n")

    # 构造请求
    url = COZE_WEBHOOK_URL
    headers = {
        'Authorization': COZE_BEARER_TOKEN,
        'Content-Type': 'application/json'
    }

    # 请求数据
    data = {
        "query": "你好,请介绍一下你自己",
        "conversation_id": ""
    }

    print("发送请求...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")
        print(f"\n响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def test_coze_workflow():
    """测试工作流方式调用"""

    if WORKFLOW_ID == "你的工作流ID" or WORKFLOW_API_TOKEN == "你的API Token":
        print("⚠️ 请先配置 WORKFLOW_ID 和 WORKFLOW_API_TOKEN")
        return None

    print("="*60)
    print("测试扣子(Coze) 工作流 API")
    print("="*60)
    print(f"Workflow ID: {WORKFLOW_ID}")
    print("="*60 + "\n")

    url = f"https://api.coze.cn/v1/workflow/run"
    headers = {
        'Authorization': f'Bearer {WORKFLOW_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        "workflow_id": WORKFLOW_ID,
        "parameters": {
            "input": "你好,介绍一下AI科技的最新动态"
        }
    }

    print("发送请求...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")
        print(f"\n响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def show_curl_example():
    """显示curl调用示例"""
    print("\n" + "="*60)
    print("curl 调用示例 (Webhook方式)")
    print("="*60)
    print("""
# Webhook调用
curl -X POST '你的Webhook URL' \\
  -H 'Authorization: Bearer 你的Token' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "query": "你好",
    "conversation_id": ""
  }'

# 工作流调用
curl -X POST 'https://api.coze.cn/v1/workflow/run' \\
  -H 'Authorization: Bearer 你的API Token' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "workflow_id": "你的工作流ID",
    "parameters": {
      "input": "你好"
    }
  }'
""")


if __name__ == '__main__':
    print("请选择调用方式:")
    print("1. Webhook方式")
    print("2. 工作流方式")
    print("3. 显示curl示例")
    print("0. 退出")

    choice = input("\n请输入选项 (1/2/3/0): ").strip()

    if choice == '1':
        test_coze_webhook()
    elif choice == '2':
        test_coze_workflow()
    elif choice == '3':
        show_curl_example()
    else:
        print("退出")
