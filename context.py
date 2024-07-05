import re
import nltk
import subprocess
from nltk.corpus import stopwords

# Download the stopwords list if not already downloaded
nltk.download('stopwords')

def preprocess_text(text):
    # Define stop words
    stop_words = set(stopwords.words('english'))
    
    # Split the text into words and filter out stop words
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    return filtered_words

def get_surrounding_words(text, target_word, num_words=40):
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

def main():
    # Path to your text file
    file_path = 'dataset.txt'
    
    # Read the entire content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Get the target sentence from the user
    target_sentence = input("What is your question: ")
    
    # Preprocess the target sentence to remove non-context words
    target_words = preprocess_text(target_sentence)
    
    paragraphs = []
    for word in target_words:
        paragraph = get_surrounding_words(text, word)
        if paragraph:
            paragraphs.append(paragraph)
    
    # Join all paragraphs into a single text
    result_text = '\n\n'.join(paragraphs)
    
    # Store the result in a variable
    final_paragraph = result_text
    
    context_data = (f"question: \n {target_sentence} \ncontext information: \n {result_text}")
    # Output the result
    #print(final_paragraph)
    print(context_data)
									

if __name__ == "__main__":
    main()
