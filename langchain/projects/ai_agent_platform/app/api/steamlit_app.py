import streamlit as st
import httpx
import time
from datetime import datetime

# Backend API endpoint
API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Code Assistant", page_icon="🤖")
st.title("🤖 AI Code Assistant")

st.markdown("Submit your code or requirement below and let the agent generate reviews, tests or optimizations.")

user_input = st.text_area("Enter your code or instruction here:", height=250)

if st.button("Submit to AI Agent"):

    if not user_input.strip():
        st.error("Please enter something before submitting.")
    else:
        # Step 1 → Send input to FastAPI backend
        with st.spinner("Submitting request to AI agent..."):
            response = httpx.post(f"{API_URL}/agent", json={"input": user_input})

            if response.status_code != 200:
                st.error("Failed to submit request.")
            else:
                data = response.json()
                task_id = data.get("task_id")

                st.success("Task submitted successfully.")
                st.write(f"**Task ID:** `{task_id}`")
                st.write("Fetching results...")

                # Step 2 → Polling for result
                result = None

                poll_placeholder = st.empty()

                while True:
                    poll_response = httpx.get(f"{API_URL}/agent/{task_id}")

                    if poll_response.status_code != 200:
                        poll_placeholder.error("Failed to fetch task status.")
                        break

                    result_data = poll_response.json()
                    status = result_data.get("status")
                    poll_placeholder.info(f"Task Status: `{status}` (Polling every 5 sec...)")

                    if status == "completed":
                        result = result_data.get("result")
                        break
                    elif status == "failed":
                        result = f"❌ Failed: {result_data.get('result')}"
                        break
                    else:
                        time.sleep(5)

                # Step 3 → Display result
                poll_placeholder.empty()

                if result:
                    st.subheader("✅ AI Agent Result")
                    st.markdown(result)

                    # Optional - save in session for history
                    if "history" not in st.session_state:
                        st.session_state.history = []

                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "task_id": task_id,
                        "input": user_input,
                        "output": result
                    })

if "history" in st.session_state:
    st.sidebar.header("Previous Runs")

    for record in reversed(st.session_state.history[-5:]):  # Show last 5
        with st.sidebar.expander(f"{record['timestamp']} → Task {record['task_id']}"):
            st.markdown(f"**Input:**\n\n{record['input']}")
            st.markdown("---")
            st.markdown(f"**Output:**\n\n{record['output']}")