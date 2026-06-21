# ===== 0. Library Install =====
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ===== 1. State = グラフ全体で共有するWorking Memory =====
class State(TypedDict):
    topic: str
    notes: str

# ===== 2. Node = stateを受け取り、更新したいキーだけをdictで返却する関数 =====
def researcher(state: State) -> dict:
    print('--- Research Agent is working ---')
    topic = state['topic']
    return {'notes': f'「{topic}」について調べた結果(仮)'}

# ===== 3. グラフを組み立てる =====
graph = StateGraph(State)
graph.add_node('researcher', researcher)
graph.add_edge(START, 'researcher')
graph.add_edge('researcher', END)
app = graph.compile()

# ===== 4. 実行 =====
result = app.invoke({'topic': 'Malti Agents', 'notes': ""})
print('最終 state:', result)