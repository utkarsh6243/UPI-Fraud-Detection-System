import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_dashboard(conn):

    st.markdown("""
    <style>

    .dashboard-title{
        font-size:32px;
        font-weight:700;
        color:#38BDF8;
        margin-bottom:4px;
    }

    .dashboard-subtitle{
        font-size:14px;
        color:#94A3B8;
        margin-bottom:20px;
    }

    .metric-card{
        background:#111827;
        border-radius:14px;
        padding:18px;
        border:1px solid #1F2937;
    }

    .metric-title{
        color:#94A3B8;
        font-size:13px;
        margin-top:6px;
    }

    .metric-value{
        font-size:28px;
        font-weight:700;
        color:white;
    }

    .metric-footer{
        font-size:11px;
        color:#22C55E;
        margin-top:6px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="dashboard-title">Fraud Intelligence Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Real-Time AI Powered UPI Fraud Detection System</div>',
        unsafe_allow_html=True
    )

    st.divider()

    df = pd.read_sql_query(
        "SELECT * FROM transactions",
        conn
    )

    total_transactions = len(df)

    fraud_transactions = len(
        df[df["status"] == "Fraud"]
    )

    safe_transactions = len(
        df[df["status"] == "Safe"]
    )

    fraud_rate = 0

    if total_transactions > 0:
        fraud_rate = round(
            fraud_transactions * 100 / total_transactions,
            2
        )

    average_amount = 0

    if total_transactions > 0:
        average_amount = round(
            df["amount"].mean(),
            2
        )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">

        <div style="font-size:26px;">💳</div>

        <div class="metric-title">
        Transactions
        </div>

        <div class="metric-value">
        {total_transactions}
        </div>

        <div class="metric-footer">
        Total Records
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">

        <div style="font-size:26px;">🚨</div>

        <div class="metric-title">
        Fraud
        </div>

        <div class="metric-value">
        {fraud_transactions}
        </div>

        <div class="metric-footer" style="color:#EF4444;">
        High Risk
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">

        <div style="font-size:26px;">✅</div>

        <div class="metric-title">
        Safe
        </div>

        <div class="metric-value">
        {safe_transactions}
        </div>

        <div class="metric-footer">
        Verified
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="metric-card">

        <div style="font-size:26px;">📊</div>

        <div class="metric-title">
        Fraud Rate
        </div>

        <div class="metric-value">
        {fraud_rate}%
        </div>

        <div class="metric-footer">
        Average ₹{average_amount:,.0f}
        </div>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2, 1])
    with left:

        if total_transactions > 0:

            overview = (
                df.groupby("status")
                .size()
                .reset_index(name="Transactions")
            )

            fig = px.bar(
                overview,
                x="status",
                y="Transactions",
                color="status",
                text="Transactions",
                color_discrete_map={
                    "Fraud": "#EF4444",
                    "Safe": "#22C55E"
                },
                title="Transaction Overview"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                height=340,
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="white",
                    size=12
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=45,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No transactions available.")

    with right:

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=fraud_rate,
                number={
                    "suffix": "%",
                    "font": {
                        "size": 30
                    }
                },
                title={
                    "text": "Fraud Risk"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#EF4444"
                    },
                    "steps": [
                        {
                            "range": [0, 30],
                            "color": "#22C55E"
                        },
                        {
                            "range": [30, 70],
                            "color": "#FACC15"
                        },
                        {
                            "range": [70, 100],
                            "color": "#EF4444"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="white",
                size=12
            ),
            margin=dict(
                l=10,
                r=10,
                t=35,
                b=10
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    st.divider()

    bottom_left, bottom_right = st.columns([2, 1])
    with bottom_left:

        st.subheader("Recent Transactions")

        if total_transactions > 0:

            if "id" in df.columns:

                recent = df.sort_values(
                    by="id",
                    ascending=False
                ).head(10)

            else:

                recent = df.tail(10)

            display_columns = []

            preferred = [
                "amount",
                "status",
                "sender_bank",
                "receiver_bank",
                "location",
                "device"
            ]

            for col in preferred:

                if col in recent.columns:

                    display_columns.append(col)

            st.dataframe(
                recent[display_columns],
                use_container_width=True,
                height=320,
                hide_index=True
            )

        else:

            st.info("No transactions available.")

    with bottom_right:

        st.subheader("AI Insights")

        if total_transactions > 0:

            highest_amount = df["amount"].max()

            st.metric(
                "Highest Amount",
                f"₹{highest_amount:,.0f}"
            )

            st.metric(
                "Average Amount",
                f"₹{average_amount:,.0f}"
            )

            st.metric(
                "Fraud Rate",
                f"{fraud_rate}%"
            )

            if "device" in df.columns:

                st.info(
                    f"Most Used Device: **{df['device'].mode()[0]}**"
                )

            if "location" in df.columns:

                st.info(
                    f"Top Location: **{df['location'].mode()[0]}**"
                )

            if "sender_bank" in df.columns:

                st.info(
                    f"Top Sender Bank: **{df['sender_bank'].mode()[0]}**"
                )

            if fraud_rate < 20:

                st.success("Overall Risk Level: LOW")

            elif fraud_rate < 50:

                st.warning("Overall Risk Level: MEDIUM")

            else:

                st.error("Overall Risk Level: HIGH")

        else:

            st.info("No analytics available.")

    st.divider()

    st.subheader("Quick Statistics")

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Today's Fraud",
            fraud_transactions
        )

    with s2:

        st.metric(
            "Today's Safe",
            safe_transactions
        )

    with s3:

        protected = safe_transactions * average_amount

        st.metric(
            "Money Protected",
            f"₹{protected:,.0f}"
        )

    st.divider()
    st.subheader("Transaction Amount Distribution")

    if total_transactions > 0:

        fig = px.histogram(
            df,
            x="amount",
            nbins=20,
            title="Amount Distribution"
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="white",
                size=12
            ),
            margin=dict(
                l=20,
                r=20,
                t=45,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    summary = pd.DataFrame({

        "Metric":[
            "Total Transactions",
            "Fraud Transactions",
            "Safe Transactions",
            "Fraud Rate",
            "Average Amount"
        ],

        "Value":[
            total_transactions,
            fraud_transactions,
            safe_transactions,
            f"{fraud_rate}%",
            f"₹{average_amount:,.2f}"
        ]

    })

    st.subheader("Analytics Summary")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    csv = summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download Dashboard Report",

        data=csv,

        file_name="dashboard_report.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.divider()

    st.caption(
        "UPI AI Shield Pro • Enterprise Fraud Detection Dashboard • Version 2.0"
    )

        
        


      
      