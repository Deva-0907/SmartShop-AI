from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config import GROQ_API_KEY, OPENROUTER_API_KEY

class Models:
    """Simple model router"""
    
    @staticmethod
    def get_groq():
        """Fast model for price agent"""
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
    
    @staticmethod
    def get_openrouter():
        """Smart model for budget agent"""
        return ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="gpt-4o-mini",
            temperature=0.5
        )