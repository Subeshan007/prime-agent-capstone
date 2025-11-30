"""
Enterprise UI Components for PRIME
Strict enterprise SaaS aesthetic with minimal flat design.
"""
import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os


from prime_agent.utils.pdf_generator import generate_pdf_report

def render_notes(notes: dict):
    """Render notes with enterprise styling"""
    st.markdown("""
        <div style='background-color: #1F2124; border: 1px solid #2A2D31; border-radius: 10px; padding: 32px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.18); max-width: 900px; margin-left: auto; margin-right: auto;'>
            <h2 style='font-size: 24px; margin-top: 0; padding-bottom: 16px; margin-bottom: 24px; font-weight: 600; color: #FFFFFF; border-bottom: 1px solid #2A2D31;'>
                Research Notes
            </h2>
            <div style='color: #E4E7EC; font-family: "Inter", sans-serif; line-height: 1.7; font-size: 15px;'>
    """, unsafe_allow_html=True)
    
    content = notes.get("content", "No notes available.")
    
    # Ensure content is a string (fix for list content)
    if isinstance(content, list):
        content = "\n\n".join([str(x) for x in content])
        
    st.markdown(content)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Generate PDF
    try:
        pdf_bytes = generate_pdf_report(content)
        file_name = "research_report.pdf"
        mime_type = "application/pdf"
        data = pdf_bytes
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")
        # Fallback to markdown
        file_name = "research_report.md"
        mime_type = "text/markdown"
        data = content
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="Download PDF Report",
            data=data,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True
        )


