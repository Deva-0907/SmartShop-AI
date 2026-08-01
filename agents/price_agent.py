from models import Models
import json

class PriceAgent:
    """Agent 1: Finds products and prices (uses Groq)"""
    
    def __init__(self):
        self.model = Models.get_groq()
    
    def search(self, query):
        """Search for products and prices"""
        
        # Step 1: Extract product name
        extract_prompt = f"Extract the product name from this query. Return ONLY the product name: '{query}'"
        product_response = self.model.invoke(extract_prompt)
        product = product_response.content.strip()
        
        # Step 2: Simulate scraping (real demo with sample data)
        # In production, you'd use BeautifulSoup here
        sample_products = {
            "phone": [
                {"name": "Samsung Galaxy A15", "price": 48500, "store": "Daraz"},
                {"name": "Xiaomi Redmi Note 13", "price": 42500, "store": "Daraz"},
                {"name": "Samsung Galaxy A15", "price": 49900, "store": "Kapruka"},
            ],
            "laptop": [
                {"name": "Lenovo ThinkPad", "price": 125000, "store": "Daraz"},
                {"name": "HP Pavilion", "price": 98000, "store": "Kapruka"},
            ],
            "headphones": [
                {"name": "Sony WH-1000XM4", "price": 45000, "store": "Daraz"},
                {"name": "JBL Tune 500", "price": 8500, "store": "Kapruka"},
            ]
        }
        
        # Find matching products
        products = []
        for key, items in sample_products.items():
            if key in product.lower() or product.lower() in key:
                products.extend(items)
        
        # If no match, return generic products
        if not products:
            products = [
                {"name": "Generic Product", "price": 5000, "store": "Daraz"},
                {"name": "Generic Product", "price": 5500, "store": "Kapruka"},
            ]
        
        # Step 3: Analyze and recommend
        products_text = "\n".join([f"- {p['name']}: LKR {p['price']} ({p['store']})" for p in products])
        
        analyze_prompt = f"""
        User wants: "{query}"
        
        Products found:
        {products_text}
        
        Provide:
        1. The cheapest product
        2. Best value recommendation
        3. A short recommendation
        
        Keep it brief (max 3 sentences).
        """
        
        recommendation = self.model.invoke(analyze_prompt)
        
        return {
            "product": product,
            "products": products,
            "recommendation": recommendation.content,
            "cheapest": min(products, key=lambda x: x['price']) if products else None
        }