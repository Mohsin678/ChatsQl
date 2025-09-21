##

import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["use sqlite studentdb","connect to my sql connection"]
selected_opt = st.sidebar.radio(label="choose the db which u want tochoose",options=radio_opt)


if radio_opt.index(selected_opt)==1:
    db_url = MYSQL
    mysql_host = st.sidebar.text_input("provide host name")
    mysql_user = st.sidebar.text_input("please provide username")
    mysql_password = st.sidebar.text_input("my sql password",type="password")
    mysql_db = st.sidebar.text_input("mysql db")
else:
    db_url=LOCALDB

api_key = st.sidebar.text_input(label="groq key",type="password")

if not api_key:
    st.info("Please provide api key")
    st.stop()

if not db_url:
    st.info("please enter db info")
if not api_key:
    st.info("please provide apoi key")

llm = ChatGroq(groq_api_key = api_key,model ="Gemma2-9b-It",streaming=True)
@st.cache_resource(ttl="2h")
def configure_db(db_url,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_url==LOCALDB:
        dbfilepath = (Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    
    elif db_url==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("pls provide conection details")
            st.stop()
        else:
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
        
if db_url==MYSQL:
    db = configure_db(db_url,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db = configure_db(db_url)


#toolkit
toolkit = SQLDatabaseToolkit(db=db,llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("clear msg history"):
    st.session_state["messages"] = [{"role":"assistant","content":"how can i help u"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="ask anything from database")


if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)


    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
