from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from guardrails import mask_pii
from rag_pipeline import retrieve_policy_context

class AgentState(TypedDict):
    incident_report: str
    masked_report: Optional[str]
    policy_context: Optional[str]
    analysis_result: Optional[str]
    requires_human: bool

def node_guardrail(state: AgentState):
    masked = mask_pii(state['incident_report'])
    return {"masked_report": masked}

def node_rag_retrieval(state: AgentState):
    context = retrieve_policy_context(state['masked_report'])
    return {"policy_context": context}

def node_llm_analysis(state: AgentState):
    # Mock LLM Call using Context and MCP Data
    anomaly_score = 0.85 # Simulated LLM-as-judge score
    requires_human = anomaly_score > 0.8
    return {"analysis_result": "Breach detected based on SR 11-7.", "requires_human": requires_human}

def router_hitl(state: AgentState):
    if state['requires_human']: return "human_review"
    return "auto_approve"

def node_human_review(state: AgentState):
    # Escalation path
    return {"analysis_result": state['analysis_result'] + " [ESCALATED TO SME]"}

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("guardrail", node_guardrail)
workflow.add_node("rag", node_rag_retrieval)
workflow.add_node("llm", node_llm_analysis)
workflow.add_node("human_review", node_human_review)

workflow.set_entry_point("guardrail")
workflow.add_edge("guardrail", "rag")
workflow.add_edge("rag", "llm")
workflow.add_conditional_edges("llm", router_hitl, {"human_review": "human_review", "auto_approve": END})
workflow.add_edge("human_review", END)

app = workflow.compile()
