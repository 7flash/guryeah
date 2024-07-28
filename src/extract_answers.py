import re
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_questions_answers(input_file, output_questions_file, output_answers_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        questions = []
        answers = []
        # Indicate if the next line is expected to be an answer
        expecting_answer = False

        for i, line in enumerate(lines):
            # Remove leading/trailing whitespace
            processed_line = line.strip()

            # Debug log the processed line
            logging.debug(f"Processing line {i}: {processed_line}")

            # Skip lines starting with //
            if processed_line.startswith("//"):
                logging.debug(f"Skipping line {i} as it starts with //")
                continue

            # Check if the line is a question or an answer
            if processed_line and not re.match(r'^\s*[-]*\s*$', processed_line):
                if expecting_answer or "A:" in processed_line:
                    # Assuming the answer does not strictly need to start with "-" for the second file type
                    answer = re.sub(r'^-?\s*', '', processed_line)  # Remove leading dash and whitespace if present
                    answer = re.sub(r'^\*\*A:\s*', '', answer)  # Remove leading "**A: " if present
                    answer = re.sub(r'^A:', '', answer)
                    answers.append(answer)
                    logging.info(f"Extracted answer: {answer}")
                    expecting_answer = False
                else:
                    # Treat any non-empty line not starting with '-' as a question
                    question = re.sub(r'^\*\*Q:\s*', '', processed_line)  # Remove leading "**Q: " if present
                    question = re.sub(r'^Q:', '', processed_line)
                    questions.append(question)
                    logging.debug("Question detected.")
                    expecting_answer = True

        with open(output_questions_file, 'w') as file:
            for question in questions:
                file.write(question + '\n')

        with open(output_answers_file, 'w') as file:
            for answer in answers:
                file.write(answer + '\n')

        logging.info(f"Questions and answers extracted successfully into {output_questions_file} and {output_answers_file}.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py input_file output_questions_file output_answers_file")
    else:
        input_file = sys.argv[1]
        output_questions_file = sys.argv[2]
        output_answers_file = sys.argv[3]
        extract_questions_answers(input_file, output_questions_file, output_answers_file)
