from urlextract import URLExtract # type: ignore
from wordcloud import WordCloud # type: ignore
from collections import Counter
import pandas as pd
import emoji # type: ignore
from textblob import TextBlob # type: ignore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
from dotenv import load_dotenv # type: ignore
from langchain_core.prompts import PromptTemplate # type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore


load_dotenv()

extractor = URLExtract()
def fetch_stats(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    num_messages = df.shape[0]
    num_words = []
    for message in df['message']:
        num_words.extend(message.split())

    media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, num_words, media_messages , links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0])*100,4).reset_index().rename(columns={'user':'name','count':'percentage'})
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['user'] != 'group_notification']

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    with open('stop_words.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().split()

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['user'] != 'group_notification']

    words = []

    for message in temp['message']:
        message = emoji.replace_emoji(message, replace='')

        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    df_mwc = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return df_mwc

def emoji_solve(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
       
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df 

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline 

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


analyzer = SentimentIntensityAnalyzer()
def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['user'] != 'group_notification']

    sentiments = []
    for message in temp['message']:
        score = analyzer.polarity_scores(message)['compound']
        if score >= 0.05:
            sentiments.append("Positive")
        elif score <= -0.05:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")

    sentiment_df = pd.DataFrame(sentiments, columns=["sentiment"])

    result = sentiment_df.value_counts().reset_index()
    result.columns = ["Sentiment", "Count"]

    total = result["Count"].sum()
    result["Percentage"] = (result["Count"] / total * 100).round(2)

    overall = result.sort_values("Count", ascending=False).iloc[0]["Sentiment"]

    return result, overall

def sentiment_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    scores = []

    for message in df['message']:
        scores.append(analyzer.polarity_scores(message)['compound'])

    df2 = df.copy()
    df2['score'] = scores

    timeline = df2.groupby('only_date')['score'].mean().reset_index()
    return timeline

def most_emotional_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    scores = []
    for message in df['message']:
        scores.append(analyzer.polarity_scores(message)['compound'])

    df2 = df.copy()
    df2['score'] = scores

    day_scores = df2.groupby('only_date')['score'].mean()

    max_day = day_scores.idxmax()
    min_day = day_scores.idxmin()

    return max_day, min_day

def user_sentiment_comparison(df):

    users = df['user'].unique()

    results = []

    for user in users:
        if user == "group_notification":
            continue

        temp = df[df['user'] == user]

        scores = []
        for msg in temp['message']:
            scores.append(analyzer.polarity_scores(msg)['compound'])

        avg = sum(scores)/len(scores) if scores else 0
        results.append((user, avg))

    comp_df = pd.DataFrame(results, columns=["User","Avg Sentiment"])
    return comp_df.sort_values("Avg Sentiment", ascending=False)


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.5)

def chunk_text(text, chunk_size=3000):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks

def chat_summary(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['user'] != 'group_notification']
    
    text = " ".join(temp["message"].astype(str).tolist())
    # MAX_WORDS = 120000
    # words = text.split()
    # if len(words) > MAX_WORDS:
    #     words = words[-MAX_WORDS:]  # keep latest messages (more relevant)
    #     text = " ".join(words)  

    if not text.strip():
        return "No messages found.", []

    chunks = chunk_text(text)

    partial_summaries = []

    for chunk in chunks:
        prompt = f"""
        You are an AI chat analyst.

        Analyze this WhatsApp conversation and provide:

        1. Summary paragraph
        2. Key discussion topics
        3. Decisions made
        4. Important dates
        5. Overall tone

        Chat:
        {chunk}
        """

        response = model.invoke(prompt)
        partial_summaries.append(response.content)

    combined = "\n".join(partial_summaries)

    final_prompt = f"""
    Combine the following summaries into one final structured output.

    Provide:
    - Final concise paragraph summary
    - Key discussion points (bullets)
    - Overall conversation tone

    Summaries:
    {combined}
    """

    final_response = model.invoke(final_prompt)

    return final_response.content

