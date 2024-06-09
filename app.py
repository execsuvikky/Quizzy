import streamlit
import random
import json
from memes import get_random_meme
from session import SessionVariable

def load_data():
    with open("data.json", "r") as file:
        data_map = json.load(file)
    data_list = list(data_map.items())
    random.shuffle(data_list)
    return data_list

# Session Data
qa = SessionVariable("qa", default=load_data)
correct_counter = SessionVariable("correct_counter", default=0)
incorrect_counter = SessionVariable("incorrect_counter", default=0)
idk_counter = SessionVariable("idk_counter", default=0)
index = SessionVariable("index", default=0)
answer = SessionVariable("answer", default="$")
page = SessionVariable("page", default="start")

streamlit.set_page_config(page_title=f"Quizzy", page_icon="🧠")
streamlit.title("Quizzy")

# End of the quiz
if index.get() >= len(qa.get()):
    streamlit.subheader("Вітаю, ви пройшли всі слова!")
    streamlit.write(f"Правильних: {correct_counter.get()}, неправильних: {incorrect_counter.get()}, не знаю: {idk_counter.get()}")
    streamlit.write("Дякую за участь!")
    streamlit.stop()

# Page "start"
if page.get() == "start":
    streamlit.write("Quizzy це простий тест для вивчення англійських слів, я буду показувати вам слово, а ви повинні відповісти як його перекласти.")
    streamlit.write("Якщо ви не знаєте відповідь, просто натисніть кнопку 'Не знаю'.")
    streamlit.write("Почнемо?")
    if streamlit.button("Почати"):
        page.set("quiz_question")
        streamlit.rerun()
# Page "quiz_question"
elif page.get() == "quiz_question":
    question, answers = qa.get()[index.get()]
    streamlit.subheader(f"Питання {index.get() + 1} з {len(qa.get())}")
    streamlit.write(f"Спробуйте перекласти \"{question}\"")
    input = streamlit.text_input("Ваша відповідь")
    col1, col2 = streamlit.columns(2)
    if col1.button("Відповісти") and input != "":
        answer.set(input)
        page.set("quiz_question_result")
        streamlit.rerun()
    if col2.button("Не знаю"):
        answer.set("$")
        page.set("quiz_question_result")
        streamlit.rerun()
    streamlit.write(f"{correct_counter.get()} правильних, {incorrect_counter.get()} неправильних, {idk_counter.get()} не знаю.")
# Page "quiz_question_result"
elif page.get() == "quiz_question_result":
    question, answers = qa.get()[index.get()]
    streamlit.subheader(f"Питання {index.get() + 1} з {len(qa.get())}")
    streamlit.write(f"Речення: \"{question}\"")
    streamlit.write(f"Правильні відповіді: {', '.join(answers)}")
    if answer.get() != "$":
        # streamlit.markdown(f"<p style='color:red;'>{correct_counter.get()} правильних, {incorrect_counter.get()} неправильних, {idk_counter.get()} не знаю.</p>", unsafe_allow_html=True)
        if answer.get().lower() in answers:
            answer_state = "correct"
            streamlit.markdown(f"<p style='color:green;'>Ваша відповідь вірна: {answer.get()}</p>", unsafe_allow_html=True)
            streamlit.image(get_random_meme("correct"))
            correct_counter.update(lambda x: x + 1)
        else:
            answer_state = "incorrect"
            streamlit.markdown(f"<p style='color:red;'>Ваша відповідь невірна: {answer.get()}</p>", unsafe_allow_html=True)
            streamlit.image(get_random_meme("incorrect"))
            incorrect_counter.update(lambda x: x + 1)
    else:
        answer_state = "idk"
        streamlit.write("Ви не знали відповідь.")
        streamlit.image(get_random_meme("idk"))
        idk_counter.update(lambda x: x + 1)
    if streamlit.button("Наступне запитання"):
        index.update(lambda x: x + 1)
        page.set("quiz_question")
        if answer_state == "correct":
            correct_counter.update(lambda x: x - 1)
        elif answer_state == "incorrect":
            incorrect_counter.update(lambda x: x - 1)
        elif answer_state == "idk":
            idk_counter.update(lambda x: x - 1)
        streamlit.rerun()
