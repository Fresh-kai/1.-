# SoulConnect Coach - 智能社交破冰教练

## 项目简介

SoulConnect Coach 是一个基于AI的智能社交破冰教练应用，专为帮助用户在社交平台上建立更自然、深入的连接而设计。通过分析用户资料、生成个性化开场白和提供实时对话建议，让每次社交互动都充满温度和效率。

## 核心功能

- **智能用户分析**：深度解析用户资料，挖掘兴趣点
- **智能破冰建议**：多风格开场白生成，情境化建议
- **对话模拟练习**：真实场景模拟，实时反馈指导
- **社交技能培养**：进步追踪，技能评估，个性化训练

## 环境要求

- Python 3.8 或更高版本
- 稳定的互联网连接
- 智谱AI API密钥

## 安装步骤

### 1. 下载项目文件
确保你的项目目录包含以下文件：
```
soulconnect-coach/
├── app.py
├── requirements.txt
├── utils/
│   ├── __init__.py
│   ├── glm_client.py
│   └── emotion_analyzer.py
└── assets/
    └── style.css
```

### 2. 安装Python依赖
打开命令提示符，进入项目目录，运行：
```bash
pip install -r requirements.txt
```

如果安装缓慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 配置API密钥
在项目根目录创建 `.env` 文件，内容如下：
```
ZHIPU_API_KEY=你的智谱API密钥
```

将"你的智谱API密钥"替换为你在智谱平台获取的实际密钥。

### 4. 运行应用
在项目目录中运行：
```bash
streamlit run app.py
```

### 5. 访问应用
浏览器会自动打开，或者手动访问：`http://localhost:8501`

## 使用指南

### 首次使用步骤：
1. 在左侧边栏选择一个目标用户
2. 点击"分析此用户"按钮
3. 查看分析结果和推荐话题
4. 选择合适的聊天风格
5. 生成个性化开场白
6. 在对话模拟器中练习交流技巧

### 功能区域说明：
- **左侧面板**：用户选择、资料卡片、进度看板
- **主内容区**：用户分析、破冰建议、对话练习三个标签页
- **用户分析**：显示用户画像分析和推荐话题
- **破冰建议**：根据选择的风格生成开场白
- **对话练习**：模拟真实对话场景，提供实时建议

## 故障排除

### 常见问题解决：

**问题1：ModuleNotFoundError**
解决：重新安装依赖
```bash
pip install streamlit requests python-dotenv pandas plotly numpy
```

**问题2：端口被占用**
解决：使用其他端口
```bash
streamlit run app.py --server.port=8502
```

**问题3：编码错误**
解决：确保CSS文件使用UTF-8编码保存

**问题4：API密钥错误**
解决：检查.env文件中的密钥是否正确，确保没有多余空格

**问题5：浏览器没有自动打开**
解决：手动访问 `http://localhost:8501`

## 项目结构说明

```
soulconnect-coach/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖列表
├── .env                  # 环境配置文件（需要自己创建）
├── utils/                # 工具模块目录
│   ├── glm_client.py     # 智谱API调用模块
│   └── emotion_analyzer.py # 情感分析模块
└── assets/               # 资源文件目录
    └── style.css         # 界面样式文件
```

## 技术架构

- **前端框架**：Streamlit
- **后端语言**：Python 3.8+
- **AI模型**：智谱GLM大模型
- **数据处理**：Pandas, Plotly
- **环境管理**：python-dotenv

## 获取API密钥

如果还没有智谱API密钥，请按以下步骤获取：

1. 访问 https://open.bigmodel.cn/
2. 注册账号并完成实名认证
3. 进入控制台，创建API密钥
4. 复制密钥到.env文件中

## 注意事项

- API调用会产生费用，新用户通常有免费额度
- 确保网络稳定，能够访问智谱API
- 不要将.env文件提交到代码仓库，避免密钥泄露
- 如果遇到问题，检查终端中的错误信息

## 联系方式

如有问题，请检查：
1. 终端中的具体错误信息
2. API密钥是否正确配置
3. 网络连接是否正常

---

**让每次对话都有温度** - SoulConnect Coach 你的智能社交破冰教练