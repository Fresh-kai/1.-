import re
from typing import Dict, List

class EmotionAnalyzer:
    """简单的情感分析器（在实际项目中可以使用专业的NLP模型）"""
    
    def __init__(self):
        self.positive_words = {
            '开心', '高兴', '喜欢', '爱', '棒', '好', '优秀', '完美', '精彩',
            '有趣', '厉害', '惊喜', '幸福', '满意', '赞成', '支持', '感谢'
        }
        self.negative_words = {
            '讨厌', '烦', '生气', '愤怒', '失望', '伤心', '难过', '糟糕',
            '差', '烂', '讨厌', '恨', '抱怨', '批评', '反对', '拒绝'
        }
    
    def analyze_text_emotion(self, text: str) -> Dict:
        """分析文本情感"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        # 检测表情符号
        emoji_positive = len(re.findall(r'[😀-😍👍❤️💕🌟🎉]', text))
        emoji_negative = len(re.findall(r'[😠-😩👎💔😢]', text))
        
        total_positive = positive_count + emoji_positive
        total_negative = negative_count + emoji_negative
        
        if total_positive > total_negative:
            emotion = "positive"
            score = min(1.0, total_positive / 10)
        elif total_negative > total_positive:
            emotion = "negative" 
            score = min(1.0, total_negative / 10)
        else:
            emotion = "neutral"
            score = 0.5
        
        return {
            "emotion": emotion,
            "score": round(score, 2),
            "positive_indicators": total_positive,
            "negative_indicators": total_negative
        }
    
    def analyze_conversation_flow(self, conversation: List[Dict]) -> Dict:
        """分析对话流程"""
        if len(conversation) < 2:
            return {"status": "刚刚开始", "suggestion": "继续当前话题"}
        
        recent_messages = conversation[-4:]
        questions_count = sum(1 for msg in recent_messages if '?' in msg.get('content', ''))
        
        if questions_count == 0:
            return {
                "status": "话题可能停滞",
                "suggestion": "尝试提问来延续对话"
            }
        elif questions_count >= 2:
            return {
                "status": "积极交流中", 
                "suggestion": "保持当前节奏"
            }
        else:
            return {
                "status": "正常交流",
                "suggestion": "平衡提问和分享"
            }