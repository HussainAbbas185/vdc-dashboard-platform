
import pandas as pd
import random
import time
import requests
import streamlit as st
from datetime import datetime

def get_global_market_pulse():
    metrics = {
        "global_internet_traffic_pb": round(random.uniform(150, 200), 2),
        "active_ai_agents_b": round(random.uniform(1.2, 5.0), 3),
        "cyber_threat_level": random.choice(["Low", "Moderate", "High", "Critical"]),
        "crypto_market_cap_t": round(random.uniform(2.1, 3.5), 2),
        "cloud_compute_usage_pct": round(random.uniform(65, 92), 1)
    }
    topics = [
        {"topic": "Generative AI", "growth": "+450%", "sentiment": "Bullish"},
        {"topic": "Quantum Computing", "growth": "+120%", "sentiment": "Neutral"},
        {"topic": "Edge Computing", "growth": "+85%", "sentiment": "Bullish"},
        {"topic": "Cybersecurity Mesh", "growth": "+200%", "sentiment": "Bearish"},
        {"topic": "Green Tech", "growth": "+300%", "sentiment": "Bullish"},
        {"topic": "6G Networks", "growth": "+60%", "sentiment": "Speculative"}
    ]
    return metrics, pd.DataFrame(topics)

def get_mining_suggestions(df):
    return ["⛏️ Text Mining: Entity Extraction", "🔍 Cluster Analysis: Pattern Discovery"]

