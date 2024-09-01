import os
import json
from flask import Flask, request, jsonify
from service.base_llm_service import LLMFactory

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

@app.route('/ask', methods=['POST'])
def ask():
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    questions_file = request.files['questions_file']
    questions = json.loads(questions_file.read().decode('utf-8'))  # Parse the questions string into a list
    service_type = request.form.get('service_type', 'openai')
    # Pass the file directly to the LLM service
    file_path = os.path.join(os.path.dirname(__file__), file.filename)
    file.save(file_path)
    llm_service = LLMFactory.get_llm_service(service_type)
    # Let the LLM service handle document processing and vector store creation
    data, error = llm_service.get_answers(questions, file_path)
    # remove the file after processing
    os.remove(file_path)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)

# ["What is trip destination?", "What are the required documents for trip?", "what is the price for the trip?", "what is the itinerary of the trip?"]