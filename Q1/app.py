from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

app = Flask(__name__)

# Initialize the RAG model
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

@app.route('/question-answering', methods=['POST'])
def answer():
    question = request.json['question']

    # Encode the question and generate the answer ids
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(**inputs)

    # Decode the output ids to get the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify(answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


# curl -X POST http://localhost:5001/question-answering -H "Content-Type: application/json" -d '{"question":"What is the capital of France?"}'

