import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import time


def show_detect_fraud(conn, model):

    st.markdown("""
    <style>

    .title{

        font-size:44px;

        font-weight:bold;

        color:#38BDF8;

    }

    .subtitle{

        color:#94A3B8;

        font-size:18px;

        margin-bottom:20px;

    }

    .section{

        background:#111827;

        padding:20px;

        border-radius:15px;

        border:1px solid #1E293B;

        margin-bottom:20px;

    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(

        '<div class="title">AI Fraud Detection Center</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="subtitle">Analyze every UPI transaction using Machine Learning</div>',

        unsafe_allow_html=True

    )

    st.markdown("---")

    col1,col2=st.columns(2)

    with col1:

        amount=st.number_input(

            "Transaction Amount (₹)",

            min_value=1.0,

            value=1000.0,

            step=100.0

        )

        balance=st.number_input(

            "Account Balance (₹)",

            min_value=0.0,

            value=50000.0

        )

        transaction_hour=st.slider(

            "Transaction Hour",

            0,

            23,

            12

        )

        account_age=st.slider(

            "Account Age (Months)",

            1,

            120,

            24

        )

        daily_transactions=st.slider(

            "Transactions Today",

            1,

            20,

            3

        )

    with col2:

        sender_bank=st.selectbox(

            "Sender Bank",

            [

                "SBI",

                "HDFC",

                "ICICI",

                "Axis",

                "PNB",

                "BOB",

                "Canara",

                "Kotak"

            ]

        )

        receiver_bank=st.selectbox(

            "Receiver Bank",

            [

                "SBI",

                "HDFC",

                "ICICI",

                "Axis",

                "PNB",

                "BOB",

                "Canara",

                "Kotak"

            ]

        )

        location=st.selectbox(

            "Location",

            [

                "Delhi",

                "Mumbai",

                "Bangalore",

                "Hyderabad",

                "Chennai",

                "Kolkata",

                "Pune",

                "Ahmedabad",

                "Jaipur",

                "Lucknow"

            ]

        )

        device=st.selectbox(

            "Device",

            [

                "Android",

                "iPhone",

                "Desktop"

            ]

        )

        transaction_type=st.selectbox(

            "Transaction Type",

            [

                "Merchant",

                "P2P",

                "Recharge",

                "Bill Payment"

            ]

        )

    st.markdown("---")

    c1,c2=st.columns(2)

    with c1:

        previous_frauds=st.slider(

            "Previous Fraud Reports",

            0,

            5,

            0

        )

    with c2:

        st.write("")

        st.write("")

        new_device=st.checkbox(

            "New Device"

        )

        new_location=st.checkbox(

            "New Location"

        )

    analyze=st.button(

        "🔍 Analyze Transaction",

        use_container_width=True,

        type="primary"

    )

    if analyze:

        with st.spinner(

            "AI Engine Processing..."

        ):

            time.sleep(2)

        encoders=joblib.load(

            "models/label_encoders.pkl"

        )

        sender_bank_encoded=encoders["sender_bank"].transform(

            [sender_bank]

        )[0]

        receiver_bank_encoded=encoders["receiver_bank"].transform(

            [receiver_bank]

        )[0]

        location_encoded=encoders["location"].transform(

            [location]

        )[0]

        device_encoded=encoders["device"].transform(

            [device]

        )[0]

        transaction_type_encoded=encoders["transaction_type"].transform(

            [transaction_type]

        )[0]
        features = np.array([[

            amount,

            balance,

            transaction_hour,

            sender_bank_encoded,

            receiver_bank_encoded,

            location_encoded,

            device_encoded,

            transaction_type_encoded,

            account_age,

            daily_transactions,

            previous_frauds,

            int(new_device),

            int(new_location)

        ]])

        prediction = model.predict(

            features

        )[0]

        probability = model.predict_proba(

            features

        )[0][1]

        fraud_probability = round(

            probability * 100,

            2

        )

        if fraud_probability < 30:

            risk = "LOW"

            risk_color = "green"

        elif fraud_probability < 70:

            risk = "MEDIUM"

            risk_color = "orange"

        else:

            risk = "HIGH"

            risk_color = "red"

        st.markdown("---")

        gauge = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=fraud_probability,

                title={

                    "text":"Fraud Probability (%)"

                },

                gauge={

                    "axis":{

                        "range":[0,100]

                    },

                    "bar":{

                        "color":"darkred"

                    },

                    "steps":[

                        {

                            "range":[0,30],

                            "color":"green"

                        },

                        {

                            "range":[30,70],

                            "color":"yellow"

                        },

                        {

                            "range":[70,100],

                            "color":"red"

                        }

                    ]

                }

            )

        )

        gauge.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            font_color="white"

        )

        st.plotly_chart(

            gauge,

            use_container_width=True

        )

        m1,m2,m3 = st.columns(3)

        with m1:

            st.metric(

                "Fraud Probability",

                f"{fraud_probability}%"

            )

        with m2:

            st.metric(

                "Safe Probability",

                f"{100-fraud_probability}%"

            )

        with m3:

            st.metric(

                "Risk Level",

                risk

            )

        st.markdown("---")

        if prediction == 1:

            status = "Fraud"

            st.error(

                "🚨 Fraudulent Transaction Detected"

            )

        else:

            status = "Safe"

            st.success(

                "✅ Transaction Approved"
            )

        reasons = []

        if amount > 50000:

            reasons.append("High transaction amount detected.")

        if balance < amount:

            reasons.append("Insufficient balance before transaction.")

        if previous_frauds > 0:

            reasons.append("Customer has previous fraud history.")

        if new_device:

            reasons.append("Transaction initiated from a new device.")

        if new_location:

            reasons.append("Transaction initiated from a new location.")

        if transaction_hour >= 23 or transaction_hour <= 4:

            reasons.append("Late-night transaction detected.")

        if daily_transactions > 15:

            reasons.append("High number of daily transactions.")

        if device == "Desktop":

            reasons.append("Desktop transaction detected.")

        if len(reasons) == 0:

            reasons.append("No suspicious behaviour detected.")

        st.subheader("🧠 AI Explanation")

        for reason in reasons:

            st.write("✔", reason)

        st.markdown("---")

        st.subheader("💡 AI Recommendation")

        if fraud_probability >= 80:

            st.error("""

Block Transaction Immediately

• Verify customer identity

• Trigger OTP verification

• Notify security team

• Flag account for manual review

""")

        elif fraud_probability >= 50:

            st.warning("""

Medium Risk Transaction

• Perform OTP verification

• Monitor account activity

• Request additional authentication

""")

        else:

            st.success("""

Low Risk Transaction

• Transaction appears safe

• Continue normal processing

""")

        cursor = conn.cursor()

        cursor.execute(

            """
            INSERT INTO transactions(

                amount,

                old_balance,

                new_balance,

                upi_id,

                sender_bank,

                receiver_bank,

                location,

                device,

                transaction_type,

                status,

                fraud_probability,

                prediction,

                remarks

            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

            """,

            (

                amount,

                balance,

                balance-amount,

                "UPI-AI-001",

                sender_bank,

                receiver_bank,

                location,

                device,

                transaction_type,

                status,

                fraud_probability,

                int(prediction),

                ", ".join(reasons)

            )

        )

        conn.commit()

        st.success("Transaction saved successfully.")

        st.markdown("---")

        st.subheader("Transaction Summary")

        summary = pd.DataFrame({

            "Field":[

                "Amount",

                "Balance",

                "Hour",

                "Sender Bank",

                "Receiver Bank",

                "Location",

                "Device",

                "Transaction Type",

                "Risk",

                "Fraud Probability"

            ],

            "Value":[

                amount,

                balance,

                transaction_hour,

                sender_bank,

                receiver_bank,

                location,

                device,

                transaction_type,

                risk,

                f"{fraud_probability}%"

            ]

        })

        st.dataframe(

            summary,

            use_container_width=True,

            hide_index=True

        )
        st.balloons()

        st.markdown("---")

        csv_data = summary.to_csv(index=False).encode("utf-8")

        st.download_button(

            label="📥 Download Transaction Report",

            data=csv_data,

            file_name="transaction_report.csv",

            mime="text/csv",

            use_container_width=True

        )

        st.markdown("---")

        st.info(

            """
            AI Decision Summary

            • Prediction completed successfully

            • Transaction stored in database

            • Risk analysis generated

            • Recommendation created

            • Report ready for download
            """

        )

        if st.button(

            "🔄 Analyze Another Transaction",

            use_container_width=True

        ):

            st.rerun()

    st.markdown("---")

    st.caption(

        "UPI AI Shield Pro • Enterprise Fraud Detection Platform"

    )

                

                