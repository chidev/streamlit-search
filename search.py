from dotenv import load_dotenv
import os
import re
import streamlit as st
import requests

load_dotenv()

# Perplexity AI API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"


def tags(content: str):
    msg = f"""Your response should be 2 lines, without a label at the beginning of the line, on the first line extract all the cities in a comma separated list, and then, on the second line, extract all of the professions in a comma separated list from the following text:
    {content}"""

    payload = {
        "model": "llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": msg}],
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    print(response.text)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


def search(content: str):
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [{"role": "user", "content": content}],
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
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
st.html("<p>1. Enter a person's name.</p>")
st.html(
    "<p>2. If there are multiple results, use the additional fields to narrow down your search.</p>"
)
name = st.text_input("Enter a person's name:")
city = st.text_input("Enter a city:")
profession = st.text_input("Enter a profession:")
company = st.text_input("Enter a company:")

if st.button("Search"):
    if name:
        with st.spinner("Searching..."):
            term = ", ".join(
                list(filter(None, [name, f"in {city}", profession, company]))
            )

            # news = search(f"Find recent news mentioning {name}")
            # youtube = search(f"Find youtube for {term}")

            st.html("<h1>Report:</h1>")

            bio = search(f"Find bio for {term}")
            st.markdown(f"## bio:\n{bio}")

            linkedIn = search(f"Find LinkedIn for {term}")
            st.markdown(f"## linkedIn:\n{linkedIn}")

            twitter = search(f"Find Twitter for {term}")
            st.markdown("## twitter")
            st.markdown(twitter)
            st.html(f"<strong>Handles:</strong><ul>{extract_usernames(twitter)}</ul>")

            website = search(f"Find websites for {term}")
            st.markdown(f"## Website:\n{website}")

            # t = tags(f"{bio}\n{linkedIn}")
            t = tags(linkedIn)
            st.markdown(f"## Refine by tags:\n{t}")
            st.markdown(
                "The tags above would be used to refine the search. The app could make this easy, in this demo you need to copy and paste the tags into the search box and click search again."
            )
            # st.markdown(f"## Youtube:\n{youtube}")
    else:
        st.warning("Please enter a name.")
