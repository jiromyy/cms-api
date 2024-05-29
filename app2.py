from src.utils import ContentManagerUtilities
from src.blob_manager import BlobManager
from src.index_manager import IndexManager
import streamlit as st
import pandas as pd
from dateutil import tz
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv('.env.development', override=True)

aisearch_migo_index = os.getenv("MIGO_AZURE_AI_SEARCH_INDEX_NAME")
print(aisearch_migo_index)

aisearch_service_migo_endpoint = os.getenv("MIGO_AZURE_AI_SEARCH_ENDPOINT")
aisearch_key_migo = os.getenv("MIGO_AZURE_AI_SEARCH_API_KEY")

blob_migo_connection_string = os.getenv("MIGO_AZURE_STORAGE_ACCOUNT_CONNECTION_STRING")

blob_migo_name_ccu = os.getenv("CCU_AZURE_BLOB_CCU_CONTAINER_NAME")
blob_migo_name_aspen = os.getenv("CCU_AZURE_BLOB_ASPEN_CONTAINER_NAME")
blob_migo_name_rrhi = os.getenv("CCU_AZURE_BLOB_RRHI_CONTAINER_NAME")
blob_migo_name_rlc = os.getenv("CCU_AZURE_BLOB_RLC_CONTAINER_NAME")
blob_migo_name_jgsoc = os.getenv("CCU_AZURE_BLOB_JGSOC_CONTAINER_NAME")
blob_migo_name_preprocessing = os.getenv("CCU_AZURE_BLOB_PREPROCESS_CONTAINER_NAME")

blob_migo_name = {
    "ccu": blob_migo_name_ccu,
    "aspen": blob_migo_name_aspen,
    "rrhi": blob_migo_name_rrhi,
    "rlc": blob_migo_name_rlc,
    "jgsoc": blob_migo_name_jgsoc
}

functions = ["Finance", "HR", "IT", "Legal"]


blob_migo_link = os.getenv("CCU_AZURE_BLOB_LINK")
blob_migo_sas = os.getenv("CCU_AZURE_BLOB_SAS_TOKEN")

openai_api_key = os.getenv("BCFG_AZURE_OPENAI_API_KEY")
openai_api_version = os.getenv("BCFG_AZURE_OPENAI_API_VERSION")
openai_endpoint = os.getenv("BCFG_AZURE_OPENAI_ENDPOINT")

index = IndexManager(aisearch_service_migo_endpoint, aisearch_migo_index, aisearch_key_migo, openai_api_key, openai_api_version, openai_endpoint, blob_migo_connection_string, blob_migo_name_preprocessing)
blob = BlobManager(blob_migo_connection_string)
util = ContentManagerUtilities()

