from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>心语伴 - 情感陪伴助手</title>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; min-height: 100vh;
        }
        .container {
            max-width: 800px; margin: 0 auto; background: white;
            border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #667eea; font-size: 2.5em; }
        .demo-section { background: #f8f9fa; border-radius: 15px; padding: 25px; margin: 20px 0; }
        .btn {
            display: inline-block; background: #667eea; color: white; padding: 12px 25px;
            border-radius: 25px; text-decoration: none; margin: 10px 5px; transition: all 0.3s;
        }
        .btn:hover { background: #5a6fd8; transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💫 心语伴 - 智能情感陪伴助手</h1>
            <p>你的未来搭子 - 24小时情感支持伙伴</p>
        </div>
        
        <div class="demo-section">
            <h2>🎯 核心功能演示</h2>
            <div style="background: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
                <div style="background: #007bff; color: white; padding: 12px; border-radius: 10px; margin: 8px 0 8px auto; max-width: 70%; text-align: right;">
                    我今天感觉有点焦虑
                </div>
                <div style="background: #e9ecef; padding: 12px; border-radius: 10px; margin: 8px 0; max-width: 70%;">
                    感受到你的焦虑了，我在这里陪伴你。试试深呼吸练习？ 🌿
                </div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="https://huggingface.co/spaces/Fresh-k/1" class="btn">🚀 体验完整版应用</a>
            <a href="https://github.com/fresh-kai/1" class="btn">📁 查看源代码</a>
        </div>
        
        <div class="demo-section">
            <h3>🎨 技术特色</h3>
            <ul style="line-height: 1.8;">
                <li>🤖 基于智谱GLM-4大语言模型</li>
                <li>💝 智能情感分析与陪伴</li>
                <li>📊 个性化活动推荐系统</li>
                <li>🧘 正念练习与情绪管理</li>
                <li>🎯 用户画像与长期记忆</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
