from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import openai
import os
import textwrap

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Function to call OpenAI API for summarizing text
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following text: {text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

# Function to read the transcript and break it into chunks
def process_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()

    # Break the transcript into chunks that fit into OpenAI API chatgpt context
    chunks = textwrap.wrap(transcript, width=2048)

    # Summarize and condense each chunk
    summarized_transcript = ""
    for chunk in chunks:
        summarized_chunk = summarize_text(chunk)
        summarized_transcript += summarized_chunk + "\n"

    return summarized_transcript

# Main function to read the file path and write the summarized transcript to a new file
def main():
    file_path = input("Enter the path to the .txt file: ")

    summarized_transcript = process_transcript(file_path)

    output_file_path = os.path.splitext(file_path)[0] + "_summarized.txt"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(summarized_transcript)

    print(f"Summarized transcript saved to: {output_file_path}")

if __name__ == "__main__":
    main()
    
    # Must be a single transcript.
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    formatter = JSONFormatter()

    # .format_transcript(transcript) turns the transcript into a JSON string.
    json_formatted = formatter.format_transcript(transcript)


    # Now we can write it out to a file.
    with open('your_filename.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)
