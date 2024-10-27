# Import the necessary libraries
import streamlit as st
import csv

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

def display_cards(search_qs=''):
    print(f"displaying qs cards...with optional search term '{search_qs}'")

    with open('qs.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        
        col1, col2, col3 = st.columns(3, gap='small')
        p_container = st.container()
        col_index = 0
        i = 1

        for row in csvreader:
            qs_id = row[0]
            qs_title = row[1]
            qs_link = row[2]
            qs_authors = row[3]
            qs_summary = row[4]
            qs_categories = row[5]
            qs_status = row[6]

            if (search_qs == '') or (search_qs in qs_title or search_qs in qs_authors):
                with p_container:
                    col = col1 if col_index == 0 else col2 if col_index == 1 else col3 

                    qs_title_link = f"<a href='{qs_link}' target='_blank'>{qs_title}</a>"
                    col.markdown(f" > {qs_title_link}", unsafe_allow_html = True)
                    col.write(f"Author(s): {qs_authors}")

                    with col.expander(label='Summary'):
                        st.write(qs_summary)
                        st.markdown("___")
                        st.write(f"Categories: {qs_categories}")
                        st.write(f"Status: {qs_status}")
                    
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

    search_qs = st.text_input("Search by title or author(s)")
    display_cards(search_qs)

    st.markdown("___")
    st.caption(f"App developed by [Dash](https://www.linkedin.com/in/dash-desai/)")
