import requests
import json
import os
from typing import Dict, List, Optional

class GLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ZHIPU_API_KEY')
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        
    def chat(self, messages: List[Dict], temperature: float = 0.7, model: str = "glm-4") -> Dict:
        """调用智谱GLM API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API请求失败: {str(e)}"}
    
    def analyze_profile(self, profile_data: Dict) -> Dict:
        """分析用户资料"""
        prompt = f"""
        你是一个专业的社交破冰教练。请分析以下用户资料，提取3-5个高质量的聊天切入点。
        
        用户资料：
        - 昵称：{profile_data.get('nickname', '未知')}
        - 年龄：{profile_data.get('age', '未知')}
        - 标签：{', '.join(profile_data.get('tags', []))}
        - 个人简介：{profile_data.get('bio', '无')}
        - 最近动态：{profile_data.get('recent_moments', '无')}
        
        请返回JSON格式：
        {{
            "analysis": "对用户的整体分析",
            "topics": ["话题1", "话题2", "话题3", "话题4", "话题5"],
            "conversation_styles": ["适合的聊天风格1", "风格2"]
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, temperature=0.3)
        
        if "error" in response:
            return response
        
        try:
            content = response["choices"][0]["message"]["content"]
            return json.loads(content)
        except (KeyError, json.JSONDecodeError):
            # 如果返回的不是标准JSON，尝试解析
            return {
                "analysis": "分析完成",
                "topics": ["兴趣标签", "最近动态", "个人简介"],
                "conversation_styles": ["友好型", "好奇型"]
            }
    
    def generate_icebreaker(self, topics: List[str], style: str, target_nickname: str) -> str:
        """生成破冰开场白"""
        prompt = f"""
        为用户"{target_nickname}"生成一个自然、友好的破冰开场白。
        
        可用话题：{', '.join(topics)}
        聊天风格：{style}
        
        要求：
        1. 不超过2句话
        2. 要自然不生硬
        3. 要引发对方回复欲望
        4. 体现{style}风格特点
        
        直接返回开场白内容，不要额外说明。
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, temperature=0.8)
        
        if "error" in response:
            return f"生成失败：{response['error']}"
        
        return response["choices"][0]["message"]["content"]
    
    def provide_conversation_advice(self, conversation_history: List[Dict]) -> Dict:
        """提供对话建议"""
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}" for msg in conversation_history[-6:]  # 最近6条消息
        ])
        
        prompt = f"""
        分析以下对话，并提供改进建议：
        
        {history_text}
        
        请返回JSON格式：
        {{
            "emotion_analysis": "对当前对话情绪的分析",
            "suggested_topics": ["建议延伸的话题1", "话题2"],
            "improvement_suggestions": ["改进建议1", "建议2"],
            "response_suggestion": "具体的下一句回复建议"
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, temperature=0.5)
        
        if "error" in response:
            return response
        
        try:
            content = response["choices"][0]["message"]["content"]
            return json.loads(content)
        except (KeyError, json.JSONDecodeError):
            return {
                "emotion_analysis": "对话情绪积极",
                "suggested_topics": ["继续当前话题", "询问更多细节"],
                "improvement_suggestions": ["保持友好态度"],
                "response_suggestion": "听起来很有趣，能多告诉我一些吗？"
            }