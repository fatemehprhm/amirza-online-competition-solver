import requests
from bs4 import BeautifulSoup
import re

def extract_amirza_words(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_words = set()
        
        td_elements = soup.find_all('td', style=lambda x: x and 'text-align: center' in x)
        
        print(f"Found {len(td_elements)} centered td elements")
        
        for td in td_elements:
            text = td.get_text().strip()
            
            text = text.replace('\u00a0', '').strip()
            text = re.sub(r'^\s+', '', text)
            
            if not text or 'مرحله' in text or 'جواب' in text or 'مراحل' in text:
                continue
            
            if '/' in text:
                words = text.split('/')
                
                for word in words:
                    word = word.strip()
                    if word and contains_persian(word) and len(word) > 1:
                        all_words.add(word)
        
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for table_num, table in enumerate(tables, 1):
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                
                if len(cells) >= 2:
                    level_cell = cells[0].get_text().strip()
                    answer_cell = cells[1].get_text().strip()
                    
                    if 'مرحله' in level_cell and answer_cell:
                        answer_text = answer_cell.replace('\u00a0', '').strip()
                        
                        if '/' in answer_text:
                            words = answer_text.split('/')
                            
                            for word in words:
                                word = word.strip()
                                if word and contains_persian(word) and len(word) > 1:
                                    all_words.add(word)
        
        print(f"Extracted {len(all_words)} unique words")
        return sorted(all_words)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def contains_persian(text):
    persian_range = r'[\u0600-\u06FF]'
    return bool(re.search(persian_range, text))

def save_words_to_file(words, filename='amirza_words.txt'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')
        print(f"Successfully saved {len(words)} words to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    url = "https://www.digikala.com/mag/complete-amirza-guide/"
    
    print("Starting word extraction from Amirza guide...")
    print(f"URL: {url}")
    print("-" * 50)
    
    words = extract_amirza_words(url)
    
    if words:
        save_words_to_file(words)
        
        print("-" * 50)
        print("EXTRACTION COMPLETE!")
        print(f"Total unique words extracted: {len(words)}")
        print("\nFirst 10 words:")
        for i, word in enumerate(words[:10], 1):
            print(f"{i}. {word}")
        
        print("\nLast 10 words:")
        for i, word in enumerate(words[-10:], len(words)-9):
            print(f"{i}. {word}")
            
        word_lengths = {}
        for word in words:
            length = len(word)
            word_lengths[length] = word_lengths.get(length, 0) + 1
        
        print("\nWord length distribution:")
        for length in sorted(word_lengths.keys()):
            print(f"{length} characters: {word_lengths[length]} words")
    
    else:
        print("No words were extracted. Please check the URL and try again.")

if __name__ == "__main__":
    main()