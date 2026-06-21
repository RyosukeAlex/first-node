# ===== 0. Library Install =====
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# ===== 1. State = グラフ全体で共有するWorking Memory =====
class State(TypedDict):
    topic: str
    notes: str
    review: str

llm = ChatOpenAI(model='gpt-4o-mini')

# ===== 2. Node = stateを受け取り、更新したいキーだけをdictで返却する関数 =====
def researcher(state: State) -> dict:
    print("--- Research Agent is working ---")
    topic = state["topic"]
    response = llm.invoke(f"次のトピックを簡潔に調べて、要点を3つにまとめてください: {topic}")
    return {"notes": response.content}

# ===== 2.5. Node = stateを受け取り、レビューを行う =====
def reviewer(state: State) -> dict:               # ← ② 2体目のエージェントを追加
    print("--- Reviewer Agent is working ---")
    notes = state["notes"]                         #    researcher が書いた notes を受け取る
    response = llm.invoke(f"次の調査メモを読んで、内容が妥当か・抜けや誤りがないかを論理的に評価してください:\n\n{notes}")
    return {"review": response.content}

# ===== 3. グラフを組み立てる =====
graph = StateGraph(State)
graph.add_node("researcher", researcher)
graph.add_node("reviewer", reviewer)              # ← ③ reviewer をグラフに登録
graph.add_edge(START, "researcher")
graph.add_edge("researcher", "reviewer")          #    researcher の "後に" reviewer を繋ぐ
graph.add_edge("reviewer", END)

app = graph.compile()

result = app.invoke({"topic": "マルチエージェント", "notes": "", "review": ""})
print("最終 state:", result)