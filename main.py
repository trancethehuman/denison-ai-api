import streamlit as st

from admission_chatbot import get_admission_chatbot_response
from newsletter import get_news_recommendation

st.title("Denison University AI Tools Demo")

st.subheader("1. Admission AI Assistant")

user_response = st.text_input(
    "Type your question and hit Enter!", max_chars=80)

if (user_response):
    with st.spinner('Give me some time to think on this...'):
        st.write(get_admission_chatbot_response(user_response))

st.text("")
st.text("")
st.text("")

st.subheader("2. Personalized Newsletter")
st.markdown("This section demonstrates how each newsletter recipient gets a different set of recommended news and stories based on their profile.")

col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Name", value="Emily Blunt")

with col2:
    graduation_year = st.number_input(
        "Graduation Year", min_value=1, step=1, value=2015)

with col3:
    majors_options = ['Economics', 'Communications', 'Cinema', 'History', 'Art History', 'Environmental Studies', 'Math',
                      'International Studies', 'Music', 'Computer Science', 'Theatre', 'Queer Studies', "Women's & Gender Studies"]
    major = st.selectbox(
        'Major',
        majors_options, index=0)

interest_options = ['Fraternities & Sororities', 'Varsity Sport',
                    'Finance', 'Business', 'Arts', 'Community Service', 'Volunteering', 'Travel', 'Music', 'Science']
interests = st.multiselect(
    "Interests, Activities, or Career", interest_options, default=interest_options[:len(interest_options)//3])


article_source_column, number_of_articles_column = st.columns(2)
with article_source_column:
    articles_source = st.selectbox(
        label="Articles Source", options=('denison.edu', 'The Denisonian'), index=0)

with number_of_articles_column:
    number_of_articles = st.number_input(
        label="Number of articles", min_value=1, step=1, value=2, max_value=3)

user_profile = {
    "name": name,
    "interests": interests,
    "graduation_year": graduation_year,
    "major": major
}
user_profile_string = f"""My name is {user_profile["name"]}, has interests in {user_profile["interests"]}, graduated in {user_profile["graduation_year"]}, majored in {user_profile["major"]} """

st.text("")
st.text("")

if st.button("Generate Newsletter", type="secondary"):
    with st.spinner('Generating newsletter...'):
        newsletter = st.write(get_news_recommendation(
            user_profile_string, articles_source, number_of_articles))
