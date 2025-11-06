import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- Setup for Streamlit ---
st.set_page_config(page_title="Personal Finance Tool", layout="centered")
st.title("💸 Personal Finance Assistant")

# --- Finance FAQ (Manual Q&A Section) ---
faq = {
    "What is savings?": "Savings is the portion of income you don't spend. It's typically stored in a bank account or investment for future use.",
    "How do I budget monthly?": "Budgeting involves tracking income and expenses. A popular rule is the 50/30/20 Rule: 50% Needs, 30% Wants, 20% Savings.",
    "What is debt?": "Debt is borrowed money that must be repaid, often with interest. Examples include credit cards, loans, and mortgages.",
    "How to pay off debt fast?": "Use strategies like the Snowball Method (pay smallest debts first) or Avalanche Method (pay highest interest debt first).",
    "What is the 50/30/20 Rule?": "50% of income to necessities, 30% to wants, 20% to savings or debt repayment.",
    "What is an emergency fund?": "Savings set aside for unexpected expenses. Aim for 3–6 months of expenses.",
    "What are good vs bad debts?": "Good debt builds value (e.g., education loan). Bad debt drains finances (e.g., credit cards).",
    "What is compound interest?": "Compound interest is interest on interest. It grows savings or debt faster over time.",
    "What is inflation?": "Inflation is the rise in prices over time, which reduces purchasing power.",
    "What is financial freedom?": "Having enough income/savings to afford your lifestyle without relying on work.",
    "What are assets and liabilities?": "Assets = what you own. Liabilities = what you owe. Net worth = Assets - Liabilities.",
    "How can I start investing as a beginner?": "Start with SIPs, index funds or mutual funds. Stay consistent and learn basics.",
    "What is the rule of 72?": "72 ÷ Interest Rate = Years to double your money."
}

# --- Navigation ---
mode = st.sidebar.radio("Choose Mode", ["📊 Personal Finance Analyzer", "💬 Manual Q&A Chatbot"])

# --- Personal Finance Analyzer ---
if mode == "📊 Personal Finance Analyzer":
    st.subheader("📊 Personal Finance Analyzer")

    # --- Currency Selection ---
    currency = st.selectbox("Select your currency symbol:", ['₹', '$', '€', '£', 'Other'])
    if currency == "Other":
        currency = st.text_input("Enter custom currency symbol:", value='₹')

    # --- Financial Inputs ---
    st.markdown("### Enter Your Monthly Financial Data")

    income = st.number_input(f"Total Monthly Income ({currency})", min_value=0.0, format="%.2f")

    expenses = st.number_input(f"Expenses ({currency})", min_value=0.0, format="%.2f")
    savings = st.number_input(f"Savings ({currency})", min_value=0.0, format="%.2f")
    investments = st.number_input(f"Investments ({currency})", min_value=0.0, format="%.2f")

    total_outflow = expenses + savings + investments
    remaining = income - total_outflow

    if total_outflow > income:
        st.error(f"⚠ Your total spending ({currency}{total_outflow:,.2f}) exceeds your income ({currency}{income:,.2f})!")
    else:
        st.success(f"Remaining Balance: {currency}{remaining:,.2f}")

        if st.button("Generate Analysis"):
            # Prepare Data
            data = pd.DataFrame([
                {'Type': 'Income', 'Category': 'Income', 'Amount': income},
                {'Type': 'Expense', 'Category': 'Expenses', 'Amount': expenses},
                {'Type': 'Savings', 'Category': 'Savings', 'Amount': savings},
                {'Type': 'Investment', 'Category': 'Investments', 'Amount': investments}
            ])
            
            # --- Pie Chart: Distribution ---
            st.markdown("### 💡 Financial Distribution")
            fig1, ax1 = plt.subplots()
            pie_data = data.groupby('Type')['Amount'].sum()
            pie_data = pie_data[pie_data.index.isin(['Income', 'Expense', 'Savings', 'Investment'])]
            ax1.pie(pie_data, labels=pie_data.index,
                    autopct=lambda p: f'{p:.1f}%\n({currency}{p*sum(pie_data)/100:,.0f})',
                    colors=['#4CAF50', '#F44336', '#2196F3', '#FFC107'], startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # --- Bar Chart: Expense Breakdown ---
            st.markdown("### 📊 Expense, Savings & Investment Breakdown")
            filtered = data[data['Type'].isin(['Expense', 'Savings', 'Investment'])].copy()
            fig2, ax2 = plt.subplots()
            sns.barplot(x='Amount', y='Category', data=filtered, palette="viridis", ax=ax2)
            ax2.set_xlabel(f"Amount ({currency})")
            st.pyplot(fig2)

# --- Manual Q&A Chatbot ---
elif mode == "💬 Manual Q&A Chatbot":
    st.subheader("💬 Manual Q&A Chatbot")

    question = st.selectbox("Choose a finance question:", [""] + list(faq.keys()))
    if question:
        st.markdown("#### 🤖 Answer:")
        st.success(faq[question])

