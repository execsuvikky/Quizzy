import json
import random

import streamlit as st


def state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def get_shuffled_data():
    data = list(json.load(open('data.json')).items())
    random.shuffle(data)
    return data


if "data" not in st.session_state:
    st.session_state.data = get_shuffled_data()

data = st.session_state.data

correct_counter = state("correct_counter", 0)
wrong_counter = state("wrong_counter", 0)
idk_counter = state("idk_counter", 0)
index = state("index", 0)

st.set_page_config(
    page_title=f"Quizzy ({correct_counter}/{correct_counter + wrong_counter})",
    page_icon="🧠",
)
st.title("Quizzy")

st.subheader(f"Питання {min(index + 1, len(data))} з {len(data)}")

st.write(f"Правильних: {correct_counter}, неправильних: {wrong_counter}, не знаю: {idk_counter}")

if len(data) <= index:
    st.write("Вітаю, ви пройшли всі слова!")
    st.stop()

original, translations = data[index]

answer = st.text_input(f"Як перекласти \"{original}\"?", key="answer")

if answer:
    if answer.lower() in translations:
        st.session_state.correct_counter += 1
        st.write("Вірно!")
    else:
        st.session_state.wrong_counter += 1
        beautiful_translations = "; ".join(translations)
        st.write(f"Невірно! Правильно: {beautiful_translations}")
    st.session_state.index += 1

if st.button("Відповісти"):
    st.rerun()

if st.button("Не знаю"):
    st.session_state.idk_counter += 1
    st.session_state.index += 1
    st.rerun()


st.write("(c) Developed by Viktor")