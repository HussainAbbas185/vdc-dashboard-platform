
import streamlit as st
import pandas as pd
import altair as alt
import time
from src.audit_logger import log_action

def apply_clean_theme(chart):
    """Standard Clean Light theme for Altair."""
    return chart.configure_axis(
        labelColor='#64748b',
        titleColor='#64748b',
        gridColor='#f1f5f9',
        domainColor='#e2e8f0',
        labelFont="Inter",
        titleFont="Inter",
        titleFontWeight=600
    ).configure_view(
        stroke=None
    ).configure_title(
        color='#0f172a',
        fontSize=18,
        font="Inter",
        anchor='start'
    ).configure_legend(
        labelColor='#64748b',
        titleColor='#0f172a'
    )

def render_global_tech_news():
    st.markdown("<h1 class='vdc-main-header'>Global Tech News</h1>", unsafe_allow_html=True)
    st.write("### Aggregated Strategic Intel Feed")

    with st.sidebar:
        st.divider()
        st.write("#### Feed Configuration")
        news_api_key = st.text_input("Provider Key", type="password")

    try:
        import src.market_intelligence as mi
        if news_api_key:
            news_items = mi.get_live_tech_news(news_api_key) or mi.get_tech_news()
            st.success("🚀 Synchronized with Premium Stream")
        else:
            news_items = mi.get_tech_news()
            is_live = any(item.get('source') == 'Live RSS' for item in news_items)
            if is_live:
                st.success("📡 Synchronized with Live RSS Feed")
            else:
                st.info("💡 Simulation Mode Active")
    except Exception as e:
        st.error(f"Feed Error: {e}")
        return

    if 'selected_article_id' not in st.session_state:
        st.session_state.selected_article_id = None

    if st.session_state.selected_article_id:
        # Detail View
        article = next((a for a in news_items if a['id'] == st.session_state.selected_article_id), None)
        if article:
            if st.button("⬅️ Back to Global Feed", use_container_width=True):
                st.session_state.selected_article_id = None
                st.rerun()
            
            st.divider()
            with st.container(border=True):
                st.markdown(f"## **{article['title']}**")
                st.caption(f"Source: {article['source']} | Time: {article['time']}")
                
                st.image(article.get('image', "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800"), use_container_width=True)
                st.write(article['content'])
                st.divider()
                st.write("#### Neural Oversight")
                sc = st.slider("Categorization Accuracy", 0.0, 1.0, float(article['sentiment']))
                if st.button("Log Feedback", use_container_width=True):
                    st.toast("Feedback Committed.")
        else:
            st.session_state.selected_article_id = None
            st.rerun()
    else:
        # Feed Grid
        st.write("#### Sentiment Analysis")
        col1, col2 = st.columns(2)
        df_news = pd.DataFrame(news_items)
        with col1:
            # Clean Blue Pie Chart
            chart = alt.Chart(df_news).mark_arc(innerRadius=40, stroke="#ffffff").encode(
                theta='count()', color=alt.Color('category:N', scale=alt.Scale(scheme='blues'))
            ).properties(height=200)
            st.altair_chart(apply_clean_theme(chart), use_container_width=True)
        with col2:
            # Clean Blue Bar Chart
            hist = alt.Chart(df_news).mark_bar(color='#2563eb').encode(
                x=alt.X('sentiment:Q', title="AI Sentiment Pulse"), y=alt.Y('count()', title=None)
            ).properties(height=200)
            st.altair_chart(apply_clean_theme(hist), use_container_width=True)
        
        st.divider()
        st.write("#### Live Intel Grid")
        for i in range(0, len(news_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(news_items):
                    item = news_items[i+j]
                    with cols[j]:
                        with st.container(border=True):
                            st.image(item.get('image', "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400"), use_container_width=True)
                            st.markdown(f"**{item['title']}**")
                            st.caption(f"{item['source']} • {item['time']}")
                            if st.button("Deep Analyze", key=f"n_{item['id']}", use_container_width=True):
                                st.session_state.selected_article_id = item['id']
                                st.rerun()
