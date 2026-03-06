# 微信公众号AI文章自动生成工具

通过元宝或豆包API自动生成AI科技热点文章,并创建微信公众号草稿。

## 功能特性

- 🤖 支持多种AI提供商(豆包、元宝)
- 📝 自动生成当日AI科技热点文章
- 📤 自动创建微信公众号草稿
- ⚙️ 可配置文章分类和字数
- 💾 本地保存生成的文章

## 项目结构

```
wechattext/
├── main.py              # 主程序入口
├── ai_generator.py      # AI内容生成模块
├── weixin_client.py     # 微信公众号API客户端
├── config.json          # 配置文件
├── requirements.txt     # Python依赖
├── .env.example         # 环境变量示例
└── README.md            # 项目说明文档
```

## 安装步骤

### 1. 克隆或下载项目

```bash
cd /Users/zora/Documents/Work/mygithub/wechattext
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

#### 方式一: 修改 `config.json`

```json
{
  "weixin": {
    "appid": "你的微信公众号AppID",
    "secret": "你的微信公众号AppSecret"
  },
  "ai_provider": "doubao",
  "doubao": {
    "api_key": "你的豆包API密钥",
    "model": "doubao-pro-32k",
    "api_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
  },
  "yuanbao": {
    "api_key": "你的元宝API密钥",
    "model": "yuanbao-turbo",
    "api_url": "https://api.yuanbao.tencent.com/v1/chat/completions"
  },
  "article": {
    "max_words": 2000,
    "category": "AI科技"
  }
}
```

#### 方式二: 使用环境变量

```bash
cp .env.example .env
# 编辑 .env 文件,填入你的API密钥
```

### 4. 获取微信公众号凭证

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「开发」→「基本配置」
3. 记录 `AppID` 和 `AppSecret`

## 使用方法

### 基本使用

```bash
python main.py
```

### 自定义参数

```bash
# 指定文章分类
python main.py --category "人工智能"

# 指定字数
python main.py --words 1500

# 组合使用
python main.py --category "AI科技" --words 1800
```

### 命令行参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--category` | `-c` | 文章分类 | `--category "AI科技"` |
| `--words` | `-w` | 最大字数 | `--words 2000` |
| `--config` | - | 配置文件路径 | `--config my_config.json` |

## 工作流程

1. **生成文章**: 使用AI API生成当日热点文章内容
2. **本地保存**: 将文章保存到 `output/article_YYYYMMDD.md`
3. **获取Token**: 从微信API获取access_token
4. **格式转换**: 将Markdown转换为HTML格式
5. **创建草稿**: 在微信公众号草稿箱中创建新草稿
6. **查看草稿**: 显示当前草稿箱中的文章列表

## 注意事项

### 关于封面图

- 首次使用时,`thumb_media_id` 需要手动设置
- 需要先上传图片到微信公众号素材库获取media_id
- 当前版本创建的草稿默认不显示封面,需要在后台手动添加

### AI API配置

#### 豆包API

- 官网: https://www.volcengine.com/
- 文档: https://www.volcengine.com/docs/82379
- 需要申请API Key

#### 元宝API

- 官网: https://cloud.tencent.com/
- 文档: https://cloud.tencent.com/document/product/269/90760
- 需要开通腾讯云API服务

### 微信公众号API限制

- access_token 有效期为2小时,程序会自动获取
- 调用频率限制请参考微信官方文档
- 需要微信公众号已认证

## 常见问题

### Q1: 提示"获取access_token失败"

A: 检查 `config.json` 中的 `appid` 和 `secret` 是否正确

### Q2: 提示"AI API请求失败"

A: 检查API密钥是否正确,网络是否正常

### Q3: 草稿创建成功但没有封面图

A: 需要先上传图片到微信公众号素材库,获取media_id后更新配置

### Q4: 如何查看生成的文章

A: 
1. 本地文件: `output/article_YYYYMMDD.md`
2. 微信公众号后台: 「素材管理」→「草稿箱」

## 依赖说明

```
requests>=2.31.0       # HTTP请求库
python-dotenv>=1.0.0   # 环境变量管理
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!
