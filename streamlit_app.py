import streamlit as st
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt

# Function to fetch Hebrew date
def fetch_hebrew_date():
    try:
        response = requests.get('https://www.hebcal.com/converter?cfg=json&gy=2024&gm=8&gd=2&g2h=1')
        data = response.json()
        english_date = datetime.date(data['gy'], data['gm'], data['gd'])
        formatted_english_date = english_date.strftime("%B %d, %Y")
        return f"Today is {formatted_english_date} - {data['hebrew']}"
    except Exception as e:
        st.error(f"Error fetching Hebrew date: {e}")
        return "Error fetching date"

# Function to fetch financial data
def fetch_data():
    sheet_id = '1LwT_dQcUBvjtjwA2uAZg9BGjijznOYSLuaT6IIIzb2U'
    api_key = 'YOUR_API_KEY'  # Replace with your API key

    endpoints = {
        'balance': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Money Income!C2?key={api_key}',
        'costs': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Seforim to buy!G2?key={api_key}',
        'moneyTitle': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Seforim to buy!I1?key={api_key}',
        'moneyAmount': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Seforim to buy!I2?key={api_key}',
        'seforimLabels': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Seforim to buy!B2:B?key={api_key}',
        'seforimAmounts': f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Seforim to buy!C2:C?key={api_key}'
    }

    data = {}
    try:
        for key, url in endpoints.items():
            response = requests.get(url)
            data[key] = response.json()
    except Exception as e:
        st.error(f"Error fetching data from Google Sheets: {e}")
    
    return data

# Function to plot the charts
def plot_charts(seforim_labels, seforim_amounts):
    st.subheader("Income Chart")
    income_data = {
        'labels': ['1-Aug', '2-Aug', '3-Aug', '4-Aug'],
        'amounts': [9, 12, 7, 8]
    }
    fig, ax = plt.subplots()
    ax.plot(income_data['labels'], income_data['amounts'], marker='o', color='rgb(15, 109, 250)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income')
    st.pyplot(fig)

    st.subheader("Seforim Costs Chart")
    fig, ax = plt.subplots()
    ax.pie(seforim_amounts, labels=seforim_labels, autopct='%1.1f%%', startangle=90, colors=['#36a2eb', '#ff6384', '#ffce56'])
    ax.axis('equal')
    ax.set_title('Seforim Costs')
    st.pyplot(fig)

# Main Streamlit application
st.title("Financial Dashboard")

st.markdown(f"<h2 style='text-align: center;'>{fetch_hebrew_date()}</h2>", unsafe_allow_html=True)

data = fetch_data()

if data:
    balance = data['balance']['values'][0][0] if 'values' in data['balance'] else 'No data found'
    costs = data['costs']['values'][0][0] if 'values' in data['costs'] else 'No data found'
    money_title = data['moneyTitle']['values'][0][0] if 'values' in data['moneyTitle'] else 'No data found'
    money_amount = data['moneyAmount']['values'][0][0] if 'values' in data['moneyAmount'] else 'No data found'
    seforim_labels = data['seforimLabels']['values']
    seforim_amounts = data['seforimAmounts']['values']

    st.markdown(f"""
    <div style='display: flex; justify-content: center;'>
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin: 10px; border: 1px solid rgb(15, 109, 250); max-width: 300px;'>
            <h2 style='font-size: 60px; color: rgb(15, 109, 250);'>{balance}</h2>
            <p style='font-size: 20px; color: rgb(15, 109, 250);'>Balance</p>
        </div>
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin: 10px; border: 1px solid rgb(15, 109, 250); max-width: 300px;'>
            <h2 style='font-size: 60px; color: rgb(15, 109, 250);'>{costs}</h2>
            <p style='font-size: 20px; color: rgb(15, 109, 250);'>Costs of Seforim</p>
        </div>
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin: 10px; border: 1px solid rgb(15, 109, 250); max-width: 300px;'>
            <h2 style='font-size: 60px; color: rgb(15, 109, 250);'>{money_amount}</h2>
            <p style='font-size: 20px; color: rgb(15, 109, 250);'>{money_title}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    plot_charts(seforim_labels, seforim_amounts)

st.subheader("Add New Income")
income_date = st.date_input("Income Date")
income_amount = st.number_input("Income Amount", min_value=0.0, step=0.01)

if st.button("Add Income"):
    st.write(f"Income added: {income_date} - ${income_amount}")

