import streamlit as st


def main_page():
    st.title("#Company Name")
    st.subheader(" About Us")
    st.markdown("""


At ("#Company Name"), we're passionate about using technology to solve complex business problems. Our team of experts is
 dedicated to helping organizations of all sizes transform their operations and achieve their goals.

We offer a wide range of IT services, including software development,Data Science, system integration, cloud computing,  
and more. Our solutions are customized to meet the unique needs of each client, and we work closely with them every step 
of the way to ensure their success.

With years of experience and a deep understanding of the latest technologies, we're committed to delivering high-quality 
results that exceed our clients' expectations. Our team is constantly learning and evolving to stay ahead of the curve, 
and we're always on the lookout for new ways to innovate and improve.

We're proud to have a track record of success and to have helped many organizations achieve their IT goals. If you're 
looking for a trusted partner to help you navigate the ever-changing world of technology, 
look no further than ("#Company Name").""")


def page2():
    import pandas as pd
    from pytesseract import image_to_string, pytesseract
    import nltk
    import spacy
    from PIL import Image
    from pyresparser import ResumeParser
    from datetime import datetime
    from docx import Document
    import os
    import streamlit as stnew

    nltk.download('stopwords')
    spacy.load("en_core_web_sm")
    pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

    stnew.title("SMART CV EXTRACTOR")
    stnew.markdown("""
    <style>
    h1 {
      color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    def add_bg_from_url():
        stnew.markdown(
            f"""
             <style>
             .stApp {{
                 background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
            unsafe_allow_html=True
        )

    add_bg_from_url()

    def main():
        resumes = stnew.file_uploader("Upload your Resumes and Images", type=["pdf", "docx", "jpg", 'jpeg'],
                                      accept_multiple_files=True)
        if resumes is not None:
            all_data = []
            for resume in resumes:
                if resume.type in ["application/pdf",
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    data = ResumeParser(resume).get_extracted_data()
                    all_data.append(data)
                else:
                    image = Image.open(resume)
                    text1 = image_to_string(image)
                    document = Document()
                    document.add_paragraph(text1)
                    document.save("document.docx")
                    document = "document.docx"
                    data = ResumeParser(document).get_extracted_data()
                    all_data.append(data)
            df = pd.DataFrame(all_data, columns=['name', 'email', 'mobile_number', 'skills', 'degree', 'experience',
                                                 'company_names'])
            df.insert(0, "TimeStamp", datetime.now())
            df.insert(0, 'New_ID', range(1, 1 + len(df)))
            download = stnew.button("Download CSV File")
            if 'download_state' not in stnew.session_state:
                stnew.session_state.download_state = False
            if download or stnew.session_state.download_state:
                stnew.session_state.download_state = True
                if os.path.isfile("oryx.csv"):
                    add_to_existing = stnew.radio("Do you want to add to an existing file or create a new one?",
                                                  ["Add to existing", "Create new"])
                    if add_to_existing == "Add to existing":
                        existing_files = [file for file in os.listdir(".") if file.endswith(".csv")]
                        selected_files = stnew.multiselect("Select the files to add the resume to:", existing_files)
                        for selected_file in selected_files:
                            existing_df = pd.read_csv(selected_file)
                            last_id = existing_df["New_ID"].iloc[-1]
                            df["New_ID"] = range(last_id + 1, last_id + 1 + len(df))
                            df.to_csv(selected_file, mode='a', header=False, index=False)
                        stnew.write("Resume added to existing CSV file")
                    elif add_to_existing == "Create new":
                        new_csv_name = stnew.text_input("Enter the name of the new CSV file with the extension ")
                        csv_path = os.path.join(".", new_csv_name)
                        if not os.path.exists(csv_path):
                            with open(csv_path, "w") as f:
                                df.to_csv(f, index=False)
                            stnew.markdown(f"New CSV file {new_csv_name} created and Resume added to it")
                        else:
                            stnew.warning("Enter the valid name of the new CSV file.")
                else:
                    df.to_csv("oryx.csv", index=False)
            stnew.write(df)

        # ...

    if __name__ == '__main__':
        main()


def page3():
    import openai
    import streamlit as st10
    from streamlit_chat import message

    # set OpenAI API key
    openai.api_key = "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"

    # define Streamlit app
    def generate_response(prompt):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        messagenew = completions.choices[0].text
        return messagenew

    def ask_question(question):
        clear_chat()

    def clear_chat():

        st10.title("chatBot : Streamlit + openAI")

    # Storing the chat
    if 'generated' not in st10.session_state:
        st10.session_state['generated'] = []

    if 'past' not in st10.session_state:
        st10.session_state['past'] = []
        # run Streamlit app

    def get_text():
        input_text = st10.text_input("", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        output = generate_response(user_input)
        # store the output
        st10.session_state.past.append(user_input)
        st10.session_state.generated.append(output)

    if st10.session_state['generated']:

        for i in range(len(st10.session_state['generated']) - 1, -1, -1):
            message(st10.session_state["generated"][i], key=str(i))
            message(st10.session_state['past'][i], is_user=True, key=str(i) + '_user')


page_names_to_funcs = {
    "About Us": main_page,
    "SMART CV EXTRACTOR": page2,
    "AI Chatbot": page3,

}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
