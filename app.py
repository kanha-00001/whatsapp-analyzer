import streamlit as st
from preprocessor import preprocess  # Ensure this module is correctly implemented
import helper
import matplotlib.pyplot as plt
import pandas as pd


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    try:
   
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        # Process data into a DataFrame
        df = preprocess(data)
        st.dataframe(df)


        users_list = df["user"].unique().tolist()
        users_list.sort()
        users_list.insert(0, "Overall")  # Option for overall analysis
        
        selected_user = st.sidebar.selectbox("Show analysis with respect to", users_list)
    #for showing number of message
        if st.sidebar.button("Show analysis"):

            total_messages = len(df) if selected_user == "Overall" else df[df["user"] == selected_user].shape[0]
            
 
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Total Messages")
                st.title(total_messages)
            # for generating number of words
            words,num_media_messages= helper.fetch_stats(selected_user,df)
            with col2:
                st.header("Total words")
                st.title(len(words))


            with col3: 
                st.header("Total media shared")
                st.title(num_media_messages)




  

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)



     #for finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='Skyblue')
                plt.xticks(rotation='vertical', fontweight='bold')
                plt.yticks(fontweight='bold')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df) 




        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        st.title('Most commmon words')
        st.pyplot(fig)







  
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