def render_quiz(quiz: list):
    """Render quiz with enterprise styling"""
    if not quiz:
        st.info("No quiz generated.")
        return
    
    score = 0
    total_answered = 0
    
    for i, q in enumerate(quiz):
        st.markdown(f"""
            <div style='background-color: #1F2124; border: 1px solid #2A2D31; border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.18);'>
                <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
                    <span style='background-color: #3A7BFA; color: white; font-size: 13px; font-weight: 600; padding: 6px 12px; border-radius: 6px;'>Q{i+1}</span>
                    <span style='color: #FFFFFF; font-size: 16px; font-weight: 500;'>{q['question']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        user_answer = st.radio(
            "Select Answer",
            q["options"],
            key=f"quiz_{i}",
            index=None,
            label_visibility="collapsed"
        )
        
        if user_answer:
            total_answered += 1
            correct_option = q["options"][q["correct_index"]]
            
            if user_answer == correct_option:
                st.success("Correct!")
                score += 1
            else:
                st.error(f"Incorrect. Answer: {correct_option}")
            
            with st.expander("View Explanation"):
                st.markdown(q["explanation"])
        
        st.markdown("<div style='margin-bottom: 24px'></div>", unsafe_allow_html=True)

    if total_answered > 0:
        st.markdown(f"""
            <div style='background-color: #3A7BFA; border-radius: 10px; padding: 24px; text-align: center;'>
                <h3 style='color: white; margin: 0 0 8px 0; font-size: 16px; font-weight: 600;'>Final Score</h3>
                <div style='color: white; font-size: 36px; font-weight: 600;'>{score}/{len(quiz)}</div>
                <p style='color: rgba(255,255,255,0.9); margin-top: 8px; font-size: 14px;'>{round((score/len(quiz))*100)}% Accuracy</p>
            </div>
        """, unsafe_allow_html=True)


def render_flashcards(quiz: list):
    """Render flashcards with enterprise styling"""
    if not quiz:
        st.info("No flashcards available.")
        return
    
    cols = st.columns(2)
    
    for i, q in enumerate(quiz):
        with cols[i % 2]:
            with st.expander(f"Flashcard {i+1}", expanded=False):
                st.markdown(f"""
                    <div style='margin-bottom: 16px;'>
                        <strong style='color: #FFFFFF; display: block; margin-bottom: 10px; font-size: 15px;'>Question</strong>
                        <span style='color: #E4E7EC; font-size: 14px; line-height: 1.6;'>{q['question']}</span>
                    </div>
                    <div style='padding: 18px; background-color: #1F2124; border-radius: 8px; border: 1px solid #2A2D31; margin-bottom: 16px;'>
                        <strong style='color: #3A7BFA; display: block; margin-bottom: 8px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;'>Answer</strong>
                        <span style='color: #FFFFFF; font-size: 15px; font-weight: 500;'>{q['options'][q['correct_index']]}</span>
                    </div>
                    <div style='padding-top: 16px; border-top: 1px solid #2A2D31;'>
                        <strong style='color: #A3A8B0; display: block; margin-bottom: 8px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;'>Explanation</strong>
                        <span style='color: #E4E7EC; font-size: 14px; line-height: 1.6;'>{q['explanation']}</span>
                    </div>
                """, unsafe_allow_html=True)


def render_graph(graph_data: dict):
    """Render knowledge graph with enterprise styling"""
    if not graph_data or not graph_data.get("nodes"):
        st.info("No graph data available.")
        return
    
    G = nx.DiGraph()
    
    for node in graph_data["nodes"]:
        G.add_node(node["id"], label=node["label"], title=node["type"], group=node["type"])
    
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], title=edge["relation"], label=edge["relation"])
    
    net = Network(
        height="700px",
        width="100%",
        bgcolor="#141618",
        font_color="#E4E7EC",
        notebook=False
    )
    net.from_nx(G)
    
    net.set_options("""
    {
        "nodes": {
            "color": {
                "background": "#1F2124",
                "border": "#3A7BFA",
                "highlight": {
                    "background": "#3A7BFA",
                    "border": "#FFFFFF"
                }
            },
            "font": {
                "color": "#E4E7EC",
                "size": 14,
                "face": "Inter"
            },
            "borderWidth": 1,
            "shape": "box",
            "margin": 12,
            "shadow": {
                "enabled": true,
                "color": "rgba(0,0,0,0.2)",
                "size": 4
            }
        },
        "edges": {
            "color": {
                "color": "#2A2D31",
                "highlight": "#3A7BFA"
            },
            "smooth": true,
            "width": 1
        }
    }
    """)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        tmp.close()
        
        with open(tmp.name, 'r', encoding='utf-8') as f:
            html = f.read()
        
        st.components.v1.html(html, height=700)
        os.unlink(tmp.name)


def render_sources(credibility_scores: list):
    """Render sources with enterprise styling"""
    if not credibility_scores:
        st.info("No source analysis available.")
        return
    
    for i, item in enumerate(credibility_scores):
        score = item.get('score', 0)
        score_color = "#3A7BFA" if score >= 0.7 else "#F1C40F" if score >= 0.4 else "#E74C3C"
        
        st.markdown(f"""
            <div style='background-color: #1F2124; border: 1px solid #2A2D31; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.18);'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <a href='{item.get("source", "#")}' target='_blank' style='color: #3A7BFA; text-decoration: none; font-weight: 500; font-size: 15px; display: block; margin-bottom: 6px;'>
                            {item.get('title', 'Source')} →
                        </a>
                        <p style='color: #A3A8B0; font-size: 13px; margin: 0; line-height: 1.6;'>
                            {item.get('explanation', '')}
                        </p>
                    </div>
                    <div style='margin-left: 32px;'>
                        <div style='background-color: rgba(58,123,250,0.1); color: {score_color}; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 14px; border: 1px solid rgba(58,123,250,0.2);'>
                            {score:.2f}
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_mind_map(dot_code: str):
    """Render Graphviz mind map"""
    if not dot_code:
        st.info("No mind map available.")
        return
    
    dot_code = dot_code.replace("```dot", "").replace("```", "").strip()
    
    try:
        st.graphviz_chart(dot_code)
    except Exception as e:
        st.error(f"Failed to render: {e}")
        st.code(dot_code, language="dot")
