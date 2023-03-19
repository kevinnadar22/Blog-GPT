# Description: Streamlit app to generate blog posts using OpenAI GPT-3
# Author: Kevin Nadar

__title__ = "Blog GPT"
__author__ = "Kevin Nadar"


from datetime import datetime
import os
import random
import string
import openai
import streamlit as st

# Authenticate with OpenAI API using your API key
# (you can find your API key at https://openai.com/)
openai.api_key = os.getenv(
    "OPENAI_API_KEY")

# Define function to generate blog post
menu_items = {
    'Get Help': 'https://telegram.me/ask_admin001',
    'Report a bug': "https://github.com/kevinnadar22/Blog-GPT/issues",
    'About': "Blog-GPT is a Github repository that generates high-quality blog content using the OpenAI GPT-3.5 API. With a simple prompt, users can quickly create engaging and informative posts without sacrificing quality. Ideal for bloggers and content creators looking to enhance their content creation process."
}


def generate_blog_post(title, body_snippet=None, length=300, num_samples=1) -> list:
    # Set up the prompt for OpenAI
    prompt = f"Write a blog post titled '{title}'"
    if body_snippet:
        prompt += f" with the following body snippet: '{body_snippet}'"
    prompt += "."
    prompt += "If inputs doesn't seems like blog post title or body snippet, simply reply with exactly 'Error'"
    prompt += f"The post should be at least {length} words long"
    for i in range(num_samples):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        generated_text_ = ""
        generated_text_ += f"\n\n### Variant {i+1} of {num_samples}"
        generated_text_ += response.choices[0].message.content
        yield generated_text_


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
    st.sidebar.title("Customize Settings")
    length = st.sidebar.slider(
        "Blog Post Length", min_value=100, max_value=1000, value=500, step=50)
    num_posts = st.sidebar.slider(
        "Number of Blog Posts", min_value=1, max_value=5, value=1)
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
            with st.spinner("Generating blog post, This may take a while..."):
                st.caption(
                    "Don't close the tab, it will take some time to generate the blog post. (It may take upto 1 minute to generate the blog post.)")
                now = datetime.now()
                try:
                    res: list = generate_blog_post(
                        title, body_snippet, length, num_posts)

                    st.markdown(f"## {title}", unsafe_allow_html=True)
                    i = 1
                    generated_text = ""
                    for text in res:
                        if "Error" in text:
                            text = text.replace(
                                "Error", "`Something went wrong`")
                        # Define the content to be displayed
                        st.write(text, unsafe_allow_html=True)
                        generated_text += text
                        i += 1

                except Exception as e:
                    print(e)
                    st.error(
                        "An error occurred while generating the blog post. Please try again later.")
                    return

                else:

                    end_time = datetime.now()
                    time_taken = end_time - now
                    st.success(
                        f"Blog post generated successfully! - Time Taken: {time_taken.total_seconds()} seconds")
                    post_process_text(generated_text)
                    st.balloons()

    st.markdown('---')
    st.markdown('Created by [Kevin](https://github.com/kevinnadar22)')


# Run the app
if __name__ == "__main__":
    app()
