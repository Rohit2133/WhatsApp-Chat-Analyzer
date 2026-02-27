# import streamlit as st # type: ignore
# import preprocess , helper 
# import matplotlib.pyplot as plt

# st.sidebar.title("WhatsApp Chat Analyzer")

# file = st.sidebar.file_uploader("Upload WhatsApp Chat File", type=["txt"])
# if file is not None:
#     bytes_data = file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocess.preprocess(data)
#     # st.dataframe(df)
    
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, 'Overall')

#     selected_user = st.sidebar.selectbox("Select User", user_list)
    
#     if st.sidebar.button("Show Analysis"):
#         num_messages, num_words , media_messages , links = helper.fetch_stats(selected_user, df)

#         st.title("Top Statistics")
#         col1 , col2 , col3 , col4 = st.columns(4)

#         with col1:
#             st.subheader("Total Messages:")
#             st.title(num_messages)
#         with col2:
#             st.subheader("Total words:")
#             st.title(len(num_words))
#         with col3:
#             st.subheader("Media Messages:")
#             st.title(media_messages)
#         with col4:
#             st.subheader('Links Shared:')
#             st.title(len(links))

#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig , ax = plt.subplots()
#         ax.plot(timeline['time'],timeline['message'],color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig , ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         # activity map
#         st.title('Activity Map')
#         col1,col2 = st.columns(2)

#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index,busy_day.values,color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values,color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)


#         if selected_user == 'Overall':
#             st.title("Most Busy Users")
#             x , new_df = helper.most_busy_users(df)
#             x.index = x.index.str.split().str[0]
#             fig , ax = plt.subplots()

#             col1 , col2 = st.columns(2)
#             with col1:
#                 ax.bar(x.index, x.values , color = 'red')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)
        
#         col1 , col2 = st.columns(2)
#         with col1:
#             st.title("WordCloud")
#             df_wc = helper.create_wordcloud(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.imshow(df_wc)
#             ax.axis("off")
#             st.pyplot(fig)
#         with col2:
#             st.title("Most Common Words")
#             df_mwc = helper.most_common_words(selected_user, df)
#             fig , ax = plt.subplots()
#             ax.bar(df_mwc['word'], df_mwc['count'] , color = 'green')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         st.title("Emoji Analysis")
#         emoji_df = helper.emoji_solve(selected_user, df)
#         col1,col2 = st.columns(2)

#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig, ax = plt.subplots()
#             ax.pie(
#                 emoji_df['count'].head(),
#                 labels=[f"Emoji {i+1}" for i in range(len(emoji_df.head()))],
#                 autopct='%0.2f'
#                 )
#             st.pyplot(fig)

import streamlit as st  # type: ignore
import preprocess, helper
import matplotlib.pyplot as plt

# @st.cache_data(show_spinner=False)
# def cached_summary(user, df):
#     return helper.chat_summary(user, df)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📱 WhatsApp Chat Analyzer")
st.sidebar.markdown("---")

file = st.sidebar.file_uploader(
    "📂 Upload WhatsApp Chat File",
    type=["txt"]
)

