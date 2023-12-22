import neo4j
import streamlit as st
import login, home, search

st.set_page_config(layout="wide")

def navigate_to(page):
    '''
    function to navigate through the application
    '''
    if page == 'logout':
        st.session_state['logged_in'] = False
        st.session_state['current_page'] = 'login'
    else:
        st.session_state['current_page'] = page
    st.experimental_rerun()

def connect_db():
    '''
    function to create a client to neo4j.
    '''
    driver = neo4j.GraphDatabase.driver(uri="neo4j://0.0.0.0:7687", auth=("neo4j","password"))
    session = driver.session(database="neo4j")
    return session

# defining a variable in session_state to store neo4j's session details
st.session_state['SESSION'] = connect_db()

# initialize session state for navigation and login status
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# routing logic based on session state
if st.session_state['current_page'] == 'login':
    login.app(navigate_to)
elif st.session_state['current_page'] == 'home' and st.session_state['logged_in']:
    home.app(navigate_to)
elif st.session_state['current_page'] == 'search' and st.session_state['logged_in']:
    search.app(navigate_to)
else:
    # if not logged in, always navigate back to login page
    st.session_state['current_page'] = 'login'
    st.experimental_rerun()