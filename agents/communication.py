class AgentCommunicator:
    """Simple message passing between agents"""
    
    @staticmethod
    def send_message(from_agent, to_agent, data):
        """Send structured message from one agent to another"""
        message = {
            "from": from_agent,
            "to": to_agent,
            "data": data
        }
        return message
    
    @staticmethod
    def process_handoff(price_result, user_query):
        """Price Agent hands off product data to Budget Agent"""
        

        product_info = {
            "name": price_result.get("product", "unknown product"),
            "cheapest_price": price_result["cheapest"]["price"] if price_result.get("cheapest") else 0,
            "all_products": price_result.get("products", []),
            "recommendation": price_result.get("recommendation", "")
        }
        
        handoff = {
            "type": "PRICE_DATA_HANDOFF",
            "from": "PriceAgent",
            "to": "BudgetAgent",
            "product_info": product_info,
            "user_query": user_query
        }
        
        return handoff