file_ = open("edit_icon.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

BASE_URL = "https://jgs-ai-content-mgr-dev.azurewebsites.net/"

# Function to get the authenticated user's name
def get_user_name():
    # Make a GET request to the .auth/me endpoint
    response = requests.get(f"{BASE_URL}/.auth/me")

    if response.status_code == 200:
        # Parse the JSON response
        user_info = response.json()
        # Assuming the first identity in the list is the one you want
        # Adjust the index and keys based on your actual response structure
        name = user_info[0]["user_claims"][10]["val"]  # Example path to a name claim
        return name
    else:
        # Handle errors or return a default value
        return "User"
    
def run():
    
    st.set_page_config(
                page_title="KB Content Manager",
                page_icon=":books:",
                layout="wide",
                initial_sidebar_state="auto",
            )
    
    name = get_user_name()
    st.write(f"Welcome, {name}!")
    
    col11, col21 = st.columns([0.3, 0.6], gap="large")
    
    st.sidebar.title("CONFIGURATION")
    bu = None
    function = None

    
    
    with col11:
        st.title("Content Manager")
        st.subheader("MiGO Chatbot")
 
        blob.set_blob_service_client(blob_migo_name_ccu)
        
        applicability = st.sidebar.selectbox("Choose Applicability", [None,"Groupwide", "BU Specific"])

        if applicability == "Groupwide":
            function = st.sidebar.selectbox("Choose Function", [None, "Finance", "HR", "IT", "Legal"])
            if function != None:
                subfolder = function.lower()+'/generic/'
                blob_list = blob.list_blob(subfolder)
            
        if applicability == "BU Specific":
            bu = st.sidebar.selectbox("Choose Business Unit", [None, "CCU", "Aspen", "RLC", "RRHI", "JGSOC"])
            if bu != None:
                function = st.sidebar.selectbox("Choose Function", [None, "Finance", "HR", "IT", "Legal"])
                if function != None:
                    blob.set_blob_service_client(blob_migo_name[bu.lower()])
                    current_blob = blob_migo_name[bu.lower()]
                    subfolder = function.lower()+'/specific/'
                    blob_list = blob.list_blob(subfolder)
        else:
            pass
   
    if (applicability == 'Groupwide' and function is not None) or (applicability == 'BU Specific' and bu is not None and function is not None):
                  
        if "generic" not in subfolder:
            blob.set_blob_item_url(blob_migo_link, f'{blob_migo_name[bu.lower()]}/{subfolder}', blob_migo_sas)
            index.set_blob_item_url(blob_migo_link, f'{blob_migo_name[bu.lower()]}/{subfolder}', blob_migo_sas)
        else:
            blob.set_blob_item_url(blob_migo_link, f'{blob_migo_name_ccu}/{subfolder}', blob_migo_sas)
            index.set_blob_item_url(blob_migo_link, f'{blob_migo_name_ccu}/{subfolder}', blob_migo_sas)
            
        with col11:

            col1, col2, col3, col4 = st.columns([0.06,0.06,0.06,0.1])
            st.divider()

            if 'upload_button' not in st.session_state:
                st.session_state.upload_button = False
            if 'update_button' not in st.session_state:
                st.session_state.update_button = False
            if 'delete_button' not in st.session_state:
                st.session_state.delete_button = False

            buttons = [("New", "up"), ("Update", "upd"), ("Delete", "del")]
            cols = [col1, col2, col3]
            tooltip = ["Click to create new KB content.", "Make desired changes and save existing KB Content details.", "Remove the selected KB Content permanently."]

            for col, (label, key), h in zip(cols, buttons, tooltip):
                if col.button(label, key=key, type="primary", use_container_width=True, help=h):
                    st.session_state.upload_button = label == "New"
                    st.session_state.update_button = label == "Update"
                    st.session_state.delete_button = label == "Delete"
            
            if st.session_state.upload_button:
                upload(function, subfolder)
            if st.session_state.update_button:
                update(function, subfolder)
            if st.session_state.delete_button:
                delete(subfolder, bu)
                              
        with col21:
            st.subheader("Files")
            
            docs = index.list_index_documents(filters=f"category eq '{function}'")

            seen_files = set()
            df = pd.DataFrame()
            for doc in docs:
                print(doc['id'], doc['document_title'])
                
                if doc['document_title'] not in seen_files:
                    seen_files.add(doc['document_title'])
                    
                    if function != "HR":
                        st.page_link(doc['download_url'], label=doc['document_title'])
                    
                    else:
        
                        if "generic" in subfolder:
                            if function.lower()+'/generic' in doc['download_url']:
                                
                                # Get blob properties
                                blob_client = blob.blob_service_client.get_blob_client(blob_migo_name_ccu, function.lower()+'/generic/'+doc['document_title'])
                                print(function.lower()+'/generic/'+doc['document_title'])
                                blob_properties = blob_client.get_blob_properties()
                                file_link = f'<a href="{doc["download_url"]}" target="_blank" rel="noopener noreferrer">{doc["document_title"]}</a>'
                                edit_link = f'<a href="{doc["edit_url"]}" target="_blank" rel="noopener noreferrer"><img src="data:image/png;base64,{data_url}" alt="Edit" width="20" height="20"></a>'
                                file_link = f'{file_link} {edit_link if doc["edit_url"] else ""}'
                                data = pd.DataFrame({"File Name": [file_link],"Size": f"{round(int(blob_properties.size)/1024/1024,2)}MB" , "Created at": [blob_properties.creation_time.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")], "Last Modified": [blob_properties.last_modified.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")]})
                                df = pd.concat([df, data], ignore_index=True)
                                
                        else:
                            if blob_migo_name[bu.lower()]+'/'+function.lower()+'/specific' in doc['download_url']:
                                
                                # Get blob properties
                                blob_client = blob.blob_service_client.get_blob_client(blob_migo_name[bu.lower()], function.lower()+'/specific/'+doc['document_title'])
                                print(function.lower()+'/specific/'+doc['document_title'])
                                blob_properties = blob_client.get_blob_properties()
                                file_link = f'<a href="{doc["download_url"]}" target="_blank" rel="noopener noreferrer">{doc["document_title"]}</a>'
                                edit_link = f'<a href="{doc["edit_url"]}" target="_blank" rel="noopener noreferrer"><img src="data:image/png;base64,{data_url}" alt="Edit" width="20" height="20"></a>'
                                file_link = f'{file_link} {edit_link if doc["edit_url"] else ""}'
                                data = pd.DataFrame({"File Name": [file_link],"Size": f"{round(int(blob_properties.size)/1024/1024,2)}MB" , "Created at": [blob_properties.creation_time.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")], "Last Modified": [blob_properties.last_modified.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")]})
                                df = pd.concat([df, data], ignore_index=True)
                                
            # Add a search input field
            search_query = st.text_input("Search for a file")

            # Filter the DataFrame based on the search query
            if search_query:
                df = df[df['File Name'].str.contains(search_query, case=False)]                 
                                
            # Convert DataFrame to HTML and remove index
            df_html = df.to_html(index=False, escape=False)
            
            # Use st.markdown to display HTML
            st.markdown(df_html, unsafe_allow_html=True)
            
