# Import the necessary libraries
import streamlit as st
from bs4 import BeautifulSoup
from github import Auth
from github import Github
import requests
import re

# Setup web page
st.set_page_config(
     page_title="Getting Started with Snowflake",
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
        div[data-testid='stExpanderDetails'] p {
            color: #ffffff;
        }
        input {
            background-color: #115675 !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_qs_md_files(test_mode=False):
    print(f"processing .md files...")
    qs_md_files = []
    if test_mode:
        qs_md_files = ['site/sfguides/src/ask-questions-to-your-documents-using-rag-with-snowflake-cortex-search/ask_questions_to_your_own_documents_with_snowflake_cortex_search.md',
              'site/sfguides/src/getting_started_with_dataengineering_ml_using_snowpark_python/getting_started_with_dataengineering_ml_using_snowpark_python.md',
              'site/sfguides/src/getting_started_with_snowflake_arctic/getting_started_with_snowflake_arctic.md',
              'site/sfguides/src/build_genai_inpainting_and_hybridtable_app_in_snowpark_container_services/build_genai_inpainting_and_hybridtable_app_in_snowpark_container_services.md',
              'site/sfguides/src/ask-questions-to-your-documents-using-rag-with-snowflake-cortex/ask-questions-to-your-documents-using-rag-with-snowflake-cortex.md']
    else:
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
            except Exception as e:
                skipped_content.append(qs_guide_contents)

    qs_md_files.sort()
    print("done processing .md files!")
    return qs_md_files

def display_qs_as_cards(test_mode=False):
    print("processing qs guides...")
    skipped_items = []

    if len(qs_cards) <= 0:
        print(">>> creating qs cards...")
        rawdir  = 'https://raw.githubusercontent.com/Snowflake-Labs/sfquickstarts/master/'
    
        qs_md_files = get_qs_md_files(test_mode)
        for qs_md_file in qs_md_files:
            try:
                response = requests.get(rawdir+qs_md_file)
                qs_md = BeautifulSoup(response.content, 'html.parser').text
                qs_md_metadata = qs_md[0:qs_md.index("#")].split('\n')
                qs_md_metadata = list(filter(None, qs_md_metadata))
                # print(qs_md_metadata)
                qs_title = qs_md[qs_md.index("#")+1:qs_md.index("##")]
                qs_title = re.sub('[^0-9a-zA-Z]+', ' ', qs_title)

                qs_authors,qs_id,qs_link,qs_summary,qs_categories,qs_status = ['N/A','','','','','']

                if len(qs_title) > 1:
                    for item in qs_md_metadata:
                        k_v = item.rsplit(":")
                        k = k_v[0].strip()
                        v = k_v[1].strip() if len(k_v) > 1 else 'N/A'
                        # print(f"{k}: {v}")

                        if k == 'id':
                            qs_id = v 
                            qs_link = f"https://quickstarts.snowflake.com/guide/{qs_id}/index.html"
                        elif k == 'author' or k == 'authors':
                            qs_authors = v 
                        elif k == 'summary':
                            qs_summary = v
                        elif k == 'categories':
                            qs_categories = v
                        elif k == 'status':
                            qs_status = v

                    qs_cards[qs_title] = {"id": qs_id, "link": qs_link, "authors": qs_authors, "summary": qs_summary, "categories": qs_categories, "status": qs_status}
            except Exception as e:
                print(f"Skipping {rawdir+qs_md_file}")
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
                skipped_items.append(qs_md_file)

        st.session_state['qs_cards'] = qs_cards

    display_cards()
    print(f">>> skipped {len(skipped_items)} qs guides")
    print("done processing qs guides!")

def display_cards(search_qs=''):
    if len(qs_cards) > 0:
        print(f"displaying qs cards...with optional search term '{search_qs}'")
        col1, col2, col3 = st.columns(3, gap='small')
        p_container = st.container()
        col_index = 0
        i = 1
        for k in qs_cards.keys():
            if (search_qs == '') or (search_qs in k or search_qs in qs_cards[k]['authors']):
                with p_container:
                    col = col1 if col_index == 0 else col2 if col_index == 1 else col3 

                    qs_title_link = f"<a href='{qs_cards[k]['link']}' target='_blank'>{k}</a>"
                    col.markdown(f" > {qs_title_link}", unsafe_allow_html = True)
                    col.write(f"Author(s): {qs_cards[k]['authors']}")

                    with col.expander(label='Summary'):
                        st.write(qs_cards[k]['summary'])
                        st.markdown("___")
                        st.write(f"Categories: {qs_cards[k]['categories']}")
                        st.write(f"Status: {qs_cards[k]['status']}")
                    
                if (i % 3) == 0:
                    col1, col2, col3 = st.columns(3, gap='small')
                    p_container = st.container()
                    col_index = 0
                else:
                    col_index += 1
                i += 1

    print("done displaying qs cards!")

with st.container():
    st.header(f"Getting Started with Snowflake")
    st.write(f"""
                <a href='https://github.com/Snowflake-Labs/sfquickstarts' target='_blank'>Snowflake QuickStarts on GitHub</a>
                |
                <a href='https://www.snowflake.com/virtual-hands-on-lab' target='_blank'>Virtual Hands-On Labs</a> 
                |
                <a href='https://signup.snowflake.com/?utm_cta=quickstarts_' target='_blank'>Snowflake Free Trial</a>
            """,unsafe_allow_html=True)

    if 'qs_cards' not in st.session_state:
        st.session_state['qs_cards'] = {}
        qs_cards = {}
    else:
        qs_cards = st.session_state['qs_cards']

    search_qs = st.text_input("Search")
    if search_qs:
        display_cards(search_qs)
    else:
        display_qs_as_cards(test_mode=True)

    st.markdown("___")
    st.caption(f"App developed by [Dash](https://www.linkedin.com/in/dash-desai/)")
    




