import re

# Read the input text from a .srt file
with open('input.srt', 'r') as file:
    input_text = file.read()

# Use regular expression to find the timestamp and text on separate lines
pattern = r'\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}\n(.+?(?=\n\d{2}:\d{2}:\d{2},\d{3}\s-->)|.+)'
matches = re.findall(pattern, input_text, re.DOTALL)

# Iterate through matches to print output
for i, match in enumerate(matches):
    timestamp = re.search(r'\d{2}:\d{2}:\d{2},\d{3}', match).group()
    text = re.sub(r'\n', ' ', match).replace(timestamp, '').strip()
    print(f'{timestamp} - {text}')
