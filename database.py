import neo4j
import pandas as pd

def validate_login_details(session, username, password):
    '''
    function to validate login detail
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - password: account password of the current user
    return parameters:
        - message: string output
        - user: validated User node
    '''
    query = '''
    MATCH (user:User {username: $username})
    RETURN user
    '''
    user = pd.DataFrame(session.run(query, username=username))
    if user.shape != (1, 1):
        return "Invalid Username. Please Try Again.", dict()
    if password != user[0][0]['password']:
        return "Invalid Password. Please Try Again.", dict()

    user = user[0][0]
    user = {'education': user['education'], 'occupation': user['occupation'], 'date_of_birth': user['date_of_birth'], 'name': user['name'], 'bio': user['bio'], 'location': user['location'], 'interests': user['interests'], 'email': user['email'], 'username': user['username']}
    
    return "User Found. Logging In.", user

def find_1st_degree_friends(session, username):
    '''
    function to find first degree friends
    input parameters:
        - session: neo4j client
        - username: username of the current user
    return parameters:
        - df: dataframe with quried nodes
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(friends: User)
    RETURN DISTINCT friends
    '''
    df = pd.DataFrame(session.run(query, username=username))
    return df

def find_2nd_degree_friends(session, username):
    '''
    function to find second degree friends
    input parameters:
        - session: neo4j client
        - username: username of the current user
    return parameters:
        - df: dataframe with quried nodes
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(friends: User)-[:IS_FRIEND_OF]->(friends_of_friends: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(friends_of_friends)
        AND current_user <> friends_of_friends
    RETURN DISTINCT friends_of_friends
    '''
    df = pd.DataFrame(session.run(query, username=username))
    return df

def find_by_name(session, username, name):
    '''
    function to find user by their name
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - name: name of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND users.name = $name
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, name=name))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND users.name = $name
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, name=name))
    return df_friends, df_not_friends

def find_by_username(session, username, username_to_search):
    '''
    function to find users by their username
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - username_to_search: username of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User {username: $username_to_search})
    WHERE users.username <> $username
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, username_to_search=username_to_search))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User {username: $username_to_search})
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, username_to_search=username_to_search))
    return df_friends, df_not_friends

def find_by_school(session, username, school):
    '''
    function to find users by their school
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - school: school of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND users.education = $education
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, education=school))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND users.education = $education
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, education=school))
    return df_friends, df_not_friends

def find_by_location(session, username, location):
    '''
    function to find users by their location
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - location: location of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND users.location = $location
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, location=location))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND users.location = $location
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, location=location))
    return df_friends, df_not_friends

def find_by_occupation(session, username, occupation):
    '''
    function to find users by their occupation
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - occupation: occupation of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND users.occupation = $occupation
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, occupation=occupation))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND users.occupation = $occupation
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, occupation=occupation))
    return df_friends, df_not_friends

def find_by_interest(session, username, target_interest):
    '''
    function to find users by their interest
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - target_interest: interest of the user to find
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND ANY(interest IN $target_interest WHERE interest IN users.interests)
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username, target_interest=[target_interest]))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND ANY(interest IN $target_interest WHERE interest IN users.interests)
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username, target_interest=[target_interest]))
    return df_friends, df_not_friends

