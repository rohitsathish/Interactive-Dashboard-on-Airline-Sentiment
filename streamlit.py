import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Sentiment Analysis of Tweets about US Airlines')
st.sidebar.title('Dashboard Options')

st.markdown('This is an interactive streamlit dashboard to analyze the sentiment of tweets about US airlines')

@st.cache(persist = True)
def load_data(data_url):
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data_url = 'C:/Users/user/Documents/Course Material and Projects/Coursera/Streamlit dashboards/Tweets.csv'
data = load_data(data_url)

st.sidebar.subheader('Random Tweet')
chosen_sentiment = st.sidebar.radio('Tweet Sentiment',('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @chosen_sentiment')[['text']].sample(n=1).iat[0,0])

st.sidebar.subheader('Number of Tweets by Sentiment')
show_hide1 = st.sidebar.checkbox('Show Vizualization', True, key='1')
viz_select = st.sidebar.selectbox('Vizualization Type',['Histogram','Pie Chart'])
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if show_hide1:
    st.subheader('Number of Tweets by Sentiment')
    if viz_select == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', height=500)
        st.plotly_chart(fig)
    elif viz_select == 'Pie Chart':
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader('When and Where are Users Tweeting from?')
show_hide2 = st.sidebar.checkbox('Show Vizualization', True, key='2')
select_hour = st.sidebar.slider('Hour of Day', 0, 23)
select_raw_data = st.sidebar.checkbox('Show Raw Data', False)
selected_data = data[data['tweet_created'].dt.hour == select_hour]

if show_hide2:
    st.subheader('When and Where are Users Tweeting from?')
    st.markdown('%i tweets between %i:00 and %i:00' %(len(selected_data),select_hour, (select_hour+1)%24))
    st.map(selected_data)
    if select_raw_data:
        st.write(selected_data)

st.sidebar.subheader('Sentiment of Tweets by Airline')
show_hide3 = st.sidebar.checkbox('Show Vizualization', True, key='3')
select_airline = st.sidebar.multiselect('Choose Airlines', ('American','Delta','Southwest','United','US  Airways','Virgin America'), default=['American', 'Delta'])
airline_data = data[data['airline'].isin(select_airline)]

if (len(select_airline) > 0) and show_hide3:
    st.subheader('Sentiment of Tweets by Airline')
    fig = px.histogram(airline_data, x='airline', y='airline_sentiment', histfunc='count', labels={'airline_sentiment':'tweets'},
    height=600, width=800, facet_col = 'airline_sentiment', color='airline_sentiment')
    st.plotly_chart(fig)

st.sidebar.subheader('Word Cloud for each Sentiment')
show_hide4 = st.sidebar.checkbox('Show Vizualization', True, key='4')
word_sentiment = st.sidebar.radio('Tweet Sentiment',('positive', 'neutral', 'negative'), key='2')
df = data[data['airline_sentiment'] == word_sentiment]
words = ' '.join(df['text'])
words = ' '.join([word for word in words.split() if 'http' not in word and word != 'RT' and not word.startswith('@')])
wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height=640, width = 800).generate(words)

if show_hide4:
    st.header('Word Cloud for %s sentiment'%(word_sentiment))
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig)