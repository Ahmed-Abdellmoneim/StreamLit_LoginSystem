import streamlit as st
import bcrypt          # This library for encoding the password to make it like the hashed password
from dbConnection import DatabaseSingleton

#--------------just testing if i can get all usernames from table user------------#

def get_all_usernames(connection):
    # SQL query to select all usernames from the 'user' table
    query = "SELECT username FROM user;" 
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        st.error(f"Error executing the SQL query: {e}")
        return None

# This will be written in the main():
# # Retrieve all usernames using the function
#     usernames = get_all_usernames(connection)

#     if usernames: # means if only one user is found 
#         st.write("Usernames:")
#         for username in usernames:
#             st.write(username[0])  # Assuming the username is the first column in the result
#     else:
#         st.write("No usernames found.")
#----------------------------------------------------------------------------------#


def main():

    db_singleton = DatabaseSingleton()
    connection = db_singleton.connect_to_database()
    if not connection.is_connected():
        st.error("Could not connect to the database")
        return

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logoutsection = st.container()

def login(username,password):
    db_singleton = DatabaseSingleton()
    connection = db_singleton.connect_to_database()
    cursor = connection.cursor()
    query = "SELECT firstname,password,usertype FROM user WHERE username = '{}'".format(username) 
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        stored_firstname, stored_password,usertype = result[0]
        if password==stored_password:
            return True,usertype,stored_firstname
    else:
        return False



#----------This section will be better in the front end when the user login and wants to logout---------#
def loggedOut_clicked():
    st.session_state['LoggedIn'] = False 

def show_logout():
    loginSection.empty()
    with logoutsection:
        st.button ("Log Out",key="logout",on_click=loggedOut_clicked)
#-------------------------------------------------------------------------------------------------------#

def LoggedIn_Clicked(userName,Password):
    result,usertype,firstname = login(userName,Password)
    if result:
        st.session_state['loggedIn'] = True
        if usertype == 'doctor':
            #redirect here
            st.subheader('here is the doctor page welcome '+firstname)
        else:
            #redirect here
            st.subheader('here is the pateint page welcome '+firstname)
    else:
        st.session_state['loggedIn'] = False
        st.warning('Invalid username or password') 

def show_login_page():
    with loginSection:
        if st.session_state['loggedIn']==False:
            userName= st.text_input (label="",value="",placeholder="Enter your user name")
            password = st.text_input(label="",value="",placeholder="Enter Password",type="password")
            st.button ("Login",key='login',on_click=lambda:LoggedIn_Clicked(userName,password))

with headerSection:
    # first run will have nothing in session_state
    # Am using the session state to manage and hide these two different containers 

    if 'loggedIn' not in st.session_state: # law l status bt3tu msh logged in 5las hazherlo l login page
        st.session_state['loggedIn'] = False
        st.title('Welcome to our meal recommendation!')
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            pass
            #here will make an sql query to know if he is a doctor or pateint then redirect him to his page
        else:
            st.title('Welcome to our meal recommendation!')
            show_login_page()

if __name__ == "__main__": # means look for the main function and then doit
    main()