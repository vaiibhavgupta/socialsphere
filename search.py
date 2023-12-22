import database
import pandas as pd
import streamlit as st

def app(navigate_to):
    session = st.session_state['SESSION']
    # storing the username of the current user for cleaner code
    user_username = st.session_state['CURRENT_USER']['username']
    # updating st.session_state with relevant variables to store session data
    if "SEARCH_VALUE" not in st.session_state:
        st.session_state["SEARCH_VALUE"] = ""

    if 'DF_FRIENDS' not in st.session_state:
        st.session_state['DF_FRIENDS'] = pd.DataFrame()

    if 'DF_NOT_FRIENDS' not in st.session_state:
        st.session_state['DF_NOT_FRIENDS'] = pd.DataFrame()

    if 'TYPE_OF_QUERY' not in st.session_state:
        st.session_state['TYPE_OF_QUERY'] = ""

    if 'PRINT_INTERESTS' not in st.session_state:
        st.session_state['PRINT_INTERESTS'] = False

    with st.container(): 
        col_1, col_2 = st.columns([1, 5])
        with col_1:
            st.write(f"<h1 style='color: white;'>{st.session_state['CURRENT_USER']['name']}</h1>", unsafe_allow_html=True)
            st.markdown('---')
            # search criteria radio options that find users depending on current user's information
            st.markdown("<h4 style='text-align: left; color: white;'>Find Users by:</h4>", unsafe_allow_html=True)
            quick_search_by = st.radio("", ('1st Degree Friends', '2nd Degree Friends', 'My School', 'My Location', 'My Occupation', 'Similar Interests'))

            # calling different functions to get the list of the current user's friends and non-friends based on the selected radio button
            if quick_search_by == "1st Degree Friends":
                st.session_state['DF_FRIENDS'] = database.find_1st_degree_friends(session, user_username)
                st.session_state['DF_NOT_FRIENDS'] = pd.DataFrame()

            if quick_search_by == "2nd Degree Friends":
                st.session_state['DF_NOT_FRIENDS'] = database.find_2nd_degree_friends(session, user_username)
                st.session_state['DF_FRIENDS'] = pd.DataFrame()

            if quick_search_by == "My School":
                st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_school(session, user_username, st.session_state['CURRENT_USER']['education'])
                st.session_state['TYPE_OF_QUERY'] = "School"

            if quick_search_by == "My Location":
                st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_location(session, user_username, st.session_state['CURRENT_USER']['location'])
                st.session_state['TYPE_OF_QUERY'] = "Location"

            if quick_search_by == "My Occupation":
                st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_occupation(session, user_username, st.session_state['CURRENT_USER']['occupation'])
                st.session_state['TYPE_OF_QUERY'] = "Occupation"

            if quick_search_by == "Similar Interests":
                st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_similar_interests(session, user_username)
                st.session_state['PRINT_INTERESTS'] = True

            for i in range(3):
                st.write("")

            # display friends list on the left sidebar
            st.markdown(f"<h2 style='color: white;'>Your Friends:</h2>", unsafe_allow_html=True)
            st.markdown("---")
            for _, row in database.find_1st_degree_friends(session, user_username).iterrows():
                st.markdown(f"<h5 style='color: white;'> - {row[0]['name']}</h5>", unsafe_allow_html=True)
                st.write("")

        with col_2:
            with st.container():
                sub_col_1, sub_col_2 = st.columns([5, 1])

                with sub_col_1:
                    st.markdown("<h1 style='text-align: left; color: white;'>SocialSphere</h1>", unsafe_allow_html=True)

                with sub_col_2:
                    for i in range(2):
                        st.write("")
                    
                    # back to home button
                    if st.button("Back to Home"):
                        # resetting the search results and going back to home
                        st.session_state['DF_FRIENDS'] = pd.DataFrame()
                        st.session_state['DF_NOT_FRIENDS'] = pd.DataFrame()
                        navigate_to('home')


            st.markdown("---")

            with st.container():
                sub_col_2_1, sub_col_2_2 = st.columns([1, 4])
                # search criteria dropdown for advanced search options
                with sub_col_2_1:
                    search_criteria = st.selectbox("", ('Name', 'Username', 'Location', 'School', 'Occupation', 'Interest'), placeholder='Search Criteria', index=None)

                with sub_col_2_2:
                    
                    # function to reset the search textbox upon pressing enter and rendering results (if any)
                    def empty_search_box():
                        if search_criteria in ['Name', 'Username', 'Location', 'School', 'Occupation', 'Interest']:
                            st.session_state["SEARCH_VALUE"] = st.session_state["search_box"]
                            st.session_state["search_box"] = ""

                    # textbox to input the search value
                    st.text_input("", placeholder="...", key="search_box", on_change=empty_search_box)

                    # calling different functions to get the list of the current user's friends and non-friends based on the selected search criteria and input value
                    if st.session_state["SEARCH_VALUE"] != "":
                        st.session_state['PRINT_INTERESTS'] = False
                        if search_criteria == 'Name':
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_name(session, user_username, st.session_state["SEARCH_VALUE"])
                            st.session_state['TYPE_OF_QUERY'] = ""
                        elif search_criteria == 'Username':
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_username(session, user_username, st.session_state["SEARCH_VALUE"])
                            st.session_state['TYPE_OF_QUERY'] = ""
                        elif search_criteria == 'School':
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_school(session, user_username, st.session_state["SEARCH_VALUE"])
                            st.session_state['TYPE_OF_QUERY'] = "School"
                        elif search_criteria == 'Location':
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_location(session, user_username, st.session_state["SEARCH_VALUE"])
                            st.session_state['TYPE_OF_QUERY'] = "Location"
                        elif search_criteria == 'Occupation':
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_occupation(session, user_username, st.session_state["SEARCH_VALUE"])
                            st.session_state['TYPE_OF_QUERY'] = "Occupation"
                        elif search_criteria == "Interest":
                            st.session_state['PRINT_INTERESTS'] = True
                            st.session_state['DF_FRIENDS'], st.session_state['DF_NOT_FRIENDS'] = database.find_by_interest(session, user_username, st.session_state["SEARCH_VALUE"])

                st.markdown('---')
            
            with st.container():
                # iterating over query output (users who are friends of the current user) to render user information
                for idx, row in st.session_state['DF_FRIENDS'].iterrows():
                    sub_col_3_1, sub_col_3_2 = st.columns([5, 1])
                    with sub_col_3_1:
                        to_write = f"{row[0]['name']} ({row[0]['username']})"
                        st.markdown(f"<h5 style='text-align: left; color: white;'>{to_write}</h5>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "Location":
                            st.markdown(f"<h6 style='color: white;'>📍 {row[0]['location']}</h6>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "School":
                            st.markdown(f"<h6 style='color: white;'>🎓 {row[0]['education']}</h6>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "Occupation":
                            st.markdown(f"<h6 style='color: white;'>🧳 {row[0]['occupation']}</h6>", unsafe_allow_html=True)
                        if st.session_state['PRINT_INTERESTS']:
                            st.markdown(f"<h6 style='color: white;'>⭐ Interests:</h6>", unsafe_allow_html=True)
                            for interest in row[0]['interests']:
                                st.markdown(f"<h6 style='color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - {interest}</h6>", unsafe_allow_html=True)

                    with sub_col_3_2:
                        if st.session_state['PRINT_INTERESTS']:
                            for i in range(7):
                                st.write("")
                        else:
                            if st.session_state['TYPE_OF_QUERY'] == "":
                                for i in range(3):
                                    st.write("")
                            else:
                                for i in range(2):
                                    st.write("")
                            
                        # remove as friend button
                        if st.button("Remove Friend", key=row[0]['username']):
                            database.remove_friend(session, user_username, row[0]['username'])
                            st.experimental_rerun()
                
                    st.markdown('---')
                
                # iterating over query output (users who are not friends of the current user) to render user information
                for _, row in st.session_state['DF_NOT_FRIENDS'].iterrows():
                    sub_col_3_1, sub_col_3_2 = st.columns([5, 1])
                    with sub_col_3_1:
                        to_write = f"{row[0]['name']} ({row[0]['username']})"
                        st.markdown(f"<h5 style='text-align: left; color: white;'>{to_write}</h5>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "Location":
                            st.markdown(f"<h6 style='color: white;'>📍 {row[0]['location']}</h6>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "School":
                            st.markdown(f"<h6 style='color: white;'>🎓 {row[0]['education']}</h6>", unsafe_allow_html=True)
                        if st.session_state['TYPE_OF_QUERY'] != "Occupation":
                            st.markdown(f"<h6 style='color: white;'>🧳 {row[0]['occupation']}</h6>", unsafe_allow_html=True)
                        if st.session_state['PRINT_INTERESTS']:
                            st.markdown(f"<h6 style='color: white;'>⭐ Interests:</h6>", unsafe_allow_html=True)
                            for interest in row[0]['interests']:
                                st.markdown(f"<h6 style='color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp - {interest}</h6>", unsafe_allow_html=True)

                    with sub_col_3_2:
                        if st.session_state['PRINT_INTERESTS']:
                            for i in range(7):
                                st.write("")
                        else:
                            if st.session_state['TYPE_OF_QUERY'] == "":
                                for i in range(3):
                                    st.write("")
                            else:
                                for i in range(2):
                                    st.write("")
                        
                        # add as friend button
                        if st.button("Add Friend", key=row[0]['username']):
                            database.add_friend(session, user_username, row[0]['username'])
                            st.experimental_rerun()

                    st.markdown('---')