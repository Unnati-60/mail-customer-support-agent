import streamlit as st
import requests
import json
import pandas as pd

# ----------------------
# Config
# ----------------------
API_URL = "http://localhost:8000/response"  

st.set_page_config(
    page_title="Customer Support Agent",
    layout="wide"
)

# # ----------------------
# # Sidebar
# # ----------------------
st.sidebar.subheader("🧠 Agent Reasoning")


# ----------------------
# Main UI
# ----------------------
st.title("📨 Customer Support Agent")

st.markdown(
    "Paste a **customer query email or Natural language query** below. "
)

if st.button("Load Sample Example"):
    st.session_state["customer_email"] = (
        "Subject: Need update on my MacBook Air delivery\n\n"
        "Hi Team,\nI placed an order for the MacBook Air M2 last week and received the dispatch message, but ever since then the tracking hasn’t moved. It has been showing “in transit – arriving soon” for two full days now. Considering the price and importance of this purchase, this delay is stressing me out because I urgently need the laptop for remote office work starting next week.\n\nCould you please check the exact delivery status with the courier and let me know whether it is delayed or on schedule? If possible, please share the expected delivery timeline so I can plan accordingly.\n\nOrder was placed on 7th February under my account (Rohan Mehta)."
        "\nHoping for a quick response.\n"
        "Regards,\nRohan"
    )
# Input area
customer_email = st.text_area(
    "Customer Email / Query",
    height=200,
    key="customer_email",
    placeholder="Paste customer email or query here..."
)

# Submit
submit = st.button("🚀 Resolve Query")

# ----------------------
# API Call
# ----------------------
if submit and customer_email.strip():
    with st.spinner("Agent is processing the request..."):
        try:
            payload = {
                "customer_mail": customer_email
            }

            response = requests.post(API_URL, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()

            agent_response = data.get("response", "")
            agent_state = data.get("agent_state", {})

            extracted_intent = agent_state.get("customer_query")
            generated_sql = agent_state.get("sql_query_v2")
            sql_output = agent_state.get("sql_output_v2")

            st.success("Query resolved successfully")

        except Exception as e:
            st.error(f"Failed to get response from agent: {e}")
            st.stop()

    # ----------------------
    # Results Layout
    # ----------------------
    st.subheader("✉️ Final Response Email")
    st.text_area(
            label="",
            value=agent_response,
            height=400
        )
    
    
    st.sidebar.markdown("**Extracted User Intent**")
    st.sidebar.code(extracted_intent or "N/A", language="text",wrap_lines=True)

    st.sidebar.markdown("**Generated SQL**")
    st.sidebar.code(generated_sql or "No SQL generated", language="sql",wrap_lines=True)

    # SQL Output
    st.sidebar.subheader("📊 SQL Output")

    if sql_output:
        if isinstance(sql_output, list):
            try:
                df = pd.DataFrame(sql_output)
                st.sidebar.dataframe(df, use_container_width=True)
            except Exception:
                st.sidebar.json(sql_output)
        else:
            st.sidebar.json(sql_output)
    else:
        st.sidebar.info("No SQL output available")