if file is not None:
    bytes_data = file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox(
        "👤 Select User",
        user_list
    )

    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "📊 Navigate",
        [
            "Overview",
            "Timelines",
            "Activity Map",
            "Word Analysis",
            "Emoji Analysis",
            "Sentiment Analysis",
            "Chat Summarization"
        ]
    )

    # ---------------- OVERVIEW ----------------
    if page == "Overview":
        num_messages, num_words, media_messages, links = helper.fetch_stats(
            selected_user, df
        )

        st.title("📊 Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💬 Messages", num_messages)
        with col2:
            st.metric("📝 Words", len(num_words))
        with col3:
            st.metric("🖼️ Media", media_messages)
        with col4:
            st.metric("🔗 Links", len(links))

        if selected_user == 'Overall':
            st.markdown("---")
            st.title("🔥 Most Busy Users")

            x, new_df = helper.most_busy_users(df)
            x.index = x.index.str.split().str[0]

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    # ---------------- TIMELINES ----------------
    elif page == "Timelines":
        st.title("📆 Chat Timelines")

        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.subheader("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(
            daily_timeline['only_date'],
            daily_timeline['message'],
            color='black'
        )
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # ---------------- ACTIVITY MAP ----------------
    elif page == "Activity Map":
        st.title("🗺️ Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📅 Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("📆 Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    # ---------------- WORD ANALYSIS ----------------
    elif page == "Word Analysis":
        st.title("📝 Word Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("☁️ Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

        with col2:
            st.subheader("📊 Most Common Words")
            df_mwc = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(df_mwc['word'], df_mwc['count'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    # ---------------- EMOJI ANALYSIS ----------------
    elif page == "Emoji Analysis":
        st.title("😀 Emoji Analysis")

        emoji_df = helper.emoji_solve(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Emoji Count Table")
            st.dataframe(emoji_df)

        with col2:
            st.subheader("📊 Emoji Distribution")
            st.bar_chart(
                emoji_df.set_index('emoji')['count'].head()
            )

    # ---------------- SENTIMENT ANALYSIS ----------------
    elif page == "Sentiment Analysis":

        st.title("💬 Sentiment Analysis Dashboard")

        result, overall = helper.sentiment_analysis(selected_user, df)

        # ---------------- Distribution ----------------
        st.subheader("📊 Sentiment Distribution")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(result)

        with col2:
            st.bar_chart(result.set_index("Sentiment")["Count"])

        st.markdown("---")

        # ---------------- Overall Insight ----------------
        st.subheader("🧠 Overall Chat Mood")

        if overall == "Positive":
            st.success(f"Overall chat mood is **{overall} 😊**")
        elif overall == "Negative":
            st.error(f"Overall chat mood is **{overall} 😠**")
        else:
            st.info(f"Overall chat mood is **{overall} 😐**")

        st.markdown("---")

        # ---------------- Timeline ----------------
        st.subheader("📈 Sentiment Timeline")

        timeline = helper.sentiment_timeline(selected_user, df)
        st.line_chart(timeline.set_index("only_date"))

        st.markdown("---")

        # ---------------- Emotional Days ----------------
        st.subheader("📅 Most Emotional Days")

        max_day, min_day = helper.most_emotional_day(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"Most Positive Day → {max_day}")

        with col2:
            st.error(f"Most Negative Day → {min_day}")

        st.markdown("---")

        # ---------------- User Comparison ----------------
        if selected_user == "Overall":

            st.subheader("👥 User Sentiment Comparison")

            comp = helper.user_sentiment_comparison(df)
            st.dataframe(comp)

            st.bar_chart(comp.set_index("User"))

        st.markdown("---")

        st.subheader("🤖 Insight Summary")

        if overall == "Positive":
            st.write("This conversation is generally friendly, engaging, and positive.")
        elif overall == "Negative":
            st.write("This chat shows signs of conflict, disagreement, or frustration.")
        else:
            st.write("The conversation tone is mostly neutral and informational.")

# ---------------- CHAT SUMMARIZATION ----------------
    elif page == "Chat Summarization":
        
        st.title("🧠 AI Chat Summary")

        st.info("Generates AI summary of conversation using Gemini")

        if st.button("Generate Summary"):

            with st.spinner("Analyzing conversation..."):
                summary = helper.chat_summary(selected_user, df)

            st.success("Summary Ready ✅")
            st.markdown(summary)



else:
    st.markdown("<h1 style='text-align:center;'>📱 WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center; font-size:18px;'>Analyze your WhatsApp conversations with powerful insights</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.info("👈 Upload a WhatsApp chat file from the sidebar to begin analysis.")

    st.markdown("## 🚀 Features : ")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Statistics")
        st.write("Messages, words, links, and media stats")

    with col2:
        st.markdown("### 📆 Timelines")
        st.write("Daily and monthly chat activity")

    with col3:
        st.markdown("### 😀 Emoji Insights")
        st.write("Most used emojis and trends")

    col1 , col2  , col3 = st.columns(3)
    with col1:
        st.markdown("### 🗺️ Activity Map")
        st.write("Most active days and months")

    with col2:
        st.markdown("### 📊 Sentiment Analysis")
        st.write("Overall chat sentiment and trends")

    with col3:
        st.markdown("### 📝 Chat Summarization")
        st.write("Get a quick summary of your chat")
    st.markdown("---")

    st.markdown("### 📌 How to Use")
    st.markdown("""
    1. Export chat from WhatsApp  
    2. Upload `.txt` file  
    3. Choose user  
    4. Explore insights  
    """)

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit")

