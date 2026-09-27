import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Bank Analytics Report",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS

st.markdown(
    """
    <style>

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 16px;
        color: #777;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background-color: rgba(128, 128, 128, 0.05);
        margin-bottom: 10px;
    }

    .metric-title {
        font-size: 14px;
        color: #777;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 700;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 650;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* Report box */
    .report-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        padding: 25px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# DATA LOADING

@st.cache_data
def load_data():

    customers = pd.read_csv("customers.csv")
    accounts = pd.read_csv("accounts.csv")
    transactions = pd.read_csv("transactions.csv")
    loans = pd.read_csv("loans.csv")

    return customers, accounts, transactions, loans


# LOAD DATA SAFELY

try:

    customers, accounts, transactions, loans = load_data()

except FileNotFoundError as e:

    st.error(
        f"""
        ❌ Required CSV file was not found.

        Missing file:

        `{e.filename}`

        Make sure the following files are in the same folder as `app.py`:

        - customers.csv
        - accounts.csv
        - transactions.csv
        - loans.csv
        """
    )

    st.stop()


# DATA PREPARATION

# Convert transaction date

if "transaction_date" in transactions.columns:

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce"
    )


# Remove invalid transaction dates only where necessary

transactions["transaction_amount"] = pd.to_numeric(
    transactions["transaction_amount"],
    errors="coerce"
)

accounts["account_balance"] = pd.to_numeric(
    accounts["account_balance"],
    errors="coerce"
)

customers["income"] = pd.to_numeric(
    customers["income"],
    errors="coerce"
)


# SIDEBAR

with st.sidebar:

    st.markdown("## 🏦 Bank Analytics")

    st.caption("Professional Banking Report")

    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "👤 Customer Details",
            "🏦 Account Details",
            "💳 Transaction Details",
            "🏠 Loan Details",
            "📊 Data Analysis"
        ]
    )

    st.divider()

    st.markdown("### 📁 Database")

    st.write(
        f"Customers: **{len(customers):,}**"
    )

    st.write(
        f"Accounts: **{len(accounts):,}**"
    )

    st.write(
        f"Transactions: **{len(transactions):,}**"
    )

    st.write(
        f"Loans: **{len(loans):,}**"
    )

    st.divider()

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


# HEADER

st.markdown(
    '<div class="main-title">🏦 BANK ANALYTICS REPORT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Customer, account, transaction and loan analysis'
    '</div>',
    unsafe_allow_html=True
)


# HOME

if menu == "🏠 Home":

    st.markdown(
        '<div class="section-title">📊 Executive Summary</div>',
        unsafe_allow_html=True
    )

    # MAIN CALCULATIONS

    total_customers = customers["customer_id"].nunique()

    total_accounts = len(accounts)

    total_transactions = len(transactions)

    total_balance = accounts["account_balance"].sum()

    average_income = customers["income"].mean()

    average_transaction = transactions[
        "transaction_amount"
    ].mean()

    total_loans = len(loans)


    # KPI ROW 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col2:

        st.metric(
            "Total Accounts",
            f"{total_accounts:,}"
        )

    with col3:

        st.metric(
            "Total Transactions",
            f"{total_transactions:,}"
        )

    with col4:

        st.metric(
            "Total Loans",
            f"{total_loans:,}"
        )


    # KPI ROW 2

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Account Balance",
            f"₹{total_balance:,.2f}"
        )

    with col2:

        st.metric(
            "Average Customer Income",
            f"₹{average_income:,.2f}"
        )

    with col3:

        st.metric(
            "Average Transaction",
            f"₹{average_transaction:,.2f}"
        )


    st.divider()


    # QUICK REPORT

    st.markdown(
        '<div class="section-title">📋 Quick Report</div>',
        unsafe_allow_html=True
    )

    report_col1, report_col2 = st.columns(2)

    with report_col1:

        st.markdown("### 👤 Customers")

        st.write(
            f"Number of customers: **{total_customers:,}**"
        )

        st.write(
            f"Average income: **₹{average_income:,.2f}**"
        )

        if "age" in customers.columns:

            average_age = customers["age"].mean()

            st.write(
                f"Average age: **{average_age:.1f} years**"
            )

        if "credit_score" in customers.columns:

            average_credit = customers[
                "credit_score"
            ].mean()

            st.write(
                f"Average credit score: "
                f"**{average_credit:.0f}**"
            )


    with report_col2:

        st.markdown("### 🏦 Accounts")

        st.write(
            f"Number of accounts: **{total_accounts:,}**"
        )

        st.write(
            f"Total balance: **₹{total_balance:,.2f}**"
        )

        if "account_type" in accounts.columns:

            most_common_account = (
                accounts["account_type"]
                .value_counts()
                .index[0]
            )

            st.write(
                f"Most common account: "
                f"**{most_common_account}**"
            )


    st.divider()


    # DATABASE STATUS

    st.markdown(
        '<div class="section-title">🗄️ Database Status</div>',
        unsafe_allow_html=True
    )

    status_col1, status_col2, status_col3, status_col4 = (
        st.columns(4)
    )

    with status_col1:

        st.success("Customers Loaded")

    with status_col2:

        st.success("Accounts Loaded")

    with status_col3:

        st.success("Transactions Loaded")

    with status_col4:

        st.success("Loans Loaded")


# CUSTOMER DETAILS

# CUSTOMER DETAILS

elif menu == "👤 Customer Details":

    st.header("👤 Customer Management")

    st.caption(
        "Search, inspect, analyze, and manage individual customers."
    )

    st.divider()

    # CUSTOMER SEARCH

    st.subheader("🔎 Find Customer")

    customer_id_input = st.text_input(
        "Enter Customer ID",
        placeholder="Example: CUST001"
    ).strip()

    if customer_id_input:

        # Convert IDs to string for safe comparison
        customers["customer_id"] = (
            customers["customer_id"]
            .astype(str)
        )

        accounts["customer_id"] = (
            accounts["customer_id"]
            .astype(str)
        )

        transactions["customer_id"] = (
            transactions["customer_id"]
            .astype(str)
        )

        loans["customer_id"] = (
            loans["customer_id"]
            .astype(str)
        )

        # FIND CUSTOMER

        customer = customers[
            customers["customer_id"].str.lower()
            == customer_id_input.lower()
        ]

        if customer.empty:

            st.error(
                f"❌ Customer `{customer_id_input}` not found."
            )

        else:

            customer_data = customer.iloc[0]

            st.success(
                f"✅ Customer `{customer_data['customer_id']}` found."
            )

            # CUSTOMER PROFILE

            st.subheader("👤 Customer Profile")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Customer ID",
                    str(customer_data["customer_id"])
                )

            with col2:
                st.metric(
                    "Name",
                    str(customer_data["name"])
                )

            with col3:
                st.metric(
                    "Age",
                    str(customer_data["age"])
                )

            with col4:
                st.metric(
                    "City",
                    str(customer_data["city"])
                )

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"**Income:** ₹{customer_data['income']:,.2f}"
                )

            with col2:

                st.info(
                    f"**Credit Score:** "
                    f"{customer_data['credit_score']}"
                )
            # CUSTOMER RELATED DATA

            customer_accounts = accounts[
                accounts["customer_id"]
                == str(customer_data["customer_id"])
            ].copy()

            customer_transactions = transactions[
                transactions["customer_id"]
                == str(customer_data["customer_id"])
            ].copy()

            customer_loans = loans[
                loans["customer_id"]
                == str(customer_data["customer_id"])
            ].copy()

            # CUSTOMER SUMMARY

            st.divider()

            st.subheader("📊 Customer Activity Summary")

            total_accounts = len(customer_accounts)

            total_transactions = len(
                customer_transactions
            )

            total_balance = (
                customer_accounts["account_balance"].sum()
                if not customer_accounts.empty
                else 0
            )

            total_transaction_amount = (
                customer_transactions[
                    "transaction_amount"
                ].sum()
                if not customer_transactions.empty
                else 0
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "🏦 Accounts",
                    f"{total_accounts:,}"
                )

            with col2:

                st.metric(
                    "💳 Transactions",
                    f"{total_transactions:,}"
                )

            with col3:

                st.metric(
                    "💰 Total Balance",
                    f"₹{total_balance:,.2f}"
                )

            with col4:

                st.metric(
                    "💸 Transaction Value",
                    f"₹{total_transaction_amount:,.2f}"
                )

            # TABS

            profile_tab, account_tab, transaction_tab, loan_tab, graph_tab, delete_tab = st.tabs(
                [
                    "👤 Profile",
                    "🏦 Accounts",
                    "💳 Transactions",
                    "🏠 Loans",
                    "📊 Graphical Analysis",
                    "🗑️ Delete Customer"
                ]
            )

            # PROFILE TAB

            with profile_tab:

                st.subheader("👤 Complete Customer Information")

                profile_data = customer.T.copy()

                profile_data.columns = [
                    "Value"
                ]

                st.dataframe(
                    profile_data,
                    use_container_width=True
                )

            # ACCOUNT TAB

            with account_tab:

                st.subheader("🏦 Customer Accounts")

                if customer_accounts.empty:

                    st.info(
                        "This customer has no accounts."
                    )

                else:

                    st.dataframe(
                        customer_accounts,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.subheader(
                        "💰 Account Balance Summary"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Total Balance",
                            f"₹{customer_accounts['account_balance'].sum():,.2f}"
                        )

                    with col2:

                        st.metric(
                            "Average Balance",
                            f"₹{customer_accounts['account_balance'].mean():,.2f}"
                        )

                    with col3:

                        st.metric(
                            "Highest Balance",
                            f"₹{customer_accounts['account_balance'].max():,.2f}"
                        )

            # TRANSACTION TAB

            with transaction_tab:

                st.subheader("💳 Customer Transactions")

                if customer_transactions.empty:

                    st.info(
                        "This customer has no transactions."
                    )

                else:

                    st.dataframe(
                        customer_transactions.sort_values(
                            "transaction_date",
                            ascending=False
                        ),
                        use_container_width=True,
                        hide_index=True
                    )

                    # TRANSACTION SUMMARY

                    st.subheader(
                        "💰 Transaction Summary"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "Transactions",
                            f"{len(customer_transactions):,}"
                        )

                    with col2:

                        st.metric(
                            "Total",
                            f"₹{customer_transactions['transaction_amount'].sum():,.2f}"
                        )

                    with col3:

                        st.metric(
                            "Average",
                            f"₹{customer_transactions['transaction_amount'].mean():,.2f}"
                        )

                    with col4:

                        st.metric(
                            "Largest",
                            f"₹{customer_transactions['transaction_amount'].max():,.2f}"
                        )

            # LOAN TAB

            with loan_tab:

                st.subheader("🏠 Customer Loans")

                if customer_loans.empty:

                    st.info(
                        "This customer has no loans."
                    )

                else:

                    st.dataframe(
                        customer_loans,
                        use_container_width=True,
                        hide_index=True
                    )

                    if "loan_amount" in customer_loans.columns:

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "Total Loan Amount",
                                f"₹{customer_loans['loan_amount'].sum():,.2f}"
                            )

                        with col2:

                            st.metric(
                                "Average Loan",
                                f"₹{customer_loans['loan_amount'].mean():,.2f}"
                            )

            # GRAPHICAL ANALYSIS

            with graph_tab:

                st.subheader(
                    "📊 Customer Graphical Analysis"
                )

                if (
                    customer_accounts.empty
                    and customer_transactions.empty
                ):

                    st.warning(
                        "Not enough activity data "
                        "to create graphs."
                    )

                else:

                    # ROW 1

                    col1, col2 = st.columns(2)

                    # ACCOUNT TYPE DISTRIBUTION

                    with col1:

                        if not customer_accounts.empty:

                            account_distribution = (
                                customer_accounts[
                                    "account_type"
                                ]
                                .value_counts()
                                .reset_index()
                            )

                            account_distribution.columns = [
                                "Account Type",
                                "Count"
                            ]

                            fig_accounts = px.pie(
                                account_distribution,
                                names="Account Type",
                                values="Count",
                                title="🏦 Account Type Distribution",
                                hole=0.45
                            )

                            fig_accounts.update_layout(
                                height=450
                            )

                            st.plotly_chart(
                                fig_accounts,
                                use_container_width=True
                            )

                    # TRANSACTION TYPE DISTRIBUTION

                    with col2:

                        if (
                            not customer_transactions.empty
                            and
                            "transaction_type"
                            in customer_transactions.columns
                        ):

                            transaction_distribution = (
                                customer_transactions[
                                    "transaction_type"
                                ]
                                .value_counts()
                                .reset_index()
                            )

                            transaction_distribution.columns = [
                                "Transaction Type",
                                "Count"
                            ]

                            fig_transactions = px.pie(
                                transaction_distribution,
                                names="Transaction Type",
                                values="Count",
                                title="💳 Transaction Type Distribution",
                                hole=0.45
                            )

                            fig_transactions.update_layout(
                                height=450
                            )

                            st.plotly_chart(
                                fig_transactions,
                                use_container_width=True
                            )

                    # TRANSACTION ACTIVITY OVER TIME

                    if not customer_transactions.empty:

                        st.subheader(
                            "📈 Transaction Activity Over Time"
                        )

                        transaction_time = (
                            customer_transactions
                            .dropna(
                                subset=[
                                    "transaction_date"
                                ]
                            )
                            .groupby(
                                "transaction_date"
                            )
                            .agg(
                                Transaction_Count=(
                                    "transaction_amount",
                                    "count"
                                ),
                                Total_Amount=(
                                    "transaction_amount",
                                    "sum"
                                )
                            )
                            .reset_index()
                            .sort_values(
                                "transaction_date"
                            )
                        )

                        if not transaction_time.empty:

                            fig_activity = px.line(
                                transaction_time,
                                x="transaction_date",
                                y="Total_Amount",
                                markers=True,
                                title="💰 Transaction Value Over Time"
                            )

                            fig_activity.update_layout(
                                height=450,
                                xaxis_title="Date",
                                yaxis_title="Transaction Amount (₹)"
                            )

                            st.plotly_chart(
                                fig_activity,
                                use_container_width=True
                            )

                            # TRANSACTION COUNT

                            fig_count = px.line(
                                transaction_time,
                                x="transaction_date",
                                y="Transaction_Count",
                                markers=True,
                                title="📊 Number of Transactions Over Time"
                            )

                            fig_count.update_layout(
                                height=450,
                                xaxis_title="Date",
                                yaxis_title="Transactions"
                            )

                            st.plotly_chart(
                                fig_count,
                                use_container_width=True
                            )

                    # TRANSACTION AMOUNT DISTRIBUTION

                    if not customer_transactions.empty:

                        st.subheader(
                            "💳 Transaction Amount Distribution"
                        )

                        fig_amount = px.histogram(
                            customer_transactions,
                            x="transaction_amount",
                            nbins=20,
                            title="Distribution of Customer Transactions"
                        )

                        fig_amount.update_layout(
                            height=450,
                            xaxis_title="Transaction Amount (₹)",
                            yaxis_title="Number of Transactions"
                        )

                        st.plotly_chart(
                            fig_amount,
                            use_container_width=True
                        )

                    # ACCOUNT BALANCE DISTRIBUTION

                    if not customer_accounts.empty:

                        st.subheader(
                            "💰 Account Balance Distribution"
                        )

                        fig_balance = px.bar(
                            customer_accounts,
                            x="account_number",
                            y="account_balance",
                            title="Balance of Customer Accounts",
                            text_auto=".2s"
                        )

                        fig_balance.update_layout(
                            height=450,
                            xaxis_title="Account Number",
                            yaxis_title="Balance (₹)"
                        )

                        st.plotly_chart(
                            fig_balance,
                            use_container_width=True
                        )

                    # TRANSACTION STATISTICS

                    if not customer_transactions.empty:

                        st.subheader(
                            "📊 Transaction Statistics"
                        )

                        stats = pd.DataFrame(
                            {
                                "Metric": [
                                    "Minimum",
                                    "Average",
                                    "Median",
                                    "Maximum",
                                    "Standard Deviation"
                                ],
                                "Value": [
                                    customer_transactions[
                                        "transaction_amount"
                                    ].min(),

                                    customer_transactions[
                                        "transaction_amount"
                                    ].mean(),

                                    customer_transactions[
                                        "transaction_amount"
                                    ].median(),

                                    customer_transactions[
                                        "transaction_amount"
                                    ].max(),

                                    customer_transactions[
                                        "transaction_amount"
                                    ].std()
                                ]
                            }
                        )

                        stats["Value"] = stats[
                            "Value"
                        ].round(2)

                        st.dataframe(
                            stats,
                            use_container_width=True,
                            hide_index=True
                        )


            # DELETE CUSTOMER


            with delete_tab:

                st.subheader(
                    "🗑️ Delete Customer"
                )

                st.warning(
                    "⚠️ Deleting a customer will also remove "
                    "their related accounts, transactions, "
                    "and loans from the CSV files."
                )


                # RECORD COUNTS


                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Customer Records",
                        len(customer)
                    )

                with col2:

                    st.metric(
                        "Accounts",
                        len(customer_accounts)
                    )

                with col3:

                    st.metric(
                        "Transactions",
                        len(customer_transactions)
                    )

                with col4:

                    st.metric(
                        "Loans",
                        len(customer_loans)
                    )

                st.divider()

                confirm_delete = st.checkbox(
                    "I understand that this action cannot be easily undone."
                )

                if confirm_delete:

                    if st.button(
                        "🗑️ Permanently Delete Customer",
                        type="primary",
                        use_container_width=True
                    ):

                        try:

                            customer_id = str(
                                customer_data["customer_id"]
                            )

                            # Remove customer
                            customers = customers[
                                customers["customer_id"].astype(str)
                                != customer_id
                            ]

                            # Remove accounts
                            accounts = accounts[
                                accounts["customer_id"].astype(str)
                                != customer_id
                            ]

                            # Remove transactions
                            transactions = transactions[
                                transactions["customer_id"].astype(str)
                                != customer_id
                            ]

                            # Remove loans
                            loans = loans[
                                loans["customer_id"].astype(str)
                                != customer_id
                            ]

                            # Save files
                            customers.to_csv(
                                "customers.csv",
                                index=False
                            )

                            accounts.to_csv(
                                "accounts.csv",
                                index=False
                            )

                            transactions.to_csv(
                                "transactions.csv",
                                index=False
                            )

                            loans.to_csv(
                                "loans.csv",
                                index=False
                            )

                            # Clear Streamlit cache
                            st.cache_data.clear()

                            st.success(
                                f"✅ Customer `{customer_id}` "
                                "and all related records "
                                "were deleted successfully."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"❌ Error while deleting customer: {e}"
                            )

    else:

        st.info(
            "👆 Enter a Customer ID above to view "
            "the customer's complete profile and activity."
        )
# ============================================================
# ACCOUNT DETAILS
# ============================================================

elif menu == "🏦 Account Details":

    st.header("🏦 Account Details")

    st.write(
        f"Total accounts: **{len(accounts):,}**"
    )

    st.divider()


    # --------------------------------------------------------
    # ACCOUNT TYPE FILTER
    # --------------------------------------------------------

    if "account_type" in accounts.columns:

        account_types = sorted(
            accounts["account_type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_type = st.selectbox(
            "🏦 Account Type",
            ["All"] + account_types
        )

        filtered_accounts = accounts.copy()

        if selected_type != "All":

            filtered_accounts = filtered_accounts[
                filtered_accounts["account_type"]
                == selected_type
            ]

    else:

        filtered_accounts = accounts.copy()


    # ACCOUNT SUMMARY

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Accounts",
            f"{len(filtered_accounts):,}"
        )

    with col2:

        balance = filtered_accounts[
            "account_balance"
        ].sum()

        st.metric(
            "Total Balance",
            f"₹{balance:,.2f}"
        )

    with col3:

        avg_balance = filtered_accounts[
            "account_balance"
        ].mean()

        st.metric(
            "Average Balance",
            f"₹{avg_balance:,.2f}"
        )


    st.divider()


    st.dataframe(
        filtered_accounts,
        use_container_width=True,
        hide_index=True
    )


    st.download_button(
        label="⬇️ Download Account Data",
        data=filtered_accounts.to_csv(index=False),
        file_name="account_report.csv",
        mime="text/csv"
    )


# TRANSACTION DETAILS

elif menu == "💳 Transaction Details":

    st.header("💳 Transaction Details")

    st.write(
        f"Total transactions: **{len(transactions):,}**"
    )

    st.divider()


    # TRANSACTION TYPE FILTER

    filtered_transactions = transactions.copy()


    if "transaction_type" in transactions.columns:

        transaction_types = sorted(
            transactions["transaction_type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_transaction_type = st.selectbox(
            "Transaction Type",
            ["All"] + transaction_types
        )

        if selected_transaction_type != "All":

            filtered_transactions = (
                filtered_transactions[
                    filtered_transactions[
                        "transaction_type"
                    ] == selected_transaction_type
                ]
            )


    # TRANSACTION SUMMARY

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Transactions",
            f"{len(filtered_transactions):,}"
        )

    with col2:

        total_transaction_amount = (
            filtered_transactions[
                "transaction_amount"
            ].sum()
        )

        st.metric(
            "Total Amount",
            f"₹{total_transaction_amount:,.2f}"
        )

    with col3:

        avg_transaction = (
            filtered_transactions[
                "transaction_amount"
            ].mean()
        )

        st.metric(
            "Average Amount",
            f"₹{avg_transaction:,.2f}"
        )


    st.divider()


    st.dataframe(
        filtered_transactions,
        use_container_width=True,
        hide_index=True
    )


    st.download_button(
        label="⬇️ Download Transaction Data",
        data=filtered_transactions.to_csv(index=False),
        file_name="transaction_report.csv",
        mime="text/csv"
    )


# LOAN DETAILS

elif menu == "🏠 Loan Details":

    st.header("🏠 Loan Details")

    st.write(
        f"Total loan records: **{len(loans):,}**"
    )

    st.divider()


    # LOAN STATUS

    filtered_loans = loans.copy()


    if "loan_status" in loans.columns:

        statuses = sorted(
            loans["loan_status"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_status = st.selectbox(
            "Loan Status",
            ["All"] + statuses
        )

        if selected_status != "All":

            filtered_loans = filtered_loans[
                filtered_loans["loan_status"]
                == selected_status
            ]


    # LOAN SUMMARY

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Loan Records",
            f"{len(filtered_loans):,}"
        )

    with col2:

        if "loan_amount" in filtered_loans.columns:

            loan_amount = pd.to_numeric(
                filtered_loans["loan_amount"],
                errors="coerce"
            ).sum()

            st.metric(
                "Total Loan Amount",
                f"₹{loan_amount:,.2f}"
            )


    st.divider()


    st.dataframe(
        filtered_loans,
        use_container_width=True,
        hide_index=True
    )


    st.download_button(
        label="⬇️ Download Loan Data",
        data=filtered_loans.to_csv(index=False),
        file_name="loan_report.csv",
        mime="text/csv"
    )


# DATA ANALYSIS


elif menu == "📊 Data Analysis":

    st.header("📊 Data Analysis Dashboard")

    st.caption(
        "Interactive statistical and graphical analysis of banking data."
    )

    st.divider()

    # ANALYSIS TABS

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 General Analysis",
            "🏦 Account Analysis",
            "💳 Transaction Analysis",
            "🚨 Risk Analysis",
            "📊 Overview"
        ]
    )

    # GENERAL ANALYSIS

    with tab1:

        st.subheader("👤 Customer Analysis")

        total_customers = customers["customer_id"].nunique()

        average_income = customers["income"].mean()
        median_income = customers["income"].median()
        minimum_income = customers["income"].min()
        maximum_income = customers["income"].max()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Customers",
                f"{total_customers:,}"
            )

        with col2:
            st.metric(
                "Average Income",
                f"₹{average_income:,.2f}"
            )

        with col3:
            st.metric(
                "Median Income",
                f"₹{median_income:,.2f}"
            )

        with col4:
            st.metric(
                "Highest Income",
                f"₹{maximum_income:,.2f}"
            )

        st.divider()

        # INCOME DISTRIBUTION

        st.subheader("📊 Customer Income Distribution")

        fig_income = px.histogram(
            customers,
            x="income",
            nbins=30,
            title="Distribution of Customer Income",
            labels={
                "income": "Income",
                "count": "Number of Customers"
            }
        )

        fig_income.update_layout(
            height=450,
            xaxis_title="Income (₹)",
            yaxis_title="Customers",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_income,
            use_container_width=True
        )

        # CITY ANALYSIS

        st.subheader("🏙️ City-wise Average Income")

        city_income = (
            customers
            .groupby("city")
            .agg(
                Customers=("customer_id", "count"),
                Average_Income=("income", "mean"),
                Minimum_Income=("income", "min"),
                Maximum_Income=("income", "max")
            )
            .reset_index()
            .sort_values(
                "Average_Income",
                ascending=False
            )
        )

        city_income[
            [
                "Average_Income",
                "Minimum_Income",
                "Maximum_Income"
            ]
        ] = city_income[
            [
                "Average_Income",
                "Minimum_Income",
                "Maximum_Income"
            ]
        ].round(2)

        col1, col2 = st.columns(2)

        with col1:

            fig_city = px.bar(
                city_income,
                x="city",
                y="Average_Income",
                title="Average Income by City",
                text_auto=".2s"
            )

            fig_city.update_layout(
                height=450,
                xaxis_title="City",
                yaxis_title="Average Income (₹)"
            )

            st.plotly_chart(
                fig_city,
                use_container_width=True
            )

        with col2:

            fig_city_customers = px.bar(
                city_income,
                x="city",
                y="Customers",
                title="Customers by City",
                text_auto=True
            )

            fig_city_customers.update_layout(
                height=450,
                xaxis_title="City",
                yaxis_title="Customers"
            )

            st.plotly_chart(
                fig_city_customers,
                use_container_width=True
            )

        st.dataframe(
            city_income,
            use_container_width=True,
            hide_index=True
        )

    # ACCOUNT ANALYSIS

    with tab2:

        st.subheader("🏦 Account Analysis")

        account_analysis = (
            accounts
            .groupby("account_type")
            .agg(
                Number_of_Accounts=(
                    "account_type",
                    "count"
                ),
                Total_Balance=(
                    "account_balance",
                    "sum"
                ),
                Average_Balance=(
                    "account_balance",
                    "mean"
                ),
                Minimum_Balance=(
                    "account_balance",
                    "min"
                ),
                Maximum_Balance=(
                    "account_balance",
                    "max"
                )
            )
            .reset_index()
        )

        for column in [
            "Total_Balance",
            "Average_Balance",
            "Minimum_Balance",
            "Maximum_Balance"
        ]:

            account_analysis[column] = (
                account_analysis[column]
                .round(2)
            )

        # ACCOUNT KPI

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Accounts",
                f"{len(accounts):,}"
            )

        with col2:

            st.metric(
                "Total Balance",
                f"₹{accounts['account_balance'].sum():,.2f}"
            )

        with col3:

            st.metric(
                "Average Balance",
                f"₹{accounts['account_balance'].mean():,.2f}"
            )

        st.divider()

        # ACCOUNT TYPE GRAPHS

        col1, col2 = st.columns(2)

        with col1:

            fig_account_count = px.pie(
                account_analysis,
                names="account_type",
                values="Number_of_Accounts",
                title="Account Type Distribution",
                hole=0.4
            )

            fig_account_count.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_account_count,
                use_container_width=True
            )

        with col2:

            fig_account_balance = px.bar(
                account_analysis,
                x="account_type",
                y="Total_Balance",
                title="Total Balance by Account Type",
                text_auto=".2s"
            )

            fig_account_balance.update_layout(
                height=450,
                xaxis_title="Account Type",
                yaxis_title="Total Balance (₹)"
            )

            st.plotly_chart(
                fig_account_balance,
                use_container_width=True
            )

        # AVERAGE BALANCE

        fig_avg_balance = px.bar(
            account_analysis,
            x="account_type",
            y="Average_Balance",
            title="Average Account Balance",
            text_auto=".2s"
        )

        fig_avg_balance.update_layout(
            height=450,
            xaxis_title="Account Type",
            yaxis_title="Average Balance (₹)"
        )

        st.plotly_chart(
            fig_avg_balance,
            use_container_width=True
        )

        st.subheader("📋 Account Statistical Report")

        st.dataframe(
            account_analysis,
            use_container_width=True,
            hide_index=True
        )

    # TRANSACTION ANALYSIS

    with tab3:

        st.subheader("💳 Transaction Analysis")

        transaction_mean = (
            transactions["transaction_amount"].mean()
        )

        transaction_median = (
            transactions["transaction_amount"].median()
        )

        transaction_std = (
            transactions["transaction_amount"].std()
        )

        total_transaction_value = (
            transactions["transaction_amount"].sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Value",
                f"₹{total_transaction_value:,.2f}"
            )

        with col2:

            st.metric(
                "Average",
                f"₹{transaction_mean:,.2f}"
            )

        with col3:

            st.metric(
                "Median",
                f"₹{transaction_median:,.2f}"
            )

        with col4:

            st.metric(
                "Standard Deviation",
                f"₹{transaction_std:,.2f}"
            )

        st.divider()

        # MONTHLY TRANSACTION DATA

        monthly_transactions = (
            transactions
            .dropna(subset=["transaction_date"])
            .groupby(
                transactions["transaction_date"].dt.to_period("M")
            )
            .agg(
                Number_of_Transactions=(
                    "transaction_amount",
                    "count"
                ),
                Total_Amount=(
                    "transaction_amount",
                    "sum"
                ),
                Average_Amount=(
                    "transaction_amount",
                    "mean"
                )
            )
            .reset_index()
        )

        monthly_transactions["Month"] = (
            monthly_transactions["transaction_date"]
            .astype(str)
        )

        monthly_transactions[
            "Total_Amount"
        ] = monthly_transactions[
            "Total_Amount"
        ].round(2)

        monthly_transactions[
            "Average_Amount"
        ] = monthly_transactions[
            "Average_Amount"
        ].round(2)

        # TRANSACTION COUNT TREND

        st.subheader("📈 Monthly Transaction Trend")

        fig_monthly_count = px.line(
            monthly_transactions,
            x="Month",
            y="Number_of_Transactions",
            markers=True,
            title="Number of Transactions per Month"
        )

        fig_monthly_count.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Number of Transactions"
        )

        st.plotly_chart(
            fig_monthly_count,
            use_container_width=True
        )

        # MONTHLY AMOUNT

        st.subheader("💰 Monthly Transaction Amount")

        fig_monthly_amount = px.area(
            monthly_transactions,
            x="Month",
            y="Total_Amount",
            title="Total Transaction Amount per Month"
        )

        fig_monthly_amount.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Transaction Amount (₹)"
        )

        st.plotly_chart(
            fig_monthly_amount,
            use_container_width=True
        )

        # TRANSACTION TYPE

        if "transaction_type" in transactions.columns:

            st.subheader("💳 Transaction Type Analysis")

            transaction_type_analysis = (
                transactions
                .groupby("transaction_type")
                .agg(
                    Transactions=(
                        "transaction_amount",
                        "count"
                    ),
                    Total_Amount=(
                        "transaction_amount",
                        "sum"
                    ),
                    Average_Amount=(
                        "transaction_amount",
                        "mean"
                    )
                )
                .reset_index()
            )

            transaction_type_analysis[
                "Total_Amount"
            ] = transaction_type_analysis[
                "Total_Amount"
            ].round(2)

            transaction_type_analysis[
                "Average_Amount"
            ] = transaction_type_analysis[
                "Average_Amount"
            ].round(2)

            col1, col2 = st.columns(2)

            with col1:

                fig_transaction_type = px.pie(
                    transaction_type_analysis,
                    names="transaction_type",
                    values="Transactions",
                    title="Transaction Type Distribution",
                    hole=0.4
                )

                fig_transaction_type.update_layout(
                    height=450
                )

                st.plotly_chart(
                    fig_transaction_type,
                    use_container_width=True
                )

            with col2:

                fig_transaction_amount = px.bar(
                    transaction_type_analysis,
                    x="transaction_type",
                    y="Total_Amount",
                    title="Transaction Amount by Type",
                    text_auto=".2s"
                )

                fig_transaction_amount.update_layout(
                    height=450,
                    xaxis_title="Transaction Type",
                    yaxis_title="Total Amount (₹)"
                )

                st.plotly_chart(
                    fig_transaction_amount,
                    use_container_width=True
                )

            st.dataframe(
                transaction_type_analysis,
                use_container_width=True,
                hide_index=True
            )

        # TRANSACTION AMOUNT DISTRIBUTION

        st.subheader("📊 Transaction Amount Distribution")

        fig_transaction_hist = px.histogram(
            transactions,
            x="transaction_amount",
            nbins=40,
            title="Distribution of Transaction Amounts"
        )

        fig_transaction_hist.update_layout(
            height=450,
            xaxis_title="Transaction Amount (₹)",
            yaxis_title="Number of Transactions"
        )

        st.plotly_chart(
            fig_transaction_hist,
            use_container_width=True
        )

        st.subheader("📋 Monthly Transaction Report")

        st.dataframe(
            monthly_transactions[
                [
                    "Month",
                    "Number_of_Transactions",
                    "Total_Amount",
                    "Average_Amount"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    # RISK ANALYSIS

    with tab4:

        st.subheader("🚨 Risk & Anomaly Analysis")

        transaction_mean = (
            transactions["transaction_amount"].mean()
        )

        transaction_std = (
            transactions["transaction_amount"].std()
        )

        threshold = (
            transaction_mean +
            3 * transaction_std
        )

        suspicious = transactions[
            transactions["transaction_amount"] > threshold
        ].copy()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Average Transaction",
                f"₹{transaction_mean:,.2f}"
            )

        with col2:

            st.metric(
                "3σ Threshold",
                f"₹{threshold:,.2f}"
            )

        with col3:

            st.metric(
                "Suspicious Transactions",
                f"{len(suspicious):,}"
            )

        st.divider()

        # TRANSACTION ANOMALY GRAPH

        st.subheader("🚨 Transaction Anomaly Detection")

        transaction_chart = transactions.copy()

        transaction_chart["Risk"] = transaction_chart[
            "transaction_amount"
        ].apply(
            lambda x:
            "Suspicious"
            if x > threshold
            else "Normal"
        )

        fig_risk = px.scatter(
            transaction_chart,
            x="transaction_date",
            y="transaction_amount",
            color="Risk",
            title="Transaction Amount vs Date",
            hover_data=[
                "customer_id",
                "transaction_type"
            ]
            if "transaction_type" in transaction_chart.columns
            else ["customer_id"]
        )

        fig_risk.add_hline(
            y=threshold,
            line_dash="dash",
            annotation_text="3σ Threshold"
        )

        fig_risk.update_layout(
            height=550,
            xaxis_title="Transaction Date",
            yaxis_title="Transaction Amount (₹)"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # SUSPICIOUS TRANSACTIONS

        if len(suspicious) > 0:

            st.warning(
                f"{len(suspicious):,} transactions "
                "are above the statistical threshold."
            )

            st.subheader(
                "🚨 Suspicious Transaction Records"
            )

            suspicious = suspicious.sort_values(
                "transaction_amount",
                ascending=False
            )

            st.dataframe(
                suspicious,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                label="⬇️ Download Suspicious Transactions",
                data=suspicious.to_csv(index=False),
                file_name="suspicious_transactions.csv",
                mime="text/csv"
            )

        else:

            st.success(
                "✅ No transactions exceeded "
                "the statistical threshold."
            )

        # TOP 10 TRANSACTIONS

        st.divider()

        st.subheader(
            "💳 Top 10 Largest Transactions"
        )

        top_10 = transactions.nlargest(
            10,
            "transaction_amount"
        )

        fig_top10 = px.bar(
            top_10.sort_values(
                "transaction_amount"
            ),
            x="transaction_amount",
            y="transaction_id",
            orientation="h",
            title="Top 10 Largest Transactions",
            text_auto=".2s"
        )

        fig_top10.update_layout(
            height=500,
            xaxis_title="Transaction Amount (₹)",
            yaxis_title="Transaction ID"
        )

        st.plotly_chart(
            fig_top10,
            use_container_width=True
        )

        st.dataframe(
            top_10,
            use_container_width=True,
            hide_index=True
        )

        # ACCOUNT BALANCE RISK

        st.divider()

        st.subheader(
            "🏦 High-Balance Account Analysis"
        )

        balance_mean = (
            accounts["account_balance"].mean()
        )

        balance_std = (
            accounts["account_balance"].std()
        )

        balance_threshold = (
            balance_mean +
            3 * balance_std
        )

        high_balance_accounts = accounts[
            accounts["account_balance"] >
            balance_threshold
        ].copy()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Average Balance",
                f"₹{balance_mean:,.2f}"
            )

        with col2:

            st.metric(
                "Balance Threshold",
                f"₹{balance_threshold:,.2f}"
            )

        with col3:

            st.metric(
                "High-Balance Accounts",
                f"{len(high_balance_accounts):,}"
            )

        if len(high_balance_accounts) > 0:

            fig_balance_risk = px.histogram(
                accounts,
                x="account_balance",
                nbins=30,
                title="Account Balance Distribution"
            )

            fig_balance_risk.add_vline(
                x=balance_threshold,
                line_dash="dash",
                annotation_text="3σ Threshold"
            )

            fig_balance_risk.update_layout(
                height=450,
                xaxis_title="Account Balance (₹)",
                yaxis_title="Number of Accounts"
            )

            st.plotly_chart(
                fig_balance_risk,
                use_container_width=True
            )

            st.dataframe(
                high_balance_accounts.sort_values(
                    "account_balance",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No accounts exceeded the "
                "high-balance statistical threshold."
            )

    # OVERVIEW DASHBOARD

    with tab5:

        st.subheader("📊 Banking Overview")

        # KPI

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Customers",
                f"{customers['customer_id'].nunique():,}"
            )

        with col2:
            st.metric(
                "Accounts",
                f"{len(accounts):,}"
            )

        with col3:
            st.metric(
                "Transactions",
                f"{len(transactions):,}"
            )

        with col4:
            st.metric(
                "Loans",
                f"{len(loans):,}"
            )

        st.divider()

        # ACCOUNT + TRANSACTION OVERVIEW

        col1, col2 = st.columns(2)

        with col1:

            account_count = (
                accounts["account_type"]
                .value_counts()
                .reset_index()
            )

            account_count.columns = [
                "Account Type",
                "Count"
            ]

            fig = px.pie(
                account_count,
                names="Account Type",
                values="Count",
                title="Accounts Overview",
                hole=0.45
            )

            fig.update_layout(
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            if "transaction_type" in transactions.columns:

                transaction_count = (
                    transactions[
                        "transaction_type"
                    ]
                    .value_counts()
                    .reset_index()
                )

                transaction_count.columns = [
                    "Transaction Type",
                    "Count"
                ]

                fig = px.pie(
                    transaction_count,
                    names="Transaction Type",
                    values="Count",
                    title="Transactions Overview",
                    hole=0.45
                )

                fig.update_layout(
                    height=450
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # BALANCE DISTRIBUTION

        st.subheader("💰 Account Balance Distribution")

        fig_balance = px.histogram(
            accounts,
            x="account_balance",
            nbins=40,
            title="Distribution of Account Balances"
        )

        fig_balance.update_layout(
            height=450,
            xaxis_title="Account Balance (₹)",
            yaxis_title="Number of Accounts"
        )

        st.plotly_chart(
            fig_balance,
            use_container_width=True
        )

        # MONTHLY TREND

        monthly = (
            transactions
            .dropna(subset=["transaction_date"])
            .groupby(
                transactions["transaction_date"].dt.to_period("M")
            )
            .agg(
                Transactions=(
                    "transaction_amount",
                    "count"
                ),
                Amount=(
                    "transaction_amount",
                    "sum"
                )
            )
            .reset_index()
        )

        monthly["Month"] = (
            monthly["transaction_date"]
            .astype(str)
        )

        fig_trend = px.line(
            monthly,
            x="Month",
            y="Amount",
            markers=True,
            title="Monthly Transaction Value"
        )

        fig_trend.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Transaction Value (₹)"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )


# FOOTER

st.divider()

st.markdown(
    """
    <div class="footer">
        🏦 Bank Analytics Report<br>
        Built with Python • Pandas • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
