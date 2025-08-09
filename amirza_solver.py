import sys
from collections import Counter

def read_words_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            unique_words = [line.strip() for line in f.readlines()]
                
        print(f"Successfully loaded {len(unique_words)} unique words from {filename}")
        return unique_words
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def find_possible_words(letters, database):

    input_letters_str = "".join(letters.split())
    input_counts = Counter(input_letters_str)
    
    possible_words = []
    for word in database:
        word_counts = Counter(word)
        is_possible = True
        for char, count in word_counts.items():
            if input_counts[char] < count:
                is_possible = False
                break
        
        if is_possible:
            possible_words.append(word)
            
    return possible_words

if __name__ == "__main__":
    word_database = read_words_from_file('amirza_words.txt')
    while True:
        my_letters = input("\n> Enter your letters (or type 'exit' to close): ")

        if my_letters.lower() == 'exit':
            break

        found_words = find_possible_words(my_letters, word_database)

        if found_words:
            print(f"Found {len(found_words)} possible words:")
            print(" / ".join(found_words))
        else:
            print(f"No words could be formed with the letters '{my_letters}'.")