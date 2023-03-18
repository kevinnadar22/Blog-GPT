# Description: Streamlit app to generate blog posts using OpenAI GPT-3
# Author: Kevin Nadar

__title__ = "Blog GPT"
__author__ = "Kevin Nadar"


import os
import random
import string

import hydralit_components as hc
import openai
import streamlit as st

# Authenticate with OpenAI API using your API key
# (you can find your API key at https://openai.com/)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to generate blog post
menu_items = {
    'Get Help': 'https://telegram.me/ask_admin001',
    'Report a bug': "https://github.com/kevinnadar22/Blog-GPT/issues",
    'About': "Blog-GPT is a Github repository that generates high-quality blog content using the OpenAI GPT-3.5 API. With a simple prompt, users can quickly create engaging and informative posts without sacrificing quality. Ideal for bloggers and content creators looking to enhance their content creation process."
}


def generate_blog_post(title, body_snippet=None):
    # Set up the prompt for OpenAI
    prompt = f"Write a blog post titled '{title}'"
    if body_snippet:
        prompt += f" with the following body snippet: '{body_snippet}'"
    prompt += "."
    prompt += "If this doesn't seems like a blog post title or body snippet, simply reply with exactly 'Error'"
    prompt += "The post should be at least 300 words long"

    # Call OpenAI API to generate blog post
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    # Extract the generated text from the response
    generated_text = response.choices[0].message.content

    return generated_text


def download_button(generated_text):
    st.write("Click the button below to download the generated text.")
    random_string = "".join(random.choices(
        string.ascii_letters + string.digits, k=5))
    filename = f"generated_blog_post_{random_string}.txt"
    if st.download_button(
        label="Download Generated Text",
        data=generated_text,
        file_name=filename,
        mime="text/plain",
        key="download_button",
    ):

        with open(filename, "w") as f:
            f.write(generated_text)

        # Delete the generated text file after the download is finished
        if "download_button" in st.session_state and st.session_state.download_button:
            os.remove(filename)
            st.session_state.download_button = False


def post_process_text(generated_text):
    # Add a "Save to File" button to save the generated text to a file
    st.write("")
    download_button(generated_text)


# Define Streamlit app


def app():

    # Set app title and description
    st.set_page_config(page_title=__title__,
                       page_icon=":memo:", layout="centered", menu_items=menu_items)
    st.title(__title__)
    st.write("Enter the details below to generate a blog post using OpenAI.")

    title_placeholder = "Bitcoin is the future"
    body_snippet_placeholder = "Bitcoin is the future of money. It is the future of the world. It is the future of the universe. It is the future of everything."

    title = st.text_input("Title", placeholder=title_placeholder)
    body_snippet = st.text_area(
        "Body Snippet (Optional)", placeholder=body_snippet_placeholder)

    # Generate blog post and display to user
    if st.button("Clear", key="clear_results"):
        st.empty()

    if st.button("Generate Blog Post"):
        if title == "":
            st.error("Please enter a title for your blog post.", icon="❌")
        else:
            st.empty()
            # with st.spinner("Generating blog post..."):
            with hc.HyLoader('<h4>This may take a few minutes<h4>', hc.Loaders.standard_loaders, index=3, height=100):
                try:
                    generated_text = generate_blog_post(title, body_snippet)
                except Exception as e:
                    print(e)
                    st.error(
                        "An error occurred while generating the blog post. Please try again later.")
                    return

                if "error" in generated_text.lower():
                    st.error(
                        "Trye again with a different proper title or body snippet.")
                else:
                    st.success("Blog post generated successfully!")
                    # Define the content to be displayed
                    st.markdown(f"## {title}", unsafe_allow_html=True)
                    st.write(generated_text)
                    post_process_text(generated_text)
                    st.balloons()


# Run the app
if __name__ == "__main__":
    app()
