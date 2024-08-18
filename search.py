import re
import streamlit as st
import requests
import json

# Perplexity AI API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"

# Replace with your actual API key
API_KEY = "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"


def search(content: str):
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [{"role": "user", "content": content}],
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    print(response.text)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


def extract_usernames(text):
    # Regular expression pattern to match @username
    pattern = r"@(\w+)"
    # Find all matches in the text
    usernames = re.findall(pattern, text)
    handles = list(set(usernames))
    return "".join(
        [f"<li><a href='https://x.com/{x}' target='_blank'>@{x}</li>" for x in handles]
    )


# Streamlit UI
st.title("Humblebrag AI lookup")

name = st.text_input("Enter a person's name:")

if st.button("Search"):
    if name:
        with st.spinner("Searching..."):
            news = search(f"Find recent news mentioning {name}")
            bio = search(f"Find bio for {name}")
            linkedIn = search(f"Find LinkedIn for {name}")
            twitter = search(f"Find Twitter for {name}")
            website = search(f"Find websites for {name}")
            youtube = search(f"Find youtube for {name}")

            st.html("<h1>Report:</h1>")
            st.markdown(f"## news:\n{news}")
            st.markdown(f"## bio:\n{bio}")
            st.markdown(f"## linkedIn:\n{linkedIn}")
            st.markdown("## twitter")
            st.markdown(twitter)
            st.html(f"<strong>Handles:</strong><ul>{extract_usernames(twitter)}</ul>")
            st.markdown(f"## Website:\n{website}")
            st.markdown(f"## Youtube:\n{youtube}")
    else:
        st.warning("Please enter a name.")
