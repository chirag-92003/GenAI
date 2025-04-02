import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langdetect import detect
from googletrans import Translator

# Load environment variables
load_dotenv()

# Get API Key
Api_key = os.getenv("API_KEY")

# Debug: Check if API Key is loaded
if not Api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=Api_key)
translator = Translator()

# Use a valid Gemini model
model_name = "gemini-1.5-pro"

def generate_questions(model_name, text):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"Generate questions from the following text:\n\n{text}\n\nQuestions:")

        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "No questions generated"
    except Exception as e:
        return f"Error generating questions: {e}"

def main():
    st.title("Inquisitive")

    user_text = st.text_area("Enter the text you want questions generated from:")

    if st.button("Generate Questions"):
        if user_text:
            try:
                detected_language = detect(user_text)

                # Translate if needed
                if detected_language != 'en':
                    translated_text = translator.translate(user_text, src=detected_language, dest='en').text
                else:
                    translated_text = user_text

                # Generate questions
                questions = generate_questions(model_name, translated_text)

                # Translate back if needed
                if detected_language != 'en':
                    questions = translator.translate(questions, src='en', dest=detected_language).text

                st.subheader("Generated Questions:")
                st.write(questions)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()




# import streamlit as st
# import os
# from dotenv import load_dotenv
# import google.generativeai as palm
# from langdetect import detect
# from googletrans import Translator, LANGUAGES

# load_dotenv()

# Api_key = os.getenv("API_KEY")

# palm.configure(api_key=Api_key)
# translator = Translator()

# i = 0
# model_list = palm.list_models()
# for model in model_list:
#     if i == 1:
#         model_name = model.name
#         break
#     i += 1

# def generate_questions(model_name, text):
#     response = palm.generate_text(
#         model=model_name,
#         prompt=f"Generate questions from the following text:\n\n{text}\n\nQuestions:",
#         max_output_tokens=150
#     )

#     questions = response.result.strip() if response.result else "No questions generated"

#     return questions

# def main():
#     st.title("Inquisitive")

#     user_text = st.text_area("Enter the text you want questions generated from:")

#     if st.button("Generate Questions"):
#         if user_text:
#             try:
#                 detected_language = detect(user_text)

#                 if detected_language != 'en':
#                     translated_text = translator.translate(user_text, src=detected_language, dest='en').text
#                 else:
#                     translated_text = user_text

#                 questions = generate_questions(model_name, translated_text)

#                 if detected_language != 'en':
#                     questions = translator.translate(questions, src='en', dest=detected_language).text

#                 st.subheader("Generated Questions:")
#                 st.write(questions)
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")
#         else:
#             st.warning("Please enter some text.")

# if __name__ == "__main__":
#     main()
