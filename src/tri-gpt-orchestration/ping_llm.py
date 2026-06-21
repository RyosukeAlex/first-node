from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model='gpt-4o-mini')
responce = llm.invoke('こんにちは。あなたは誰ですか。')

print(responce.content)