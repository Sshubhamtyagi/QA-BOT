# Clone the repository

# Install the dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Test the application
curl -X POST http://localhost:5000/ask -H "Content-Type: multipart/form-data" -F "file=@path/to/your/file.pdf" -F "questions_file=@path/to/your/questions.json"