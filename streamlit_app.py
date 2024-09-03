# Import the necessary libraries
import streamlit as st
from urllib.request import urlopen
import glob

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
    }
    blockquote p {
        font-size: 30px;
        color: #FFFFFF;
    }
    [data-testid=stSidebar] {
        background-color: rgb(129, 164, 182);
        color: #FFFFFF;
    }
    [aria-selected="true"] {
         color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

def process_qs_files():
    rootdir = 'https://github.com/Snowflake-Labs/sfquickstarts/tree/master/site/sfguides/'
    rawdir  = 'https://raw.githubusercontent.com/Snowflake-Labs/sfquickstarts/master/site/sfguides/'
    files = glob.glob('**/*.md', recursive=True)
    qs = {}
    skipped_qs = []

    for file in files:
        if file.endswith(('.md', '.markdown')):
            filepath = rootdir+file
            rawpath = rawdir+file
            try:
                data = urlopen(rawpath).read(1000).decode('utf-8',errors='ignore').strip()
                lines = data.split("\n") # split it into lines
                author_names = None
                title = None
                id = None
                for line in lines:
                    # get id, author(s) and title
                    if line.startswith("id:"):
                        id = line.strip()[line.strip().find(" "):].strip()
                    elif line.startswith("author"):
                        author_names = line.strip()[line.strip().find(" "):].strip()
                    elif line.startswith("# "):
                        title = line.strip()[line.strip().find(" "):].strip()
                qs[file] = {'id': id, 'authors': author_names,'title': title,'path': filepath}
            except Exception as error:
                skipped_qs.append(f"{rawpath}: {error}")
    
    return qs,skipped_qs

def display_qs_as_blocks():
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0

    for k,v in qs.items():
        qs_id = v['id']
        qs_authors = v['authors']
        qs_title = v['title']
        qs_link = f"https://quickstarts.snowflake.com/guide/{qs_id}/index.html"

        with p_container:
            col = col1 if col_index == 0 else col2 if col_index == 1 else col3 
        
            col.markdown(" > " + qs_title)
            qs_tag = f"<a href=\'{qs_link['href']}\' target=\'_blank\'>Visit guide</a>"
            col.caption(f"{qs_tag}", unsafe_allow_html = True)
            col.write(qs_authors)
            
        if (i % 3) == 0:
            col1, col2, col3 = st.columns(3, gap='small')
            p_container = st.container()
            col_index = 0
        else:
            col_index += 1

repo_anaconda_com_url = 'https://repo.anaconda.com/pkgs/snowflake/'
qs,skipped_qs = process_qs_files()
display_qs_as_blocks()

with st.container():
    col1,col2,_,_ = st.columns([1,14,1,1],gap="large")
    with col2:
        st.header(f"QuickStart Guides on Snowflake")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.markdown("___")


