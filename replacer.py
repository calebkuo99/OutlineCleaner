import re
import sys

def process_text(text):
    # Replace all newline characters with a space
    text = text.replace('\n', ' ')
    
    # Add a line break before numbers followed by a period and space, while keeping the period number space format
    # text = re.sub(r'\s(\d+)\.\s', r'.\1 ', text)
    
    # Add a line break before Roman numerals followed by a period and space
    text = re.sub(r'(\b[IVXLCDM]+\b)\.\s', r'\n\n \1. ', text)
    
    # Add a line break before capital letters followed by a period and space
    text = re.sub(r'(\b[A-Z]\b)\.\s', r'\n\n\1. ', text)

    # Add a line break before capital letters (without a period) followed by a period and space
    text = re.sub(r'(\b[A-Z]\b)\s', r'\n\n\1. ', text)

    # Add a line break before number followed by a period and space
    text = re.sub(r'(\s[\d+]\b)\.\s', r'\n\n.\1 ', text)

    # Add a line break before number followed by a period and space
    text = re.sub(r'(\s[a-z]\b)\.\s', r'\n\n.\1 ', text)
    
    return text

def run_tests():
    # Test cases and their expected results
    test_cases = [
        {
            "input": "1. First item\n2. Second item\n3. Third item",
            "expected": "\n.1 First item \n.2 Second item \n.3 Third item"
        },
        {
            "input": "I. First section\nII. Second section",
            "expected": "\n I. First section \n II. Second section"
        },
        {
            "input": "A. Apple\nB. Banana\nC. Cherry",
            "expected": "\n A. Apple \n B. Banana \n C. Cherry"
        },
        {
            "input": "1. First line\n2. Second line\n3. Third line\nI. Fourth line\nA. Fifth line",
            "expected": "\n.1 First line \n.2 Second line \n.3 Third line \n I. Fourth line \n A. Fifth line"
        }
    ]
    
    # Run each test case
    for idx, case in enumerate(test_cases, 1):
        output = process_text(case['input'])
        assert output == case['expected'], f"Test case {idx} failed: {output} != {case['expected']}"
        print(f"Test case {idx} passed")

if __name__ == "__main__":
    # First, run the test cases
    # print("Running test cases...\n")
    # try:
    #     run_tests()
    #     print("\nAll test cases passed!\n")
    # except AssertionError as e:
    #     print(e)
    
    # Now allow user to input text
    print("Paste your text (press Ctrl+D when done on Linux/macOS or Ctrl+Z then Enter on Windows):")
    
    # Read entire input until EOF
    user_input = sys.stdin.read()
    
    # Process the text
    processed_text = process_text(user_input)
    
    # Print the result
    print("\nProcessed text:")
    print(processed_text)