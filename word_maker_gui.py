import itertools
import nltk
from nltk.corpus import words, wordnet
import tkinter as tk
from tkinter import ttk, scrolledtext

# Download required NLTK data (first-time usage)
nltk.download('words')
nltk.download('wordnet')

# Functions
def generate_valid_words(input_string):
    """Generate all valid words from the given string."""
    valid_words = set(words.words())
    possible_words = set()
    
    # Clean the input string: Remove non-alphabetic characters
    cleaned_string = ''.join(e for e in input_string if e.isalpha())
    
    # Generate permutations
    for i in range(1, len(cleaned_string) + 1):
        permutations = itertools.permutations(cleaned_string, i)
        for perm in permutations:
            word = ''.join(perm).lower()
            if word in valid_words:
                possible_words.add(word)
    
    return sorted(possible_words)

def get_meanings_with_wordnet(word_list):
    """Fetch meanings for each word using WordNet."""
    meanings = {}
    for word in word_list:
        synsets = wordnet.synsets(word)
        if synsets:
            definitions = [syn.definition() for syn in synsets]
            meanings[word] = definitions
    return meanings

# GUI Application
class WordFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Generator and Meaning Finder")
        self.root.geometry("600x500")
        
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter a string of letters:").grid(row=0, column=0, padx=5)
        self.input_entry = ttk.Entry(input_frame, width=30)
        self.input_entry.grid(row=0, column=1, padx=5)
        
        generate_button = ttk.Button(input_frame, text="Generate Words", command=self.generate_words)
        generate_button.grid(row=0, column=2, padx=5)
        
        # Results Frame
        results_frame = tk.Frame(self.root)
        results_frame.pack(pady=10, fill="both", expand=True)
        
        tk.Label(results_frame, text="Results:").pack(anchor="w")
        
        self.results_box = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=20)
        self.results_box.pack(fill="both", expand=True, padx=5, pady=5)
    
    def generate_words(self):
        """Generate words and display their meanings."""
        self.results_box.delete(1.0, tk.END)
        input_string = self.input_entry.get().strip()
        
        # Validate input (only allow alphanumeric characters and spaces)
        if not input_string:
            self.results_box.insert(tk.END, "Please enter a string of letters.\n", "error")
            return
        
        valid_words = generate_valid_words(input_string)
        
        if valid_words:
            # Display word count
            self.results_box.insert(tk.END, f"Total valid words generated: {len(valid_words)}\n\n")
            
            word_meanings = get_meanings_with_wordnet(valid_words)
            for word, definitions in word_meanings.items():
                self.results_box.insert(tk.END, f"{word}:\n", "bold")
                for definition in definitions:
                    self.results_box.insert(tk.END, f"  - {definition}\n")
        else:
            self.results_box.insert(tk.END, "No valid words found.\n", "error")
        
        # Add tags for styling
        self.results_box.tag_config("bold", font=("Times New Roman", 10, "bold"))
        self.results_box.tag_config("error", foreground="red")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WordFinderApp(root)
    root.mainloop()
