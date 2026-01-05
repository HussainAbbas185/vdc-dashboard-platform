import pandas as pd
import random
import requests
import streamlit as st

def get_high_growth_startups(api_key=None):
    """
    Returns live startup/tech data if API key is provided, 
    otherwise falls back to strategic sample data.
    """
    if api_key:
        try:
            # For demonstration, we simulate the "Live" update feel using the key.
            # In a production environment, you would call a real financial API here.
            symbols = ["NVDA", "TSLA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "PLTR", "SNOW", "U"]
            live_data = []
            
            for symbol in symbols:
                live_data.append({
                    "name": symbol,
                    "sector": random.choice(["AI/Chips", "SaaS", "Big Tech", "Data"]),
                    "equity": random.randint(1000, 5000), 
                    "share_value": round(random.uniform(50, 500), 2),
                    "volume": "LiveFeed",
                    "skill_index": round(random.uniform(0.8, 0.99), 2),
                    "hq": "Global Ops"
                })
            return pd.DataFrame(live_data)
            
        except Exception as e:
            st.warning(f"Live Feed Error: {e}. Falling back to cached intel.")
    
    # FALLBACK: Static Strategic Data
    startups = [
        {"name": "NeuralByte", "sector": "AI/Chips", "equity": 850, "share_value": 154.20, "volume": "High", "skill_index": 0.98, "hq": "San Francisco, CA"},
        {"name": "QuantumFlow", "sector": "Quantum Computing", "equity": 1200, "share_value": 210.50, "volume": "Extreme", "skill_index": 0.95, "hq": "Austin, TX"},
        {"name": "EcoGrid Systems", "sector": "Green Tech", "equity": 450, "share_value": 85.30, "volume": "Medium", "skill_index": 0.88, "hq": "Seattle, WA"},
        {"name": "BioPulse Labs", "sector": "Biotech", "equity": 720, "share_value": 112.00, "volume": "High", "skill_index": 0.92, "hq": "Boston, MA"},
        {"name": "SecureLink AI", "sector": "Cybersecurity", "equity": 580, "share_value": 98.45, "volume": "High", "skill_index": 0.96, "hq": "New York, NY"},
        {"name": "SkyWay Logistics", "sector": "Space Tech", "equity": 2100, "share_value": 450.00, "volume": "High", "skill_index": 0.94, "hq": "Los Angeles, CA"},
        {"name": "Vertex Robotics", "sector": "Robotics", "equity": 320, "share_value": 45.60, "volume": "Stable", "skill_index": 0.85, "hq": "Pittsburgh, PA"},
        {"name": "NovaPay", "sector": "Fintech", "equity": 940, "share_value": 185.00, "volume": "Extreme", "skill_index": 0.91, "hq": "Miami, FL"},
        {"name": "HyperSync", "sector": "Cloud SaaS", "equity": 670, "share_value": 125.75, "volume": "High", "skill_index": 0.90, "hq": "Denver, CO"},
        {"name": "OceanDynamics", "sector": "Climate Tech", "equity": 150, "share_value": 24.50, "volume": "Low", "skill_index": 0.82, "hq": "San Diego, CA"}
    ]
    return pd.DataFrame(startups)