def get_tech_news():
    """
    Returns a list of tech news articles with GUARANTEED high-uptime Unsplash IDs.
    All images use production-grade query parameters for reliability.
    """
    articles = [
        {
            "id": "q-leap",
            "title": "Quantum Leap: New Processor Breaks Encryption Barriers",
            "source": "TechCrunch",
            "time": "2 hrs ago",
            "category": "Hardware",
            "sentiment": 0.8,
            "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&q=80&w=1080",
            "summary": "Researchers achieve quantum supremacy with a new 1000-qubit cooling system, redefining secure communications.",
            "content": """
            ### The Dawn of Quantum Utility
            Researchers at the Global Quantum Institute have unveiled 'Project Frost', a 1000-qubit quantum processor that operates at temperatures near absolute zero with unprecedented stability. 
            
            This breakthrough allows the processor to maintain coherence for minutes rather than milliseconds, enabling it to perform complex cryptographic calculations that would take traditional supercomputers thousands of years.
            
            #### Key Takeaways:
            - **Coherence Time:** Improved by 500x.
            - **Error Correction:** New hardware-level parity checks implemented.
            - **Implications:** Future-proofing encryption is now an urgent priority for global banks and security agencies.
            """
        },
        {
            "id": "ai-surge",
            "title": "Market Watch: AI Stocks Surge as Adoption Hits 40%",
            "source": "Bloomberg",
            "time": "4 hrs ago",
            "category": "Finance",
            "sentiment": 0.9,
            "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1080",
            "summary": "Global enterprise adoption of GenAI has doubled in Q1, driving record highs in semiconductor evaluations.",
            "content": """
            ### The AI Supercycle Continues
            Wall Street is buzzing as quarterly reports from major tech firms indicate a massive shift in capital expenditure towards AI infrastructure. 
            
            GenAI is no longer just a 'pilot' program; it is being integrated into core workflows across finance, legal, and manufacturing sectors.
            
            #### Market Indicators:
            - **Semi Index:** Up 12% week-over-week.
            - **Cloud Capex:** Projected to hit $200B this year.
            - **Efficiency:** Early adopters report 25% reduction in operational costs.
            """
        },
        {
            "id": "zero-click",
            "title": "Cybersecurity Alert: New 'Zero-Click' Exploit Found",
            "source": "Wired",
            "time": "5 hrs ago",
            "category": "Security",
            "sentiment": -0.7,
            "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1080",
            "summary": "A critical vulnerability in mobile OS kernels allows attackers to execute code without user interaction.",
            "content": """
            ### Invisible Threats
            Security firm 'DeepPulse' discovered a vulnerability named 'PhantomRing' that exploits the way mobile devices handle Bluetooth handshakes. 
            
            Unlike traditional phishing, the victim does not need to click a link or open a file. Simply having Bluetooth enabled in a public space could expose the device's kernel to remote code execution.
            
            #### Risk Assessment:
            - **Affected Devices:** Estimated 2.1 billion smartphones.
            - **Difficulty:** High; requires specialized proximity hardware.
            """
        },
        {
            "id": "green-dc",
            "title": "Green Energy: Data Centers Aim for Carbon Neutrality by 2028",
            "source": "Reuters",
            "time": "6 hrs ago",
            "category": "Infrastructure",
            "sentiment": 0.6,
            "image": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&q=80&w=1080",
            "summary": "Major cloud providers pledge to power 90% of global infrastructure with renewables within four years.",
            "content": """
            ### Sustainable Scaling
            As the demand for AI compute explodes, so does the energy consumption of data centers. To combat the rising carbon footprint, the 'Big Five' cloud giants have formed the 'Green Cloud Coalition'.
            
            #### Strategic Initiatives:
            - **Nuclear Power:** Investment in Small Modular Reactors (SMRs).
            - **Cooling:** Transitioning to liquid immersion cooling to reduce HVAC load by 40%.
            """
        },
        {
            "id": "starship",
            "title": "SpaceX Success: Starship Orbit Achieved",
            "source": "SpaceNews",
            "time": "12 hrs ago",
            "category": "Space Tech",
            "sentiment": 0.95,
            "image": "https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&q=80&w=1080",
            "summary": "The massive heavy-lift vehicle successfully completed a full orbital insertion, paving the way for lunar missions.",
            "content": """
            ### To the Moon and Beyond
            In a historic flight from Starbase, Texas, the integrated Starship flight system successfully reached orbital velocity and performed a controlled de-orbit burn over the Indian Ocean.
            
            #### Mission Highlights:
            - **Payload Capacity:** Confirmed 100+ tons to LEO.
            - **Recovery:** Booster perform successful 'catch' maneuver at the launch site.
            """
        },
        {
            "id": "robotics",
            "title": "Robotics: Humanoid Pilots Begin Testing in Logistics Hubs",
            "source": "IEEE Spectrum",
            "time": "1 day ago",
            "category": "Robotics",
            "sentiment": 0.85,
            "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=1080",
            "summary": "New bipedal robots equipped with multimodal LLMs are now performing unstructured tasks in warehouses.",
            "content": """
            ### The Labour Force of the Future
            A startup backed by major e-commerce players has deployed 50 humanoid robots in a pilot program in Nevada. These robots don't just follow pre-programmed paths; they use vision-language models to understand verbal instructions.
            
            #### Features:
            - **End-to-End Learning:** Can learn new physical tasks by watching human demonstrations.
            - **Safety:** Collaborative skin sensors detect human presence within 1ms.
            """
        }
    ]
    return articles

@st.cache_data(ttl=3600)
def get_live_tech_news(api_key):
    """
    Fetches real-time technology news from NewsAPI.org.
    Normalizes the data to match the VDC Intelligence format.
    """
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") != "ok":
            return None # Handle error in dashboard
            
        articles = []
        for i, item in enumerate(data.get("articles", [])[:12]): # Limit to 12 articles
            articles.append({
                "id": f"live-{i}",
                "title": item.get("title", "Classified Intel"),
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "time": item.get("publishedAt", "Recent")[:10], # Extract YYYY-MM-DD
                "category": "Live Intelligence",
                "sentiment": round(random.uniform(-0.5, 0.9), 2), # Simulated sentiment for live data
                "image": item.get("urlToImage") or "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800",
                "summary": item.get("description", "No summary available for this encrypted feed."),
                "content": f"### {item.get('title')}\n\n**Source:** {item.get('source', {}).get('name')}\n\n{item.get('content', 'Full content restricted to source terminal.')}\n\n[Read Original Report]({item.get('url')})"
            })
        return articles
    except Exception as e:
        print(f"API Fetch Failure: {e}")
        return None
