import argparse
import re

# Set up argparse
parser = argparse.ArgumentParser(description='Convert a subtitle file to a formatted text file.')
parser.add_argument('input_file',
        metavar='input_file', type=str, help='The input subtitle file in .srt format')
parser.add_argument('output_file',
        metavar='output_file', type=str, help='The output file to write formatted text to')
args = parser.parse_args()

# Read the input text from the specified file
with open(args.input_file, 'r') as file:
    input_text = file.read()

# Use regular expression to find the timestamp and text on separate lines
pattern = r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\n(.+?)(?=\n\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\n|$)'
matches = re.findall(pattern, input_text, re.DOTALL)

# Write output to the specified file
with open(args.output_file, 'w') as file:
    for i, match in enumerate(matches):
        print(f'match {i}: {match}')
        timestamp = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', match).group(1)
        text = re.sub(r'\n', ' ', match).replace(timestamp, '').strip()
        file.write(f'{timestamp} - {text}\n')
