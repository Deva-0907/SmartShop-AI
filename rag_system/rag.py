import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

class SimpleRAG:
    """Minimal RAG with FAISS"""
    
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.texts = []
        self.load_or_create()
    
    def load_or_create(self):
        """Load existing RAG or create sample data"""
        if os.path.exists('faiss_index.bin'):
            self.index = faiss.read_index('faiss_index.bin')
            with open('texts.json', 'r') as f:
                self.texts = json.load(f)
            print(f"✅ Loaded {len(self.texts)} spending records")
        else:
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create 20 sample spending records"""
        data = [
            {"category": "Groceries", "item": "Rice 5kg", "amount": 1200},
            {"category": "Groceries", "item": "Chicken 1kg", "amount": 850},
            {"category": "Groceries", "item": "Vegetables", "amount": 600},
            {"category": "Groceries", "item": "Milk 1L", "amount": 350},
            {"category": "Groceries", "item": "Bread", "amount": 250},
            {"category": "Groceries", "item": "Oil 1L", "amount": 600},
            {"category": "Transport", "item": "Bus fare", "amount": 150},
            {"category": "Transport", "item": "Fuel", "amount": 4500},
            {"category": "Transport", "item": "Car maintenance", "amount": 3500},
            {"category": "Shopping", "item": "T-shirt", "amount": 3500},
            {"category": "Shopping", "item": "Shoes", "amount": 8500},
            {"category": "Shopping", "item": "Phone case", "amount": 1200},
            {"category": "Shopping", "item": "Backpack", "amount": 4200},
            {"category": "Food", "item": "Lunch outside", "amount": 600},
            {"category": "Food", "item": "Coffee", "amount": 250},
            {"category": "Food", "item": "Dinner out", "amount": 1200},
            {"category": "Utilities", "item": "Electricity bill", "amount": 3500},
            {"category": "Utilities", "item": "Water bill", "amount": 800},
            {"category": "Entertainment", "item": "Movie ticket", "amount": 800},
            {"category": "Entertainment", "item": "Netflix", "amount": 1200},
        ]
        
    
        self.texts = [f"{d['category']}: {d['item']} - LKR {d['amount']}" for d in data]
        
    
        embeddings = self.embedder.encode(self.texts)
        embeddings_np = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings_np)
        
    
        self.index = faiss.IndexFlatIP(384)
        self.index.add(embeddings_np)
        
    
        faiss.write_index(self.index, 'faiss_index.bin')
        with open('texts.json', 'w') as f:
            json.dump(self.texts, f)
        
        print(f" Created RAG with {len(self.texts)} spending records")
    
    def retrieve(self, query, k=3):
        """Search for relevant spending records"""
        if self.index is None:
            return ["No spending data available"]
        
    
        query_embed = self.embedder.encode([query])
        query_np = np.array(query_embed).astype('float32')
        faiss.normalize_L2(query_np)
        
        scores, indices = self.index.search(query_np, k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.texts) and score > 0.1:
                results.append(self.texts[idx])
        
        return results if results else ["No relevant spending found"]