# 测试中文编码
import requests
import json

# 测试数据
data = {
    "title": "AI技术发展趋势分析",
    "content": "测试内容"
}

# 方法1: 直接json参数
print("方法1: json参数")
print(json.dumps(data, ensure_ascii=False))

# 方法2: 手动编码
print("\n方法2: 手动编码")
payload_str = json.dumps(data, ensure_ascii=False)
print(payload_str.encode('utf-8'))
