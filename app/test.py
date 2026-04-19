from app.graph.builder import build_graph

graph = build_graph()

result = graph.invoke({
    "query": "What is black hole?"
})

print(result["answer"])