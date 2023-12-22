<!-- To preview this file, open it in VS Code, and press Ctrl+Shift+V (on Windows/Linux) or Cmd+Shift+V (on Mac).  -->
# DS5760 Final Project - SocialSphere

## About

The project aims to develop a social networking application with Python and Neo4j.

## Requirements

- Docker
- Python 3.9
    - Neo4j
    - Streamlit
    - Pandas

## Setup Instructions:

1. Download all the files in the folder and navigate to the download location in your local and open a terminal window and follow the following commands. `cd` into the directory

   `cd socialsphere`

2. Install dependencies

   `pip install -r requirements.txt`

3. Start the docker container (neo4j)

   `docker-compose up`

4. Import data into neo4j: Open `data_import.ipynb` and run all the cells. (Make sure that the notebook environment has requirements installed)

5. Run Streamlit Application

   `streamlit run app.py`

## About the Application:

1. Get any user's username and password from `data_import.ipynb` and login with their credentials. Click on the login button to log in to their account.

2. On the Home page and the Search Users page, at the press of the `Enter`, the values in the textfield that asks for posts/comments and search value for advanced search gets submitted and queries are run.

3. On the Search Users page, you have to UNSELECT the criteria from the dropdown menu to search users by shortcuts (radio buttons) present on the left sidebar.

## Database Design

The graph database consists of 3 Nodes and 4 Edges as follows:

Nodes:

1. `User` - Stores user information. Attributes:

    - username: str
    - password: str
    - name: str
    - email: str
    - date_of_birth: str
    - location: str
    - interests: list[str]
    - bio: str
    - education: str
    - occupation: str

2. `Post` - Stores information about user-created posts. Attributes:

    - id: str
    - content: str
    - timestamp: str (not stored for newly created posts from the streamlit application)

3. `Comment` - Stores information about users' comments on posts. Attributes:

    - id: str
    - text: str
    - timestamp: str (not stored for newly created comments from the streamlit application)

Edges:

1. `IS_FRIEND_OF`: Connects `User` to `User` who are friends of each other.

2. `CREATED`: Connects `Post` or `Comment` to the `User` who has created the `Post` or `Comment`.
    - `Post` to the `User` that created it.
    - `Comment` to the `User` that created it.

3. `LIKED`: Connects `Post` or `Comment` to the `User`(s) who have liked the `Post` or `Comment`.
    - `Post` to the `User` that liked it.
    - `Comment` to the `User` that liked it.

4. `HAS_COMMENT`: Connects `Post` to `Comment`(s) that users have created in response to the `Post`.
    - `Post` to its `Comment`.

## Use of Generative AI

I have used ChatGPT to generate **ALL** the data. Due to this data may have some inconsistencies where non-friend users may have commented or liked a post or comment. But filters are in place to not reflect this data on the front-end. Only the comments and likes by the friend of the creator are allowed and displayed.