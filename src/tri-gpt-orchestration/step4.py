from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

class State(TypedDict):
    topic: str
    notes: str
    review: str

llm = ChatOpenAI(model="gpt-4o-mini")

def orchestrator(state: State) -> dict:           # ← ① まとめ役（今は判断するだけ）
    print("--- Orchestrator: 状況を確認中 ---")
    return {}

def route(state: State) -> str:                   # ← ② 次に誰を動かすか決める関数
    if not state["notes"]:
        return "researcher"
    elif not state["review"]:
        return "reviewer"
    else:
        return "end"

def researcher(state: State) -> dict:
    print("--- Research Agent is working ---")
    topic = state["topic"]
    response = llm.invoke(f"次のトピックを簡潔に調べて、要点を3つにまとめてください: {topic}")
    return {"notes": response.content}

def reviewer(state: State) -> dict:
    print("--- Reviewer Agent is working ---")
    notes = state["notes"]
    response = llm.invoke(f"次の調査メモを読んで、内容が妥当か・抜けや誤りがないかを簡潔に評価してください:\n\n{notes}")
    return {"review": response.content}

graph = StateGraph(State)
graph.add_node("orchestrator", orchestrator)
graph.add_node("researcher", researcher)
graph.add_node("reviewer", reviewer)

graph.add_edge(START, "orchestrator")
graph.add_conditional_edges("orchestrator", route, {   # ← ③ 条件分岐
    "researcher": "researcher",
    "reviewer": "reviewer",
    "end": END,
})
graph.add_edge("researcher", "orchestrator")       # ← ④ 終わったら戻る（ループ）
graph.add_edge("reviewer", "orchestrator")

app = graph.compile()

result = app.invoke({"topic": "マルチエージェント", "notes": "", "review": ""})
print("最終 state:", result)