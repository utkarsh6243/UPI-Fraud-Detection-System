import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_analytics(conn):

    st.markdown("""
    <style>

    .title{
        font-size:32px;
        font-weight:700;
        color:#38BDF8;
    }

    .subtitle{
        color:#94A3B8;
        font-size:14px;
        margin-bottom:20px;
    }

    .card{
        background:#111827;
        border:1px solid #1F2937;
        border-radius:14px;
        padding:18px;
    }

    .card-title{
        color:#94A3B8;
        font-size:13px;
    }

    .card-value{
        font-size:28px;
        font-weight:bold;
        color:white;
        margin-top:6px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="title">Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Real-Time Fraud Analytics</div>',
        unsafe_allow_html=True
    )

    st.divider()

    df = pd.read_sql_query(
        "SELECT * FROM transactions",
        conn
    )

    total = len(df)

    fraud = len(
        df[df["status"]=="Fraud"]
    )

    safe = len(
        df[df["status"]=="Safe"]
    )

    fraud_rate = 0

    if total > 0:

        fraud_rate = round(
            fraud * 100 / total,
            2
        )

    avg_amount = 0

    if total > 0:

        avg_amount = round(
            df["amount"].mean(),
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="card">
        <div class="card-title">Transactions</div>
        <div class="card-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="card">
        <div class="card-title">Fraud</div>
        <div class="card-value">{fraud}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="card">
        <div class="card-title">Safe</div>
        <div class="card-value">{safe}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="card">
        <div class="card-title">Fraud Rate</div>
        <div class="card-value">{fraud_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    left,right = st.columns([2,1])
    with left:

        if total > 0:

            chart = (
                df.groupby("status")
                .size()
                .reset_index(name="Count")
            )

            fig = px.pie(
                chart,
                names="status",
                values="Count",
                hole=0.60,
                color="status",
                color_discrete_map={
                    "Fraud":"#EF4444",
                    "Safe":"#22C55E"
                },
                title="Fraud vs Safe Transactions"
            )

            fig.update_layout(
                height=360,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                showlegend=True
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
                number={"suffix":"%"},
                title={"text":"Fraud Risk"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"#EF4444"},
                    "steps":[
                        {"range":[0,30],"color":"#22C55E"},
                        {"range":[30,70],"color":"#FACC15"},
                        {"range":[70,100],"color":"#EF4444"}
                    ]
                }
            )
        )

        gauge.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    st.divider()

    left,right = st.columns(2)

    with left:

        location = (
            df.groupby("location")
            .size()
            .reset_index(name="Transactions")
        )

        fig = px.bar(
            location,
            x="location",
            y="Transactions",
            color="Transactions",
            text="Transactions",
            title="Location Analysis"
        )

        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.histogram(
            df,
            x="amount",
            nbins=20,
            title="Transaction Amount Distribution"
        )

        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    left,right = st.columns([2,1])
    with left:

        st.subheader("Recent Fraud Transactions")

        fraud_df = df[df["status"] == "Fraud"]

        if len(fraud_df) > 0:

            st.dataframe(
                fraud_df[
                    [
                        "id",
                        "amount",
                        "upi_id",
                        "location",
                        "fraud_probability"
                    ]
                ].sort_values(
                    "id",
                    ascending=False
                ),
                use_container_width=True,
                height=350,
                hide_index=True
            )

        else:

            st.success("No fraudulent transactions found.")

    with right:

        st.subheader("🤖 AI Insights")

        if total > 0:

            highest_amount = df["amount"].max()

            highest_probability = df["fraud_probability"].max()

            avg_probability = round(
                df["fraud_probability"].mean(),
                2
            )

            top_location = df["location"].mode()[0]

            st.metric(
                "Highest Amount",
                f"₹{highest_amount:,.0f}"
            )

            st.metric(
                "Highest Risk",
                f"{highest_probability:.2f}%"
            )

            st.metric(
                "Average Risk",
                f"{avg_probability:.2f}%"
            )

            st.info(
                f"📍 Top Location\n\n{top_location}"
            )

            if fraud_rate < 20:

                st.success(
                    "Overall Risk Level : LOW"
                )

            elif fraud_rate < 50:

                st.warning(
                    "Overall Risk Level : MEDIUM"
                )

            else:

                st.error(
                    "Overall Risk Level : HIGH"
                )

    st.divider()

    st.subheader("Fraud Probability Analysis")

    fig = px.scatter(

        df,

        x="amount",

        y="fraud_probability",

        color="status",

        size="fraud_probability",

        hover_data=[
            "upi_id",
            "location"
        ],

        title="Amount vs Fraud Probability"

    )

    fig.update_layout(

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "Average Amount",
            f"₹{avg_amount:,.0f}"
        )

    with s2:

        st.metric(
            "Highest Amount",
            f"₹{highest_amount:,.0f}"
        )

    with s3:

        st.metric(
            "Average Probability",
            f"{avg_probability:.2f}%"
        )

    with s4:

        st.metric(
            "Top Location",
            top_location
        )

    st.divider()
    st.subheader("Analytics Summary")

    summary = pd.DataFrame({

        "Metric":[

            "Total Transactions",

            "Fraud Transactions",

            "Safe Transactions",

            "Fraud Rate",

            "Average Amount",

            "Highest Amount",

            "Average Fraud Probability",

            "Highest Fraud Probability"

        ],

        "Value":[

            total,

            fraud,

            safe,

            f"{fraud_rate}%",

            f"₹{avg_amount:,.2f}",

            f"₹{highest_amount:,.2f}",

            f"{avg_probability:.2f}%",

            f"{highest_probability:.2f}%"

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("Top 5 Highest Risk Transactions")

    if total > 0:

        highest_risk = df.sort_values(

            "fraud_probability",

            ascending=False

        ).head(5)

        st.dataframe(

            highest_risk[

                [

                    "id",

                    "upi_id",

                    "amount",

                    "location",

                    "status",

                    "fraud_probability"

                ]

            ],

            use_container_width=True,

            hide_index=True

        )

    st.divider()

    csv = df.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        label="📥 Download Analytics Report",

        data=csv,

        file_name="analytics_report.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.markdown("""

    <div style="

        text-align:center;

        color:#94A3B8;

        padding:20px;

        font-size:13px;

    ">

        <hr>

        <b>UPI Fraud Detection System</b><br>

        AI Powered Analytics Dashboard

    </div>

    """, unsafe_allow_html=True)
    

        

        