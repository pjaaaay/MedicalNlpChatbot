from flask import Flask, render_template, request
import re
import nltk
import subprocess
from nltk.corpus import stopwords

# Download the stopwords list if not already downloaded
nltk.download('stopwords')

app = Flask(__name__)

def preprocess_text(text):
    # Define stop words
    stop_words = set(stopwords.words('english'))

    # Split the text into words and filter out stop words
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return filtered_words

def get_surrounding_words(text, target_word, num_words=20):
    # Find the first occurrence of the target word
    match = re.search(r'\b{}\b'.format(re.escape(target_word)), text)
    if not match:
        return ""

    # Calculate the positions to slice around the target word
    start_idx = match.start()
    end_idx = match.end()

    # Get words before and after the target word
    words_before = text[:start_idx].split()[-num_words:]
    words_after = text[end_idx:].split()[:num_words]

    # Combine them into a paragraph
    surrounding_words = words_before + [target_word] + words_after

    return ' '.join(surrounding_words)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input from the form
        target_sentence = request.form['target_sentence']

        # Path to your text file
        file_path = 'dataset.txt'

        # Read the entire content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Preprocess the target sentence to remove non-context words
        target_words = preprocess_text(target_sentence)

        paragraphs = []
        for word in target_words:
            paragraph = get_surrounding_words(text, word)
            if paragraph:
                paragraphs.append(paragraph)

        # Join all paragraphs into a single text
        final_paragraph = '\n\n'.join(paragraphs)

        # Form the context data prompt
        context_data = f"Question: {target_sentence}\nContext:\n{final_paragraph}"

        # Attempt to run ollama with the context_data
        try:
            process = subprocess.Popen(['ollama', 'run', 'llama2'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(input=context_data)
            ollama_output = output if output else error  # Capture ollama output or error
        except Exception as e:
            ollama_output = f"Error running ollama: {e}"

        return render_template('index.html', target_sentence=target_sentence, final_paragraph=final_paragraph, ollama_output=ollama_output)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
