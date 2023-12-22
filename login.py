import database
import streamlit as st

def app(navigate_to):
    '''
    function that renders the login page
    input parameters:
        navigate_to: function to render the appropriate page basis user interaction
    '''

    with st.container():
        st.markdown("<h1 style='text-align: center; color: white;'>SocialSphere</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<h4 style='text-align: center; color: white;'>Login to your account</h4>", unsafe_allow_html=True)
    
    with st.container():
        _, col_2_1, _ = st.columns([1, 2, 1])
        with col_2_1:
            username = st.text_input("", placeholder="Username")
            password = st.text_input("", placeholder="Password", type="password")

    login_output = None
    login_result = None
    with st.container():
        _, col_2_2 = st.columns([0.9, 1])

        with col_2_2:
            st.write("")
            st.write("")
            # login button that when clicked calls the function to perform credential validation
            if st.button("Login"):
                # validating the login credentials collected above
                login_result, user = database.validate_login_details(st.session_state['SESSION'], username, password)
                if login_result.startswith("Invalid"):
                    login_output = 'Error'
                elif login_result == "User Found. Logging In.":
                    login_output = 'Success'
                    st.session_state['CURRENT_USER'] = user
                    st.session_state['logged_in'] = True
                    # navigate to home page if login credentials are sucessfully validated
                    navigate_to('home')

    with st.container():
        _, col_2_3, _ = st.columns([1, 2, 1])
        with col_2_3:
            if login_output == 'Success':
                st.success(login_result)
            elif login_output == 'Error':
                st.error(login_result)
    
    st.markdown("---")
    # st.markdown("<h4 style='text-align: center; color: white;'>You can create a new account here.</h4>", unsafe_allow_html=True)