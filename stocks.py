#Library Imports
import os
import streamlit as st
import openai
from metaphor_python import Metaphor
from datetime import date, timedelta

#Setting APIs 
openai.api_key = st.secrets.OPENAI_API
metaphor = Metaphor(st.secrets.METAPHOR_API)

#Streamlit UI
st.title("Stock Market Pulse")
st.markdown("<p> Your Stock Market Companion for Bullish Insights and Future Performance Predictions in One Line", unsafe_allow_html=True,)
st.markdown("<p/><i> Sarah Faiz",unsafe_allow_html=True)
option = st.radio("Choose an option:", ["General Market Trends", "Specific Stock Forecast"],index=None)

if option == "General Market Trends":

    # Framing query using ChatGPT
    USER_QUESTION = "Suggest verified financial articles that predicts bullish stocks in the upcoming week"
    SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": USER_QUESTION},
        ],
    )
    query = completion.choices[0].message.content

    # Metaphor's response
    search_response = metaphor.search(
        query, num_results=5, use_autoprompt=True, start_published_date=str(date.today() - timedelta(days=7))
    )

    #extract stock names from search_response

    contents_result = search_response.get_contents()
    SYSTEM_MESSAGE = "You are a financial assistant that advises how stocks will perform in the upcoming week. You read the article and give a list of names of stocks predicted to grow. You only give the name of stocks, no other message. You ignore the articles that do not mention companies in the article"

    # Create an empty list to store stock names
    stocks = []

    # Loop through all the search results and extract names from each result
    for result in contents_result.contents:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": result.extract},
            ],
        )
        stock = completion.choices[0].message.content
        stocks.append(stock)

    # Combine all the names into one
    stocks_list = "\n".join(stocks)
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are  financial analyst, that count and output the names from the list based on their frequency. You just output the a bullet list of the companies sorted on the descending order of the frequencies, nothing else."},
                {"role": "user", "content": stocks_list},
            ],
        )
    st.markdown("<h4 style='color:Green'> Results </h4>",unsafe_allow_html=True)
    st.write("Stocks to be on the watchlist, based on the recent data")
    #Display the list of favored stocks
    st.write(completion.choices[0].message.content)



elif option == "Specific Stock Forecast":
    specific_stock = st.text_input("Enter the stock name:", placeholder = "Please enter a valid stock")
    if specific_stock:              
    # Framing query using ChatGPT
        query = f"Articles about {specific_stock} stock "
        # Metaphor's response
        search_response = metaphor.search(
            query, num_results=5, use_autoprompt=True, start_published_date=str(date.today() - timedelta(days=7))
        )

        # Determine performance from search_response
        contents_result = search_response.get_contents()
        #st.write(contents_results)

        SYSTEM_MESSAGE = "You are financial assistant that advises whether to in invest in a particular stock or not. You read the article and give a one line to assist a potential investor."
    
        # Create an empty list to store stock names
        summaries = []

        # Loop through all the search results and summarise each result
        for result in contents_result.contents:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": result.extract},
                ],
            )
            summary = completion.choices[0].message.content
            summaries.append(summary)

        # Combine all the names into one
        SYSTEM_MESSAGE = "You are a financial analyst collating the summaries from multiple artcles and giving a single line gist about the company's performance."
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": result.extract},
                ],
            )
        
        #Display the specific stock forecast
        st.markdown("<h4 style='color:Green'> Results </h4>",unsafe_allow_html=True)
        st.write(f"{completion.choices[0].message.content}")


st.write("Application powered by OpenAI, Metaphor, and Streamlit")
    