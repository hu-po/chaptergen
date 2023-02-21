from typing import List
import os
import openai
import argparse
import re
import polars as pl
from sentence_transformers import SentenceTransformer, util

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
pattern = r'(\d{2}:\d{2}:\d{2}),\d{3} --> (\d{2}:\d{2}:\d{2}),\d{3}\n(.+?)(?=\n)'
matches = re.findall(pattern, input_text, re.DOTALL)

# Get the text and timestamps from the matches
_data = {
    'start_time' : [],
    'end_time' : [],
    'raw_text' : [],
}
for i, match in enumerate(matches):
    start, end, text = match
    _data['start_time'].append(start)
    _data['end_time'].append(end)
    _data['raw_text'].append(text)

# Pack into a polars DataFrame
df = pl.DataFrame(_data)

def batch_text_to_sentences(raw_text: List[str], max_prompt_length: int = 2048):
    paragraph = ''
    for text in raw_text:
        if len(paragraph + text) < max_prompt_length:
            paragraph += text
        else:
            yield paragraph
            paragraph = ''

openai.api_key = os.getenv("OPENAI_API_KEY")

for prompt in batch_text_to_sentences(df['raw_text']):

prompt = ''
    prompt += "\n\nTl;dr"
    # From TL:DR example
    # https://platform.openai.com/examples/default-tldr-summary
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

# Split TLDR into sentences

# Use word similarity to find the most relevant timestamps for each part of the TLDR.
# https://huggingface.co/tasks/sentence-similarity
sentences = ["I'm happy", "I'm full of happiness"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

util.pytorch_cos_sim(embedding_1, embedding_2)
## tensor([[0.6003]])


# Make sure chapters are somewhat evenly spaced