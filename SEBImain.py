import streamlit as st
import google.genai as genai

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="AI Assisted SEBI Circular Finder",
    page_icon="📈",
    layout="wide"
)

# =====================================
# Gemini Client
# =====================================

try:
    google_api_key = st.secrets["google"]["api_key"]
    client = genai.Client(api_key=google_api_key)

except Exception as e:
    st.error("Unable to load Google API Key.")
    st.stop()

# =====================================
# Header
# =====================================

st.title("📈 AI Assisted SEBI Circular Finder")

st.markdown(
    """
Search SEBI circulars, generate summaries, identify actionables,
and ask AI-powered regulatory questions.
"""
)

# =====================================
# Sidebar
# =====================================

st.sidebar.header("Search Options")

search_option = st.sidebar.radio(
    "Choose Search Type",
    (
        "📅 Recent Circulars",
        "🔍 Search Specific Circular",
        "🤖 Ask AI"
    )
)

# =====================================
# RECENT CIRCULARS
# =====================================

if search_option == "📅 Recent Circulars":

    st.subheader("Find Recent SEBI Circulars")

    days = st.slider(
        "Select Time Horizon (days)",
        min_value=1,
        max_value=90,
        value=1,
        step=1
    )

    if st.button("Find Circulars"):

        prompt = f"""
You are an expert SEBI Regulatory Analyst.

Search the SEBI website (https://www.sebi.gov.in/)
and identify all important circulars issued in the recent {days} days related to Merchant Banking, PMS, Research Analyst(RA), Investment Advisor(IA).

For every circular provide:

1. Circular Title
2. Circular Number
3. Issue Date
4. Official SEBI Link
5. Executive Summary
6. Key Regulatory Changes
7. Applicability
8. Actionables
9. Compliance Timeline

Display the result in Markdown format with proper headings and tables.
"""

        with st.spinner("Searching SEBI Circulars..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.success("Report Generated Successfully!")

                st.markdown(response.text)

            except Exception as e:
                st.error(e)

# =====================================
# SEARCH SPECIFIC CIRCULAR
# =====================================

elif search_option == "🔍 Search Specific Circular":

    st.subheader("Search Specific Circular")

    circular = st.text_input(
        "Enter Circular Name / Circular Number / Topic"
    )

    st.write("Examples")

    st.write("- Cyber Security")
    st.write("- Mutual Funds")
    st.write("- Insider Trading")
    st.write("- SEBI/HO/IMD/...")
    st.write("- ESG Disclosure")

    if st.button("Search Circular"):

        if circular.strip() == "":

            st.error("Please enter a Circular Name or Topic.")

        else:

            prompt = f"""
You are an expert SEBI Regulatory Analyst.

Search the official SEBI website and internet for:

"{circular}"

Return:

# Circular Details

- Circular Title
- Circular Number
- Issue Date
- Official SEBI Link

# Executive Summary

Summarize in bullet points.

# Who is Impacted

# Key Regulatory Changes

# Actionables

Create a table:

| Action | Owner | Timeline | Priority |

# Compliance Checklist

# Important Dates

If multiple circulars exist,
display them in chronological order.
"""

            with st.spinner("Searching Circular..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.success("Circular Found!")

                    st.markdown(response.text)

                except Exception as e:

                    st.error(e)

# =====================================
# AI Q&A
# =====================================

elif search_option == "🤖 Ask AI":

    st.subheader("Ask AI About SEBI Circulars")

    question = st.text_area(
        "Ask your question",
        height=150,
        placeholder="Example: Summarize the latest cyber security circular applicable to stock brokers."
    )

    if st.button("Ask AI"):

        if question.strip() == "":

            st.error("Please enter a question.")

        else:

            prompt = f"""
You are an experienced SEBI Regulatory Consultant.

Answer the following question:

{question}

Instructions:

1. Prefer information from the official SEBI website.
2. Mention the relevant circular(s).
3. Provide official SEBI links.
4. Summarize the regulation.
5. Explain practical implications.
6. Provide actionables.
7. Create a compliance checklist whenever applicable.
8. Format the answer in Markdown.
"""

            with st.spinner("Generating AI Response..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.success("Response Generated!")

                    st.markdown(response.text)

                except Exception as e:

                    st.error(e)

# =====================================
# Footer
# =====================================

st.divider()

st.caption(
    """
AI Assisted SEBI Circular Finder

• Search recent circulars

• Search specific circulars

• Generate summaries and actionables

• Ask regulatory questions using Gemini AI
"""
)
