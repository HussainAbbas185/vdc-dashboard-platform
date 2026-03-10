
import pandas as pd
import random
import time
import requests
import streamlit as st
import xml.etree.ElementTree as ET
from datetime import datetime

def get_global_market_pulse():
    """
    Returns high-fidelity simulated operational metrics.
    Metrics are semi-stable based on current hour to simulate real-world day/night cycles.
    """
    hour = datetime.now().hour
    # Daytime (9-17) has higher traffic/load
    is_peak = 9 <= hour <= 17
    
    traffic_base = 180 if is_peak else 120
    compute_base = 85 if is_peak else 60
    
    metrics = {
        "global_internet_traffic_pb": round(traffic_base + random.uniform(-10, 10), 2),
        "active_ai_agents_b": round(2.5 + (datetime.now().day / 10) + random.uniform(-0.1, 0.1), 3),
        "cyber_threat_level": "High" if is_peak else "Moderate",
        "crypto_market_cap_t": round(2.8 + random.uniform(-0.05, 0.05), 2),
        "cloud_compute_usage_pct": round(compute_base + random.uniform(-5, 5), 1)
    }
    
    # Purpose: Market focus areas tracking growth sectors
    topics = [
        {"topic": "Generative AI", "growth": "+450%", "sentiment": "Bullish", "impact": "High"},
        {"topic": "Quantum Computing", "growth": "+120%", "sentiment": "Neutral", "impact": "Disruptive"},
        {"topic": "Edge Computing", "growth": "+85%", "sentiment": "Bullish", "impact": "Medium"},
        {"topic": "Cybersecurity Mesh", "growth": "+200%", "sentiment": "Bearish", "impact": "Critical"},
        {"topic": "Green Tech", "growth": "+300%", "sentiment": "Bullish", "impact": "Sustainable"},
        {"topic": "6G Networks", "growth": "+60%", "sentiment": "Speculative", "impact": "Future-Proof"}
    ]
    return metrics, pd.DataFrame(topics)

def get_mining_suggestions(df):
    """Real Logic: Suggest operations based on DataFrame properties."""
    suggestions = []
    if df is None or df.empty:
        return ["📥 Please upload data to receive suggestions."]
        
    cols = df.columns.tolist()
    if any(df[col].dtype == 'object' for col in cols):
        suggestions.append("⛏️ NLP Mining: String detected. Recommend Entity Extraction or Sentiment Analysis.")
    if len(cols) > 5:
        suggestions.append("🔍 Dimensionality Reduction: High column count. Recommend PCA or Feature Selection.")
    if len(df) > 1000:
        suggestions.append("📊 Big Data Sampling: High row count. Recommend stratified sampling for visualization speed.")
    
    if not suggestions:
        suggestions.append("⚡ Standard Analysis: Recommend Correlation Matrix and Distribution Plotting.")
        
    return suggestions

def get_tech_news():
    """
    Attempts to fetch live news from public RSS feeds (Wired, TechCrunch).
    Falls back to curated simulated reports if offline.
    """
    # Try fetching live news first
    live_news = get_live_rss_news()
    if live_news: return live_news

    # Fallback to simulated reports if live fetch fails
    articles = [
        {
            "id": "q-leap",
            "title": "Quantum Supremacy: Core-Link Established",
            "source": "VDC Intel",
            "time": "Real-time",
            "category": "Quantum",
            "sentiment": 0.8,
            "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1080",
            "summary": "Platform Quantum Orchestrator v3.0 successfully routed first batch of NP-Hard instructions to cold-gate simulator.",
            "content": """
            ### Operational Milestone
            The VDC Quantum Layer has achieved a stable 'Cold-Gate' link. This allows the platform to offload classical HPC tasks directly into a simulated Hilbert space.
            """
        },
        {
            "id": "ai-ethics",
            "title": "Autonomous Governance: The New Enterprise Standard",
            "source": "Ethics Board",
            "time": "1 hr ago",
            "category": "AI",
            "sentiment": 0.5,
            "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080",
            "summary": "VDC Neural Controller implements new safety guardrails for autonomous data center management.",
            "content": "Full report encrypted."
        }
    ]
    return articles

@st.cache_data(ttl=1800) # Fast refresh for live news
def get_live_rss_news():
    """
    Fetches real-time technology news from public RSS feeds using ElementTree.
    """
    urls = [
        "https://www.wired.com/feed/rss",
        "https://techcrunch.com/feed/"
    ]
    
    all_articles = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200: continue
            
            # Simple XML parsing
            root = ET.fromstring(response.text)
            
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text if item.find('title') is not None else "Unknown Intel"
                link = item.find('link').text if item.find('link') is not None else "#"
                desc = item.find('description').text if item.find('description') is not None else "No summary available."
                pub = item.find('pubDate').text if item.find('pubDate') is not None else "Recent"
                cat = item.find('category').text if item.find('category') is not None else "Technology"
                
                # Try to find media thumbnail or content
                image = "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800"
                media_ns = "{http://search.yahoo.com/mrss/}"
                thumbnail = item.find(f'{media_ns}thumbnail')
                if thumbnail is not None:
                    image = thumbnail.get('url')
                
                all_articles.append({
                    "id": f"rss-{random.randint(1000, 9999)}",
                    "title": title,
                    "source": "Live RSS",
                    "time": pub[5:16] if len(pub) > 16 else pub,
                    "category": cat,
                    "sentiment": round(random.uniform(0.3, 0.9), 2),
                    "image": image,
                    "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                    "content": f"### {title}\n\n{desc}\n\n[Read Full Intel Report]({link})"
                })
        except Exception as e:
            continue
            
    if not all_articles: return None
    
    # Sort and return
    random.shuffle(all_articles)
    return all_articles[:15]

@st.cache_data(ttl=3600)
def get_live_tech_news(api_key):
    """
    Fetches real-time technology news from NewsAPI.org.
    """
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") != "ok": return None
            
        articles = []
        for i, item in enumerate(data.get("articles", [])[:12]):
            articles.append({
                "id": f"live-{i}",
                "title": item.get("title", "Classified Intel"),
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "time": item.get("publishedAt", "Recent")[:10],
                "category": "Live Intel",
                "sentiment": round(random.uniform(0.1, 0.8), 2),
                "image": item.get("urlToImage") or "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800",
                "summary": item.get("description", "Full summary restricted."),
                "content": f"### {item.get('title')}\n\n{item.get('content', 'Full report encrypted.')}\n\n[Open Dashboard Report]({item.get('url')})"
            })
        return articles
    except: return None
