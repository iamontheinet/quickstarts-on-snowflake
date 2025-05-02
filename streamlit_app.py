# Import the necessary libraries
import streamlit as st
import csv
import re
from datetime import datetime

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
            # background-color: #249edc;
            height: 125px;
        }
        blockquote p {
            font-size: 25px;
            color: #ffffff;
        }
        a.published {
            color: #ffffff !important;
            text-decoration: none;
        }
        a.final {
            color: #ffffff !important;
            text-decoration: none;
        }
        a.hidden {
            color: red !important;
            text-decoration: none;
        }
        a.draft {
            color: #ffffff !important;
            text-decoration: none;
            font-style: italic;
        }
        a.updated {
            # color: #000000 !important;
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
        .st-b6 {
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

DEBUG = False
if DEBUG:
    DATA_FILE = 'qs_test.csv'
else:
    DATA_FILE = 'qs.csv'

def display_cards(search_qs='',selected_status='All',selected_order_by='Created date',selected_order='Desc'):
    search_qs = re.sub('[^0-9a-zA-Z]+', ' ', search_qs)
    search_qs = search_qs.lower()

    if selected_order_by == 'Title':
        col_idx = 1
    elif selected_order_by == 'Created date':
        col_idx = 7
    else:
        col_idx = 8
    
    with open(DATA_FILE) as csvfile:
        org_list = list(csv.reader(csvfile))
        data = []
        for qs in org_list:
            qs_title = qs[1]
            qs_authors = qs[3]
            qs_status = qs[6]
            if (qs_status != 'Archived') and ((search_qs == '') or (search_qs in qs_title.lower() or search_qs in qs_authors.lower())) and (qs_status.lower() == selected_status.lower() or selected_status == 'All'):
                data.append(qs)

        st.caption(f"Number of matching QS guides: {len(data)}")

        reverse_order = selected_order == "Desc"
        if col_idx == 1:
            sorted_data = sorted(data, key=lambda row: row[col_idx], reverse=reverse_order)
        else:
            try:
                sorted_data = sorted(data, key=lambda row: datetime.strptime(row[col_idx], "%b %d, %Y"), reverse=reverse_order)
            except:
                sorted_data = sorted(data, key=lambda row: row[col_idx], reverse=reverse_order)
                
    if DEBUG:
        print(f"\nUser params >> Search: {search_qs} | Status: {selected_status} | Order by: {selected_order_by} | Order: {selected_order}\n")
        print(sorted_data[:10])
    
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0
    i = 1

    for qs in sorted_data:
        qs_id = qs[0]
        qs_title = qs[1]
        qs_link = qs[2]
        qs_authors = qs[3]
        qs_summary = qs[4]
        qs_categories = qs[5]
        qs_status = qs[6]
        qs_md_first_updated = qs[7]
        qs_md_last_updated = qs[8]
        qs_md_last_updated_by = qs[9]

        with p_container:
            col = col1 if col_index == 0 else col2 if col_index == 1 else col3 

            col.write("<div style='border:1px solid #29b5e8'>", unsafe_allow_html = True)
            qs_title_link = f"<a class='{qs_status.lower()}' href='{qs_link}' target='_blank'>{qs_title}</a>"
            col.markdown(f" > {qs_title_link}", unsafe_allow_html = True)
            col.markdown(f"<h6>Author(s): {qs_authors}</h6>", unsafe_allow_html = True)
            col.markdown(f"<h6>Created date: {qs_md_first_updated}</h6>", unsafe_allow_html = True)
            col.markdown(f"<h6>Last updated date: {qs_md_last_updated} | Last updated by: <a class='updated' href='https://github.com/{qs_md_last_updated_by}'>{qs_md_last_updated_by}</a> </h6>", unsafe_allow_html = True)
            col.write("</div>", unsafe_allow_html = True)

            with col.expander(label='Summary'):
                st.write(qs_summary)
                st.markdown("___")
                st.write(f"Id: {qs_id}")
                st.write(f"Categories: {qs_categories}")
                st.write(f"Status: {qs_status}")
            
        if (i % 3) == 0:
            col1, col2, col3 = st.columns(3, gap='small')
            p_container = st.container()
            col_index = 0
        else:
            col_index += 1
        i += 1

    if DEBUG:
        print("done displaying qs cards!")

with st.container():
    st.header(f"QuickStart Guides on Snowflake")
    st.write(f"""
                <a href="https://www.snowflake.com/en/developers/solutions-center/?utm_cta=quickstarts_" target="_blank">Solutions Center</a>
                |
                <a href='https://quickstarts.snowflake.com/?utm_cta=quickstarts_' target='_blank'>QuickStarts official website</a> 
                |
                <a href='https://github.com/Snowflake-Labs/sfquickstarts/?utm_cta=quickstarts_' target='_blank'>QuickStarts on GitHub</a>
                |
                <a href='https://www.snowflake.com/virtual-hands-on-lab/?utm_cta=quickstarts_' target='_blank'>Virtual Hands-On Labs</a> 
            """,unsafe_allow_html=True)

    st.caption(f"App developed by [Dash](https://www.linkedin.com/in/dash-desai/)")
    st.markdown("___")

    col1, col2, col3, col4 = st.columns([3.2,1.5,1.8,.8])
    with col1:
        search_qs = st.text_input("Search by title or author(s)",placeholder="Enter title or author")
    with col2:
        selected_status = st.radio(
            "Filter by status",
            key="status_visibility",
            horizontal=True,
            options=['All','Published','Hidden'],
            index=1
        )
    with col3:
        selected_order_by = st.radio(
            "Sort by",
            key="order_by_visibility",
            horizontal=True,
            options=['Title','Created date','Last updated date'],
            index=1
        )
    with col4:
        selected_order = st.radio(
            "Sort order",
            key="order_visibility",
            horizontal=True,
            options=['Asc','Desc'],
            index=1
        )

    display_cards(search_qs,selected_status,selected_order_by,selected_order)

    st.markdown("___")
    st.caption(f"App developed by [Dash](https://www.linkedin.com/in/dash-desai/)")
