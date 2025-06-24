💸 Money Manager App
A Streamlit-based personal finance application that helps users track daily expenses, visualize spending patterns, and maintain monthly budgets — all in a clean, interactive dashboard. Perfect for students, working professionals, and budget-conscious individuals who want a simple yet powerful way to manage their finances.

🧠 What It Does
💰 Adds expenses by category, amount, date, and notes

📅 Filters expenses by month and category

📊 Generates visual analytics: bar charts, pie charts, and trendlines

💡 Tracks remaining monthly budget

🗑️ Allows expense deletion with instant feedback

📥 Enables CSV downloads of filtered data

🔁 Auto-refreshes the dashboard after data input

🚀 Features
🧾 Expense Tracker with SQLite: Efficient local database to persist user inputs

🧠 Auto-Rerun After Adding: Instantly see updated charts after adding a new expense

📈 Visual Analytics:

📅 Daily Spending Bar Chart (Plotly)

📂 Category Breakdown Pie Chart

📈 Altair Trend Line with Gradient

📆 Monthly Budget Tracker: Set a monthly limit and monitor spending

📤 Download Filtered CSV: Export filtered results for offline review

🧼 Clean UI: Simple layout with sidebar controls and collapsible sections

📱 How to Use
Add a new expense from the sidebar form (amount, category, date, notes)

Set your monthly budget for financial tracking

Choose a month and category filter from the dashboard

Explore your data visually in bar, pie, and trendline charts

Download your filtered data as a .csv file

Delete old entries directly from the dashboard

🧩 How It Works
🗂️ Data Management
Stores all expenses in a local SQLite database

Updates data in real-time without needing a manual refresh

📊 Visual Engine
Plotly for daily spending and pie breakdown

Altair for aesthetic area-based spending trend

Color-coded overspending days (e.g., red bars for ₹1000+)

🔧 Tech Stack
Frontend: Streamlit

Backend: SQLite

Libraries: pandas, plotly, altair, datetime
