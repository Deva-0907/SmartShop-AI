from models import Models
from rag_system.rag import SimpleRAG

class BudgetAgent:
    """Agent 2: Analyzes budget and spending (uses OpenRouter)"""
    
    def __init__(self):
        self.model = Models.get_openrouter()
        self.rag = SimpleRAG()
    
    def analyze(self, query, product_info=None):
        """Analyze spending and give budget advice"""
        
        context = self.rag.retrieve(query)
        context_text = "\n".join(context)
        
        
        if product_info:
            prompt = f"""
            You are a budget advisor. The user wants to buy:
            {product_info}
            
            Their spending history:
            {context_text}
            
            User's question: "{query}"
            
            Provide:
            1. Is this purchase affordable based on their spending?
            2. How much they typically spend on {product_info}
            3. Quick budget tip
            
            Keep it short and practical (max 4 sentences).
            """
        else:
            prompt = f"""
            You are a budget advisor. 
            
            User's spending history:
            {context_text}
            
            User's question: "{query}"
            
            Provide specific money-saving advice based on their spending pattern.
            Keep it short and practical (max 4 sentences).
            """
        
        response = self.model.invoke(prompt)
        return response.content