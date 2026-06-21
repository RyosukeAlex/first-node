# ===== 0. Library Install =====
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# ===== 1. State = グラフ全体で共有するWorking Memory =====
class State(TypedDict):
    topic: str
    notes: str

llm = ChatOpenAI(model='gpt-4o-mini')

# ===== 2. Node = stateを受け取り、更新したいキーだけをdictで返却する関数 =====
def researcher(state: State):
    print('--- Research Agent is working ---')
    topic = state['topic']
    responce = llm.invoke(f'次のトピックを簡潔に調べて、要点を3つにまとめてください: {topic}')
    return {'notes': responce.content}


# ===== 3. グラフを組み立てる =====
graph = StateGraph(State)
graph.add_node("researcher", researcher)
graph.add_edge(START, "researcher")
graph.add_edge("researcher", END)
app = graph.compile()

# ===== 4. 実行 =====
result = app.invoke({"topic": "マルチエージェント", "notes": ""})
print("最終 state:", result)