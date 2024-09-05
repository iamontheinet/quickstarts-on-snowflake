# Import the necessary libraries
import streamlit as st
from bs4 import BeautifulSoup
from github import Auth
from github import Github
import requests
import re

# Setup web page
st.set_page_config(
     page_title="QuickStart Guides on Snowflake",
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com'
     }
)

st.markdown("""
    <style type="text/css">
        blockquote {
            margin: 1em 0px 1em -1px;
            padding: 0px 0px 0px 1.2em;
            font-size: 20px;
            border-left: 5px solid rgb(230, 234, 241);
            # background-color: rgb(129, 164, 182);
            height: 125px;
        }
        blockquote p {
            font-size: 25px;
            color: #ffffff;
        }
        a {
            color: #ffffff !important;
            text-decoration: none;
        }
        p {
            color: rgb(129, 164, 182);
        }
        [aria-selected="true"] {
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=True)
def get_qs_md_files():
    print("processing .md files...")
    # qs_md_files = ['ask-questions-to-your-documents-using-rag-with-snowflake-cortex-search/ask_questions_to_your_own_documents_with_snowflake_cortex_search.md',
    #       'getting_started_with_dataengineering_ml_using_snowpark_python/getting_started_with_dataengineering_ml_using_snowpark_python.md',
    #       'getting_started_with_snowflake_arctic/getting_started_with_snowflake_arctic.md',
    #       'build_genai_inpainting_and_hybridtable_app_in_snowpark_container_services/build_genai_inpainting_and_hybridtable_app_in_snowpark_container_services.md',
    #       'ask-questions-to-your-documents-using-rag-with-snowflake-cortex/ask-questions-to-your-documents-using-rag-with-snowflake-cortex.md']

    qs_md_files = []
    skipped_content = []
    auth = Auth.Token(st.secrets["G_TOKEN"])
    g = Github(auth=auth)

    repo = g.get_repo('Snowflake-Labs/sfquickstarts')
    qs_guides = repo.get_contents("site/sfguides/src")
    for qs_guide in qs_guides:
        qs_guide_contents = repo.get_contents(qs_guide.path)
        try:
            for qs_guide_content in qs_guide_contents:
                if qs_guide_content.path.endswith(".md"):
                    md_path = qs_guide_content.path
                    qs_md_files.append(md_path)
                    # print(md_path)
        except Exception as e:
            # print(f">>>>>> skipping: {qs_guide_contents}")
            skipped_content.append(qs_guide_contents)

    qs_md_files.sort()
    print("done processing .md files!")
    # print(qs_md_files)
    return qs_md_files

def display_qs_as_blocks():
    print("displaying qs guides...")
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0
    i = 1
    skipped_items = []
    rawdir  = 'https://raw.githubusercontent.com/Snowflake-Labs/sfquickstarts/master/'
 
    qs_md_files = get_qs_md_files()
    for qs_md_file in qs_md_files:
        try:
            response = requests.get(rawdir+qs_md_file)
            qs_md = BeautifulSoup(response.content, 'html.parser').text
            qs_md_metadata = qs_md[0:qs_md.index("#")].split('\n')
            qs_md_metadata = list(filter(None, qs_md_metadata))
            # print(qs_md_metadata)
            qs_title = qs_md[qs_md.index("#")+1:qs_md.index("##")]
            qs_title = re.sub('[^0-9a-zA-Z]+', ' ', qs_title)

            qs_id = ''
            qs_link = ''
            qs_authors = 'N/A'

            if len(qs_title) > 1:
                for item in qs_md_metadata:
                    k_v = item.rsplit(":")
                    k = k_v[0].strip()
                    v = k_v[1].strip() if len(k_v) > 1 else ''
                    # print(f"{k}: {v}")

                    if k == 'id':
                        qs_id = v 
                        qs_link = f"https://quickstarts.snowflake.com/guide/{qs_id}/index.html"
                    elif k == 'author' or k == 'authors':
                        qs_authors = v 

                with p_container:
                    col = col1 if col_index == 0 else col2 if col_index == 1 else col3 
                
                    qs_tag = f"<a href='{qs_link}' target='_blank'>{qs_title}</a>"
                    col.markdown(f" > {qs_tag}", unsafe_allow_html = True)
                    col.write(f"Author(s): {qs_authors}")
                    
                if (i % 3) == 0:
                    col1, col2, col3 = st.columns(3, gap='small')
                    p_container = st.container()
                    col_index = 0
                else:
                    col_index += 1
                i += 1

        except Exception as e:
            # print(f"Skipping {qs_md_file}")
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
            skipped_items.append(qs_md_file)

    print(f">>> skipped {len(skipped_items)} qs guides")
    print("done displaying qs guides!")

with st.container():
    st.header(f"QuickStart Guides on Snowflake")
    st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
    st.markdown("___")

display_qs_as_blocks()
