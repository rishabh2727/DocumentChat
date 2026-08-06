from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# define the workflow nodes
workflow.add_node("check_relevance", self._check_relevance_step)
workflow.add_node("check_relevance", self._check_relevance_step)


workflow.set_entry_point("check_relevance")

