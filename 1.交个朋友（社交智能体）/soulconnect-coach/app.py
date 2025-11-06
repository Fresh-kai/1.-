import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# 导入自定义模块
from utils.glm_client import GLMClient
from utils.emotion_analyzer import EmotionAnalyzer

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="SoulConnect Coach - 智能社交破冰教练",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 加载自定义CSS
def load_css():
    """修复：更安全的CSS加载"""
    try:
        st.markdown("""
        <style>
        .companion-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
        }
        /* 简化其他样式，移除可能冲突的样式 */
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning("样式加载遇到问题，但不影响功能使用")

load_css()

class SoulConnectApp:
    def __init__(self):
        self.glm_client = GLMClient()
        self.emotion_analyzer = EmotionAnalyzer()
        self.initialize_session_state()
    
    def initialize_session_state(self):
    """修复：更安全的会话状态初始化"""
    default_states = {
        'messages': [],
        'user_info_set': False,
        'current_emotion': "未知",
        'conversation_count': 0,
        'last_reset': datetime.now().isoformat()
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-header">
            <h1>💬 SoulConnect Coach</h1>
            <p>你的智能社交破冰教练 - 让每次对话都有温度</p>
        </div>
        """, unsafe_allow_html=True)
    
    def sample_profiles(self):
        """示例用户资料库"""
        return [
            {
                "id": 1,
                "nickname": "音乐爱好者小张",
                "age": 24,
                "tags": ["吉他", "民谣", "旅行", "摄影", "咖啡"],
                "bio": "用音乐记录生活，用脚步丈量世界",
                "recent_moments": "刚刚在丽江古城听到一首超棒的民谣！准备学起来🎵"
            },
            {
                "id": 2, 
                "nickname": "读书人小王",
                "age": 26,
                "tags": ["阅读", "写作", "哲学", "历史", "茶道"],
                "bio": "在书海中寻找智慧，在文字间表达思考",
                "recent_moments": "最近在读《人类简史》，对认知革命有了新的理解📚"
            },
            {
                "id": 3,
                "nickname": "运动达人小李",
                "age": 23,
                "tags": ["篮球", "健身", "跑步", "营养", "健康"],
                "bio": "生命在于运动，健康源于坚持",
                "recent_moments": "今天完成了半马训练，刷新了个人记录！🏃‍♂️"
            },
            {
                "id": 4,
                "nickname": "美食家小赵",
                "age": 25,
                "tags": ["烹饪", "烘焙", "探店", "咖啡", "美食摄影"],
                "bio": "吃货的人生不需要解释，唯美食与爱不可辜负",
                "recent_moments": "发现了一家超赞的意大利餐厅，提拉米苏绝了！🍰"
            }
        ]
    
    def analyze_user_profile(self, profile):
        """分析用户资料"""
        with st.spinner("正在分析用户资料并生成破冰建议..."):
            result = self.glm_client.analyze_profile(profile)
            
            if "error" in result:
                st.error(f"分析失败：{result['error']}")
                return None
            
            st.session_state.analysis_result = result
            st.session_state.current_target = profile
            st.session_state.user_progress["conversations_started"] += 1
            
            return result
    
    def render_profile_analysis(self, analysis_result, profile):
        """渲染资料分析结果"""
        st.subheader(f"📊 用户分析：{profile['nickname']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**用户画像分析：**")
            st.info(analysis_result.get("analysis", "分析完成"))
            
            st.write("**推荐聊天风格：**")
            for style in analysis_result.get("conversation_styles", []):
                st.write(f"• {style}")
        
        with col2:
            st.write("**基础信息：**")
            st.write(f"👤 年龄：{profile.get('age', '未知')}")
            st.write(f"🏷️ 标签：{', '.join(profile.get('tags', []))}")
    
    def render_topic_suggestions(self, analysis_result):
        """渲染话题建议"""
        st.subheader("💡 推荐话题")
        
        topics = analysis_result.get("topics", [])
        for i, topic in enumerate(topics[:5], 1):
            st.write(f"{i}. {topic}")
        
        # 话题选择
        selected_topic = st.selectbox(
            "选择你想要深入的话题：",
            options=topics,
            key="selected_topic"
        )
        
        return selected_topic
    
    def render_icebreaker_generator(self, analysis_result, profile, selected_topic):
        """渲染破冰生成器"""
        st.subheader("🎯 破冰开场白生成")
        
        # 风格选择
        style_options = analysis_result.get("conversation_styles", ["友好型", "好奇型", "幽默型"])
        selected_style = st.radio(
            "选择聊天风格：",
            options=style_options,
            horizontal=True
        )
        
        if st.button("✨ 生成智能开场白", type="primary"):
            topics_to_use = [selected_topic] + [t for t in analysis_result.get("topics", []) if t != selected_topic][:2]
            
            icebreaker = self.glm_client.generate_icebreaker(
                topics_to_use, 
                selected_style, 
                profile['nickname']
            )
            
            st.markdown("""
            <div class="icebreaker-example">
                <strong>💡 推荐开场白：</strong><br>
            """, unsafe_allow_html=True)
            st.write(icebreaker)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 保存到对话历史
            st.session_state.conversation_history.append({
                "role": "coach",
                "content": f"建议开场白：{icebreaker}",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": "icebreaker"
            })
    
    def render_conversation_simulator(self, profile):
        """渲染对话模拟器"""
        st.subheader("💬 对话模拟练习")
        
        st.write(f"与 **{profile['nickname']}** 的对话练习：")
        
        # 显示对话历史
        for msg in st.session_state.conversation_history[-10:]:  # 显示最近10条
            if msg["role"] == "coach":
                st.chat_message("assistant").write(msg["content"])
            else:
                st.chat_message("user").write(msg["content"])
        
        # 用户输入
        user_input = st.chat_input("在这里输入你的回复...")
        
        if user_input:
            # 添加用户消息到历史
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": "user_message"
            })
            
            # 分析对话并提供建议
            with st.spinner("正在分析对话..."):
                advice = self.glm_client.provide_conversation_advice(
                    st.session_state.conversation_history
                )
                
                if "error" not in advice:
                    # 显示建议
                    st.markdown("""
                    <div class="advice-card">
                        <strong>🤔 对话建议：</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**情绪分析：**")
                        st.write(advice.get("emotion_analysis", "分析中..."))
                        
                        st.write("**改进建议：**")
                        for suggestion in advice.get("improvement_suggestions", []):
                            st.write(f"• {suggestion}")
                    
                    with col2:
                        st.write("**推荐话题：**")
                        for topic in advice.get("suggested_topics", []):
                            st.write(f"• {topic}")
                        
                        st.write("**回复建议：**")
                        st.info(advice.get("response_suggestion", ""))
    
    def render_progress_dashboard(self):
        """渲染进度看板"""
        st.sidebar.subheader("📈 你的社交进步")
        
        progress = st.session_state.user_progress
        
        col1, col2, col3 = st.sidebar.columns(3)
        
        with col1:
            st.metric("开启对话", progress["conversations_started"])
        
        with col2:
            st.metric("成功破冰", progress["successful_icebreakers"])
        
        with col3:
            st.metric("对话评分", "8.5/10")
        
        # 技能雷达图数据
        skills_data = {
            "技能类型": ["话题开启", "情绪感知", "对话延续", "深度连接", "幽默感"],
            "当前水平": [8, 7, 6, 5, 7],
            "目标水平": [9, 8, 8, 7, 8]
        }
        
        df = pd.DataFrame(skills_data)
        fig = px.line_polar(df, r='当前水平', theta='技能类型', 
                           line_close=True, title="社交技能雷达图")
        st.sidebar.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        """运行主应用"""
        self.render_header()
        self.render_progress_dashboard()
        
        # 侧边栏 - 选择目标用户
        st.sidebar.subheader("👥 选择练习对象")
        sample_profiles = self.sample_profiles()
        
        selected_profile_id = st.sidebar.selectbox(
            "选择目标用户：",
            options=[p["id"] for p in sample_profiles],
            format_func=lambda x: next(p["nickname"] for p in sample_profiles if p["id"] == x)
        )
        
        selected_profile = next(p for p in sample_profiles if p["id"] == selected_profile_id)
        
        # 显示用户资料卡
        st.sidebar.markdown("""
        <div class="profile-card">
            <strong>用户资料卡</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.write(f"**昵称：** {selected_profile['nickname']}")
        st.sidebar.write(f"**年龄：** {selected_profile.get('age', '未知')}")
        st.sidebar.write(f"**标签：** {', '.join(selected_profile.get('tags', []))}")
        st.sidebar.write(f"**简介：** {selected_profile.get('bio', '')}")
        st.sidebar.write(f"**最近动态：** {selected_profile.get('recent_moments', '')}")
        
        # 分析按钮
        if st.sidebar.button("🔍 分析此用户", type="secondary"):
            self.analyze_user_profile(selected_profile)
        
        # 主内容区
        if st.session_state.analysis_result and st.session_state.current_target:
            analysis_result = st.session_state.analysis_result
            current_target = st.session_state.current_target
            
            # 创建标签页
            tab1, tab2, tab3 = st.tabs(["📊 用户分析", "🎯 破冰建议", "💬 对话练习"])
            
            with tab1:
                self.render_profile_analysis(analysis_result, current_target)
            
            with tab2:
                selected_topic = self.render_topic_suggestions(analysis_result)
                self.render_icebreaker_generator(analysis_result, current_target, selected_topic)
            
            with tab3:
                self.render_conversation_simulator(current_target)
        
        else:
            # 欢迎页面
            st.info("👈 请在左侧边栏选择一个目标用户，然后点击『分析此用户』开始使用")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 核心功能")
                st.write("""
                - **智能资料分析**：深度解析用户资料，发现聊天切入点
                - **个性化破冰建议**：根据不同风格生成自然开场白
                - **实时对话辅导**：在对话中提供实时建议和改进方向
                - **社交技能培养**：记录进步，提升整体社交能力
                """)
            
            with col2:
                st.subheader("🚀 使用指南")
                st.write("""
                1. 在左侧选择目标用户
                2. 点击「分析此用户」获取破冰建议
                3. 选择合适的聊天风格生成开场白
                4. 在对话模拟器中练习交流技巧
                5. 查看分析报告，持续改进社交技能
                """)

# 运行应用
if __name__ == "__main__":
    app = SoulConnectApp()

    app.run()

