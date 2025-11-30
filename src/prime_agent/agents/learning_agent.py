"""
Learning agent.
"""
from prime_agent.agents.state import AgentState
from prime_agent.tools.quiz_generator import generate_quiz
from prime_agent.storage.vector_store import VectorStore
from loguru import logger

def learning_node(state: AgentState) -> AgentState:
    """
    Generate learning materials (Quizzes).
    """
    logger.info("Starting learning content generation...")
    topic = state["topic"]
    
    # Retrieve context again or use summary/notes
    # Handle notes structure which might be a dict of sections or a string
    notes_content = ""
    notes = state.get("notes", {})
    if isinstance(notes, str):
        notes_content = notes
    elif isinstance(notes, dict):
        # Join all values if it's a dict of sections
        notes_content = "\n\n".join([str(v) for v in notes.values()])
    
    context = state.get("summary", "") + "\n\n" + notes_content
    
    logger.info(f"Context length for quiz: {len(context)}")
    
    if not context or len(context) < 100:
        logger.warning("Context too short, fetching from VectorStore...")
        vs = VectorStore()
        results = vs.search(topic, k=5)
        context = "\n\n".join([r["content"] for r in results])
        logger.info(f"Context length after VS search: {len(context)}")
        
    if context:
        quiz = generate_quiz(context, num_questions=5)
        logger.info(f"Generated {len(quiz)} quiz questions")
        state["quiz"] = quiz
    else:
        logger.warning("No context available for quiz generation")
        state["quiz"] = []
        
    return state
