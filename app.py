
# Hard-coded API key
from groq import Groq
import ollama
import anthropic
import streamlit as st
import requests
import os

# ANTHROPIC KEY
api_key = "ANTHROPIC KEY"


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")

    api_key="ANTHROPIC KEY"
)

clientGroq = Groq(
    api_key="GROK_KEY"
)


def search_files(directory, search_text, rank_config, context_window=250):
    results = []
    search_text = search_text.lower()  # Convert search text to lowercase
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    content_lower = content.lower()  # Convert file content to lowercase for searching
                    if search_text in content_lower:
                        rank = rank_config.get(os.path.dirname(file_path), 0)
                        context = get_surrounding_context(
                            content, search_text, context_window)
                        results.append((file_path, rank, content, context))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def get_surrounding_context(content, search_text, context_window):
    index = content.lower().find(search_text.lower())
    if index != -1:
        start = max(0, index - context_window)
        end = min(len(content), index + len(search_text) + context_window)
        return content[start:end]
    return ""


def summarize_files_ollama(file_contents, search_text):
    summaries = []
    for content in file_contents:
        prompt = f"Acting as a thorough senior medical resident, please summarize the following medical record text as short bullets about the outcome of: '{search_text}'. Include no more than 5 bullets. Start first with the title of the document and the date, and then summarize. Here is the text:\n\n{content}\n"
        response = ollama.generate(model='mistral', prompt=prompt)
        summary = response['response']
        print("Generated Summary:")
        print(summary)
        print("---")
        summaries.append(summary)
    return summaries


def summarize_files_groq(file_contents, search_text):
    summaries = []
    for content in file_contents:
        prompt = f"Acting as a thorough senior medical resident, please summarize the following medical record text as short bullets about the outcome of: '{search_text}'. Include no more than 5 bullets. Start first with the title of the document and the date, and then summarize. Here is the text:\n\n{content}\n"
        chat_completion = clientGroq.chat.completions.create(messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
            model="mixtral-8x7b-32768",)

        summary = chat_completion.choices[0].message.content
        print("Generated Summary:")
        print(summary)
        print("---")
        summaries.append(summary)
    return summaries


def summarize_files_anthropic(file_contents, search_text, api_key):
    summaries = []
    for content in file_contents:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=3000,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Acting as a thorough senior medical resident, please summarize the following medical record text as short bullets about the outcome of: '{search_text}'. Include no more than 5 bullets. Start first with the title of the document and the date, and then summarize. Here is the text:\n\n{content}\n"
                        }
                    ]
                }
            ]
        )
        content_block = message.content[0]
        summary = content_block.text

        print("Generated Summary:")
        print(summary)
        print("---")
        summaries.append(summary)
    return summaries


def main():
    st.header("🔍 Searching :blue[**Steven Chou**]'s Medical Record")
    st.subheader(" \nDOB 1/7/1959 (59M)")

    # User input for search text
    search_text = st.text_input("Enter search text:")

    # Dropdown to select the summarization function
    summarization_function = st.selectbox(
        "Select Summarization Function", ("Anthropic", "Mistral (Local)", "Groq"))

    # Hard-coded directory path
    directory = "./"

    # User input for rank configuration
    rank_config = {
        "./procedure": 4,
        "./discharge": 3,
        "./admission": 2,
        "./progress": 1
    }

    if st.button("Search and Summarize"):
        if search_text:
            search_results = search_files(directory, search_text, rank_config)
            top_files = [content for _, _, content, _ in search_results[:3]]
            top_contexts = [context for _, _, _, context in search_results[:3]]

            st.subheader("Top Documents Searched:")
            for i, (file_path, _, _, context) in enumerate(search_results[:3], start=1):
                file_name = os.path.basename(file_path)
                directory_name = os.path.basename(os.path.dirname(file_path))
                expander = st.expander(
                    f"Document {i}: (Category: {directory_name}) \n\n {file_name} ")
                with expander:
                    st.write(context)

#            summaries = summarize_files_anthropic(            top_files, search_text, api_key)

            if summarization_function == "Anthropic":
                summaries = summarize_files_anthropic(
                    top_files, search_text, api_key)
            elif summarization_function == "Groq":
                summaries = summarize_files_groq(top_files, search_text)
            elif summarization_function == "Mistral (Local)":
                summaries = summarize_files_ollama(top_files, search_text)

            st.subheader("Document Summaries:")
            for i, summary in enumerate(summaries, start=1):
                st.markdown(f"**AI Summary:**")
                st.write(summary)
                st.write("---")
        else:
            st.warning("Please enter a search text.")


if __name__ == "__main__":
    main()
