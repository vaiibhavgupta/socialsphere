from datetime import datetime
import streamlit as st
import database

def birthday_from_dob(date_of_birth):
    """
    extracts the birthday in the format 'month day' from a given date of birth.
    
    input parameters:
        date_of_birth (str): the date of birth in the format 'YYYY-MM-DD'.
    
    returns:
        str: the birthday in the format 'month day'.
    """
    # convert the date_of_birth string to a datetime object
    dob_datetime = datetime.strptime(date_of_birth, '%Y-%m-%d')
    
    # extract the month and day
    birthday = dob_datetime.strftime('%B %-d')
    
    return birthday

def app(navigate_to):
    '''
    function that renders the login page
    input parameters:
        navigate_to: function to render the appropriate page basis user interaction
    '''

    session = st.session_state['SESSION']
    # creating a dictionary with the details of the current user for cleaner code
    current_user = {
        'name': st.session_state['CURRENT_USER']['name'],
        'bio': st.session_state['CURRENT_USER']['bio'],
        'education': st.session_state['CURRENT_USER']['education'],
        'occupation': st.session_state['CURRENT_USER']['occupation'],
        'date_of_birth': st.session_state['CURRENT_USER']['date_of_birth'],
        'birthday': birthday_from_dob(st.session_state['CURRENT_USER']['date_of_birth']),
        'location': st.session_state['CURRENT_USER']['location'],
        'interests': st.session_state['CURRENT_USER']['interests'],
        'email': st.session_state['CURRENT_USER']['email'],
        'username': st.session_state['CURRENT_USER']['username']
    }
    
    with st.container():
        col_1, col_2 = st.columns([1, 5])
        with col_1:
            # user details on the left sidebar
            st.markdown(f"<h1 style='color: white;'>{current_user['name']}</h1>", unsafe_allow_html=True)
            st.markdown("---")
            
            st.markdown(f"<h5 style='color: white;'>{current_user['bio']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>📍 {current_user['location']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>🎂 {current_user['birthday']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>🎓 {current_user['education']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>🧳 {current_user['occupation']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>📧 {current_user['email']}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: white;'>⭐ Interests:</h5>", unsafe_allow_html=True)
            for interest in current_user['interests']:
                st.markdown(f"<h5 style='color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp - {interest}</h5>", unsafe_allow_html=True)
            
        with col_2:
            with st.container():
                sub_col_1, _, _, sub_col_2, sub_col_3 = st.columns([3, 3, 3, 1, 1])

                with sub_col_1:
                    st.markdown("<h1 style='text-align: left; color: white;'>SocialSphere</h1>", unsafe_allow_html=True)

                with sub_col_2:
                    # the button that navigates to the search page
                    for i in range(2):
                        st.write("")
                    if st.button("Search Users"):
                        navigate_to('search')

                with sub_col_3:
                    # the button to logout from the account
                    for i in range(2):
                        st.write("")
                    if st.button("Logout"):
                        navigate_to('logout')

            st.markdown("---")

            with st.container():
                sub_col_2_1, sub_col_2_2 = st.columns([4, 1])

                with sub_col_2_1:

                    def empty_new_post_box():
                        database.create_new_post(session, current_user["username"], st.session_state["new_post"])
                        st.session_state["new_post"] = ""

                    # new post textbox
                    st.text_input("", placeholder="Create a new post... What's on your mind?", key="new_post", on_change=empty_new_post_box)

            st.markdown("---")

            # calling a function to fetch comments and posts (and number of likes) made by the current user and their friends
            df = database.fetch_posts_and_comments(session, current_user['username'])

            for idx1, row in df.iterrows():

                with st.container():
                    col_content_1, col_like_1 = st.columns([5, 1])

                    with col_content_1:
                        st.markdown(f"<h2 style='text-align: left; color: white;'>{row['post']['content']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h5 style='text-align: left; color: white;'>By: {row['creator']}</h6>", unsafe_allow_html=True)
                        st.markdown(f"<h5 style='text-align: left; color: white;'>Liked By: {row['like_on_post']}</h6>", unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"<h4 style='text-align: left; color: white;'>Comments:</h6>", unsafe_allow_html=True)
                    
                    with col_like_1:
                        for i in range(3):
                            st.write("")
                        
                        # button to like a post
                        if st.button("Like", key=row['post']['id']):
                            # updating the action in the database
                            database.update_number_of_likes(session, 'post', row['post']['id'], current_user['username'])
                            st.experimental_rerun()

                with st.container():
                    col_content_2, col_like_2 = st.columns([5, 1])
                    for (comment_creator, comment, likes_on_comment) in zip(row["comment_creators"], row["comments"], row["like_on_comments"]):
                        with col_content_2:
                            st.markdown(f"<h2 style='text-align: left; color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;{comment['text']}</h2>", unsafe_allow_html=True)
                            st.markdown(f"<h5 style='text-align: left; color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; By: {comment_creator}</h5>", unsafe_allow_html=True)
                            st.markdown(f"<h5 style='text-align: left; color: white;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Liked By: {likes_on_comment}</h5>", unsafe_allow_html=True)

                        with col_like_2:
                            for i in range(5):
                                st.write("")
                            
                            # button to like a comment
                            if st.button("Like", key=comment['id']):
                                # updating the action in the database
                                database.update_number_of_likes(session, 'comment', comment['id'], current_user['username'])
                                st.experimental_rerun()


                with st.container():

                    col_content_3, col_like_3 = st.columns([4, 1])

                    def empty_new_comment_box(widget_key):
                        database.create_new_comment(session, current_user["username"], widget_key, st.session_state[widget_key])
                        st.session_state[widget_key] = ""
                    
                    # textbox to create new comments
                    with col_content_3:
                        st.text_input("", placeholder="Add a new comment...", key=f"{row['post']['id']}_new_comment", args=[f"{row['post']['id']}_new_comment"], on_change=empty_new_comment_box)


                st.markdown('---')