def find_by_similar_interests(session, username):
    '''
    function to find users with similar interest to the current user
    input parameters:
        - session: neo4j client
        - username: username of the current user
    return parameters:
        - df_friends: dataframe with quried nodes who are friends of the current user
        - df_not_friends: dataframe with quried nodes who are not friends of the current user
    '''

    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(users: User)
    WHERE users.username <> $username AND ANY(interest IN current_user.interests WHERE interest IN users.interests)
    RETURN DISTINCT users
    '''
    df_friends = pd.DataFrame(session.run(query, username=username))

    query = '''
    MATCH (current_user: User {username: $username}), (users: User)
    WHERE NOT (current_user)-[:IS_FRIEND_OF]->(users)
        AND users.username <> $username 
        AND ANY(interest IN current_user.interests WHERE interest IN users.interests)
    RETURN DISTINCT users
    '''
    df_not_friends = pd.DataFrame(session.run(query, username=username))
    return df_friends, df_not_friends

def add_friend(session, username, friend_username):
    '''
    a function to add an IS_FRIEND edge between teo User nodes.
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - friend_username: username of the other user whom the current user added as a friend
    '''
    query = '''
    MATCH (current_user: User {username: $username}), (friend_user: User {username: $friend_username})
    MERGE (current_user)-[:IS_FRIEND_OF]->(friend_user)
    '''
    session.run(query, username=username, friend_username=friend_username)    
    return None

def remove_friend(session, username, friend_username):
    '''
    a function to remove an IS_FRIEND edge between teo User nodes.
    input parameters:
        - session: neo4j client
        - username: username of the current user
        - friend_username: username of the other user whom the current user added as a friend
    '''
    query = '''
    MATCH (current_user: User {username: $username})-[friendship: IS_FRIEND_OF]->(friend_user: User {username: $friend_username})
    DELETE friendship
    '''
    session.run(query, username=username, friend_username=friend_username)    
    return None

def fetch_posts_and_comments(session, username):
    '''
    a function to fetch posts and comments and likes by the current user and their friends.
    input parameters:
        - session: neo4j client
        - username: username of the current user
    '''

    df = pd.DataFrame(columns = ['creator', 'post', 'like_on_post', 'comment_creators', 'comments', 'like_on_comments'])

    # fetch posts made by 1st degree friends of the current user
    query = '''
    MATCH (current_user: User {username: $username})-[:IS_FRIEND_OF]->(friends: User)
    MATCH (friends)-[:CREATED]->(post: Post)
    RETURN friends, post
    '''
    output0 = pd.DataFrame(session.run(query, username=username))

    # fetch posts made by the current user
    query = '''
    MATCH (current_user: User {username: $username})-[:CREATED]->(post: Post)
    RETURN current_user, post
    '''
    output1 = pd.DataFrame(session.run(query, username=username))

    output = pd.concat([output1, output0])
    output.reset_index(drop=True, inplace=True)

    # returning empty dataframe if no posts found. this could occue 
    if output.shape == (0, 0):
        return df

    # fetching the post node and the name of the creator into the dataframe to be returned
    df['creator'] = [f"{out['name']}" for out in output[0]]
    df['post'] = output[1]

    for idx, row in df.iterrows():
        post_id = row['post']['id']

        # number of likes on a post
        query = '''
        MATCH (:Post {id: $post_id})<-[:LIKED]-(users: User)
        RETURN COUNT(users)
        '''
        df['like_on_post'][idx] = pd.DataFrame(session.run(query, post_id=post_id))[0][0]

        # fetch comments a post
        query = '''
        MATCH (post: Post {id: $post_id})-[:HAS_COMMENT]->(comment: Comment)
        RETURN comment
        '''
        
        output = pd.DataFrame(session.run(query, post_id=post_id))
        
        if output.shape == (0, 0):
            df['comments'][idx] = pd.Series()
        else:
            df['comments'][idx] = output[0]

    for idx, row in df.iterrows():
        like_on_comments = list()
        comment_creators = list()
        for comment in row['comments']:
            comment_id = comment['id']

            # fetch creator of a comment
            query = '''
            MATCH (:Comment {id: $comment_id})<-[:CREATED]-(creator: User)
            RETURN creator
            '''
            output = pd.DataFrame(session.run(query, comment_id=comment_id))
            comment_creators.append(f"{output[0][0]['name']}")

            # fetch number of likes on a comment
            query = '''
            MATCH (:Comment {id: $comment_id})<-[:LIKED]-(users: User)
            RETURN COUNT(users)
            '''
            like_on_comments.append(pd.DataFrame(session.run(query, comment_id=comment_id))[0][0])
        
        df['like_on_comments'][idx] = like_on_comments
        df['comment_creators'][idx] = comment_creators
    
    return df

def update_number_of_likes(session, item_type, item_id, username):
    '''
    function to update the number of likes on a post / comment
    input parameters:
        - session: neo4j client
        - item_type: comment / post
        - item_id: id of the comment / post
        - username: username of the current user who liked the post / comment
    '''
    if item_type == 'post':
        query = '''
        MATCH (current_user: User {username: $username}), (post_to_like: Post {id: $item_id})
        MERGE (current_user)-[:LIKED]->(post_to_like)
        '''
        session.run(query, username=username, item_id=item_id)    
    elif item_type == 'comment':
        query = '''
        MATCH (current_user: User {username: $username}), (comment_to_like: Comment {id: $item_id})
        MERGE (current_user)-[:LIKED]->(comment_to_like)
        '''
        session.run(query, username=username, item_id=item_id)    

    return None

def create_new_post(session, username, content):
    '''
    function to create a new post
    input parameters:
        - session: neo4j client
        - username: username of the current user who liked the post / comment
        - content: content of the post
    '''
    # get new id for the new post
    query = '''
    MATCH (posts: Post)
    return posts.id
    '''
    new_post_id = max(pd.DataFrame(session.run(query))[0].str.replace('post', '').astype(int)) + 1
    # create node and edge
    query = '''
    MATCH (current_user: User {username: $username})
    CREATE (p: Post {id: $new_post_id, content: $content})
    CREATE (current_user)-[:CREATED]->(p)
    '''

    session.run(query, username=username, new_post_id='post'+str(new_post_id), content=content)
    return None

def create_new_comment(session, username, widget_key, comment_text):
    '''
    function to create a new comment
    input parameters:
        - session: neo4j client
        - username: username of the current user who liked the post / comment
        - key to get comment id from
        - comment_text: content of the post
    '''
    # get new id for the new comment
    query = '''
    MATCH (comments: Comment)
    return comments.id
    '''
    new_comment_id = max(pd.DataFrame(session.run(query))[0].str.replace('comment', '').astype(int)) + 1
    post_id = widget_key.split('_')[0]
    # create node and edge
    query = '''
    MATCH (current_user: User {username: $username}), (p: Post {id: $post_id})
    CREATE (c: Comment {id: $new_comment_id, text: $comment_text})
    CREATE (current_user)-[:CREATED]->(c)
    CREATE (p)-[:HAS_COMMENT]->(c)
    '''
    
    session.run(query, username=username, post_id=post_id, new_comment_id="comment"+str(new_comment_id), comment_text=comment_text)
    return None