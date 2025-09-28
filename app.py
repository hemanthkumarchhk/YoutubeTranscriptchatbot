import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from transcript_utils import fetch_transcript, combine_transcript_text
from embeddings import get_openai_embeddings, get_local_embeddings
from vectorstore import build_faiss_index, similarity_search
from qa import answer_with_openai
from export_utils import export_transcript_pdf, export_transcript_docx

try:
    import openai
except:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="YouTube Transcript Chat")
st.title("🎥 Chat with YouTube Transcript")

video_url = st.text_input("Enter a YouTube video URL:")
process_btn = st.button("Fetch Transcript")

if "index" not in st.session_state:
    st.session_state["index"] = None
    st.session_state["metadata"] = None
    st.session_state["transcript"] = None

if process_btn and video_url:
    with st.spinner("Fetching transcript..."):
        transcript = fetch_transcript(video_url)
    st.session_state["transcript"] = transcript
    text_chunks = [ {"text": entry["text"], "metadata": entry} for entry in transcript ]
    texts = [c["text"] for c in text_chunks]

    if OPENAI_API_KEY and openai:
        openai.api_key = OPENAI_API_KEY
        try:
            embeddings = get_openai_embeddings(openai, texts)
        except Exception:
            embeddings = get_local_embeddings(texts)
    else:
        embeddings = get_local_embeddings(texts)

    idx, metadata = build_faiss_index(embeddings, text_chunks)
    st.session_state["index"] = idx
    st.session_state["metadata"] = metadata
    st.success("Transcript processed!")

if st.session_state["index"]:
    st.header("Ask a question about the video")
    q = st.text_input("Your question")
    if st.button("Ask") and q:
        if OPENAI_API_KEY and openai:
            q_emb = get_openai_embeddings(openai, [q])[0]
        else:
            q_emb = get_local_embeddings([q])[0]

        results = similarity_search(st.session_state["index"], q_emb, st.session_state["metadata"], top_k=5)

        st.subheader("Answer")
        try:
            ans = answer_with_openai(openai, q, results)
            st.write(ans)
        except Exception as e:
            st.error(f"OpenAI failed: {e}")
            st.write("Here are the top relevant transcript chunks instead:")
            for r in results:
                st.write(r["metadata"]["text"])

    if st.button("Export Transcript as PDF"):
        export_transcript_pdf(st.session_state["transcript"])
        st.success("Transcript saved as transcript.pdf")

    if st.button("Export Transcript as DOCX"):
        export_transcript_docx(st.session_state["transcript"])
        st.success("Transcript saved as transcript.docx")