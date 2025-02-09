import google.generativeai as genai
import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Lấy API Key 
load_dotenv()
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
API_KEY_GPT = os.getenv("GPT_API_KEY")

# Gemini
def generate_content_genai(prompt):
    try:
        genai.configure(API_KEY_GEMINI)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except genai.errors.InvalidApiKeyError:
        return "Error: API key không hợp lệ."
    except genai.errors.RequestError as e:
        return f"Error: Yêu cầu không hợp lệ. {e}"
    except Exception as e:
        return f"Error: Đã xảy ra lỗi không xác định. {e}"

# GPT
def generate_content_openai(prompt):
    try:
        openai.api_key = API_KEY_GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.AuthenticationError:
        return "Error: API key không hợp lệ."
    except openai.error.InvalidRequestError as e:
        return f"Error: Yêu cầu không hợp lệ. {e}"
    except Exception as e:
        return f"Error: Đã xảy ra lỗi không xác định. {e}"

# Giao diện 
st.title("Tạo bài viết ")

st.subheader("Nhập tiêu đề bài viết")
title = st.text_input("Tiêu đề bài viết", placeholder="Nhập tiêu đề tại đây...")

ai_choice = st.radio(
    "Chọn API để tạo bài viết:",
    ("Google Gemini AI", "OpenAI GPT")
)

if st.button("Tạo bài viết"):
    if title:
        with st.spinner("Đang tạo bài viết..."):
            prompt = f"Viết một bài viết dài 1200 từ về chủ đề: {title}."
            if ai_choice == "Google Gemini AI":
                content = generate_content_genai(prompt)
            else:
                content = generate_content_openai(prompt)
            
            if "Error" in content:
                st.error(content)
            else:
                st.success("Bài viết đã được tạo thành công!")
                st.write(content)
    else:
        st.error("Vui lòng nhập tiêu đề bài viết!")
