import streamlit as st

def about_me():
    st.title("About Me")
    # General information about the author
    st.markdown(
        """
        Hello, I'm Jun Yip, a final year BCSI (Software Engineering) student studying at Inti International University. 
        I have a passion for AI projects and enjoy working on Sentimental Analysis Systems.

        This Streamlit app is a part of my exploration in creating interactive and data-driven web applications. 
        Feel free to explore the different sections and features.

        If you have any questions or feedback, please don't hesitate to [contact me](mailto:makatomfjy@gmail.com).

        Enjoy your time exploring the app!
        """
    )

    # Citation
    st.markdown(
        """
        **Citation:**
        If you find this app useful or use it in your work, please consider citing it. 
        You can use the following BibTeX entry:

        ```
        @misc{your_name_streamlit_app,
            title={Sentimental Analysis Dashboard System},
            author={JUN YIP FONG},
            year={2023},
            publisher={GitHub},
            journal={GitHub Repository},
            howpublished={\url{https://github.com/martinfjy/sentiment-analysis-project}},
        }
        ```
        """
    )

if __name__ == "__main__":
    about_me()