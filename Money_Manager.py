import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import sqlite3
from datetime import datetime

st.set_page_config(page_title="💸 Money Manager", layout="wide")
st.title("💰 Personal Money Manager")



def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TEXT,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date, notes):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, date, notes) VALUES (?, ?, ?, ?)",
              (amount, category, date, notes))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql("SELECT * FROM expenses", conn, parse_dates=["date"])
    conn.close()
    return df


init_db()



st.sidebar.header("➕ Add New Expense")

with st.sidebar.form("expense_form"):
    amount = st.number_input("Amount (₹)", min_value=1.0, format="%.2f")

    category_list = [
        "🍔 Food", "🎉 Social Life", "🐶 Pets", "🚗 Transport", "🎭 Culture",
        "🏠 Household", "👗 Apparel", "💄 Beauty", "🩺 Health",
        "🎓 Education", "🎁 Gift", "📦 Other"
    ]

    category = st.selectbox("Category", category_list)
    date = st.date_input("Date", value=datetime.today())
    notes = st.text_input("Notes (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        add_expense(amount, category, date.strftime('%Y-%m-%d'), notes)
        st.success("✅ Expense added!")
        st.rerun()  



st.sidebar.header("🎯 Monthly Budget")
monthly_budget = st.sidebar.number_input("Set Monthly Budget (₹)", min_value=0.0, format="%.2f", value=0.0)



df = fetch_expenses()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    st.subheader("📊 Expense Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        month_filter = st.selectbox(
            "Select Month",
            sorted(df["date"].dt.strftime('%B %Y').unique(), reverse=True)
        )
    with col2:
        category_filter = st.multiselect(
            "Filter by Category",
            df["category"].unique(),
            default=df["category"].unique()
        )

    df_filtered = df[
        (df["date"].dt.strftime('%B %Y') == month_filter) &
        (df["category"].isin(category_filter))
    ]

    total_spent = df_filtered["amount"].sum()
    st.metric("Total Spent", f"₹ {total_spent:,.2f}")

    if monthly_budget > 0:
        remaining = monthly_budget - total_spent
        st.metric("Remaining Budget", f"₹ {remaining:,.2f}", delta=f"{'-' if remaining < 0 else '+'}₹ {abs(remaining):,.2f}")

   

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        daily_chart = df_filtered.groupby(df_filtered["date"].dt.date)["amount"].sum().reset_index()
        threshold = 1000  # daily overspend limit
        daily_chart["Color"] = daily_chart["amount"].apply(lambda x: "crimson" if x > threshold else "seagreen")
        fig1 = px.bar(daily_chart, x="date", y="amount", title="📅 Daily Spending", color="Color", color_discrete_map="identity")
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        category_chart = df_filtered.groupby("category")["amount"].sum().reset_index()
        fig2 = px.pie(category_chart, names="category", values="amount", title="📂 Category Breakdown")
        st.plotly_chart(fig2, use_container_width=True)

    

    alt_chart = alt.Chart(df_filtered).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='lightgreen', offset=0),
                   alt.GradientStop(color='white', offset=1)],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x='date:T',
        y='amount:Q',
        tooltip=['date:T', 'amount:Q']
    ).properties(
        width=700,
        height=300,
        title="📈 Spending Trend"
    )
    st.altair_chart(alt_chart, use_container_width=True)

   

    with st.expander("📋 View All Expenses"):
        st.dataframe(df_filtered.sort_values("date", ascending=False), use_container_width=True)

    with st.expander("🗑️ Delete an Expense"):
        if not df_filtered.empty:
            delete_row = df_filtered[["id", "date", "category", "amount", "notes"]]
            delete_index = st.selectbox("Select an entry to delete", delete_row.index, format_func=lambda x: f"{delete_row.loc[x, 'date'].date()} | ₹{delete_row.loc[x, 'amount']} | {delete_row.loc[x, 'category']}")
            if st.button("Delete Selected Expense"):
                delete_expense(delete_row.loc[delete_index, 'id'])
                st.success("✅ Expense deleted! Please refresh the page.")
        else:
            st.info("No expense to delete.")

    st.download_button("📥 Download CSV", data=df_filtered.to_csv(index=False), file_name="filtered_expenses.csv")

else:
    st.info("💡 No expenses found. Add a new one from the sidebar to get started!")