def upload(function, subfolder):
    st.subheader("Create")
    files = st.file_uploader("Upload file/s", accept_multiple_files=True, type=["pdf"])
    
    if st.button("Upload"):
        for file in files:
            # upload to blob container
            with st.spinner(f"Uploading {file.name}..."):
                
                #if subfolder contains generic on the text, put all files to all business units
                if "generic" in subfolder:
                    for bu in blob_migo_name.keys():
                        blob.set_blob_service_client(blob_migo_name[bu])
                        res = blob.upload_azure_blob_item(file, subfolder)
                else:
                    res = blob.upload_azure_blob_item(file, subfolder)
            if res:
                st.success(f"{file.name} uploaded successfully", icon="✅")

                # Seek back to the start of the file
                file.seek(0)

                # upload to index
                with st.spinner(f"Indexing {file.name}..."):
                    

                    res = index.upload_update_item_azure_index(file, function)
                    if res:
                        st.success(f"{file.name} indexed successfully", icon="✅")
                    else:
                        st.error(f"{file.name} already exists in the index.", icon="❌")
            else:
                st.warning(f"{file.name} already exists in the container. Use the update button instead.", icon="⚠️")
           
def update(function, subfolder):
    st.subheader("Update")
    update = st.selectbox("Select file to update", [file.name.split("/")[-1] for file in blob.container_client.list_blobs(name_starts_with=subfolder)])
    file = st.file_uploader("Upload file", accept_multiple_files=False, type=["pdf"])
    
    if update and file:
        if file.name != update:
            st.error("File name does not match the selected file to update.")
            return
        else:
            if st.button("Update"):
                # delete first the index
                with st.spinner(f"Reindexing {file.name}..."):
                    res = index.delete_item_azure_index(file.name)
                    if res:
                        st.success(f"{file.name} reindexed successfully", icon="✅")
                    else:
                        st.error(f"error reindexing {file.name}")
                with st.spinner(f"Updating {file.name}..."):
                    if "generic" in subfolder:
                        for bu in blob_migo_name.keys():
        
                            blob.set_blob_service_client(blob_migo_name[bu])
                            res = blob.update_azure_blob_item(file, subfolder)
                    else:
                        res = blob.update_azure_blob_item(file, subfolder)

                    # Seek back to the start of the file
                    file.seek(0)
                    

                    res = index.upload_update_item_azure_index(file, function)
                    if res:
                        st.success(f"{file.name} updated successfully", icon="✅")
                    else:
                        st.error(f"An error occurred while updating {file.name}", icon="❌")

def delete(subfolder, bu):
    st.subheader("Delete")

    file_list = [file.name.split("/")[-1] for file in blob.container_client.list_blobs(name_starts_with=subfolder)]
    selected_files = []

    for file in file_list:
        if st.checkbox(file):
            selected_files.append(file)

    if st.button("Delete", key="delete"):
        for file in selected_files:
                        
            # delete blob from raw container
            with st.spinner(f"Deleting {file}..."):
                #if subfolder contains generic on the text, put all files to all business units
                if "generic" in subfolder:
                    for bu in blob_migo_name.keys():
                        blob.set_blob_service_client(blob_migo_name[bu.lower()])
    
                        res = blob.delete_azure_blob_item(file, subfolder)
                else:
                    blob.set_blob_service_client(blob_migo_name[bu.lower()])
                    res = blob.delete_azure_blob_item(file, subfolder)
            if res:
                blob.set_blob_service_client(blob_migo_name[bu.lower()])
                st.success(f"{file} deleted successfully", icon="✅")

                # delete to index
                with st.spinner(f"Unindexing {file}..."):
                    res = index.delete_item_azure_index(file)
                    if res:
                        st.success(f"{file} unindexed successfully", icon="✅")
                    else:
                        st.error(f"error unindexing {file}")

                blob.set_blob_service_client(blob_migo_name_preprocessing)
                filename = util.sanitize_filename(file)
                blob.delete_azure_blob_item(filename + ".json", "")
                blob.delete_azure_blob_item(filename + "-embedding.json", "")
            
            else:
                st.error(f"An error occurred while deleting {file}", icon="❌")
        
if __name__ == "__main__":
    run()