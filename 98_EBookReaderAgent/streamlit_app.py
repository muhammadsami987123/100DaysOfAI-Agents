"""
Streamlit UI for EBookReaderAgent
Optional web interface for easy interaction
"""

import streamlit as st
import os
from pathlib import Path
from agent import EBookReaderAgent
from utils.llm_service import LLMService
from config import Config

# Page configuration
st.set_page_config(
    page_title="EBookReaderAgent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.book_loaded = False
    st.session_state.book_info = None
    st.session_state.chapters = []


def initialize_agent():
    """Initialize the agent"""
    if st.session_state.agent is None:
        llm_service = LLMService()
        st.session_state.agent = EBookReaderAgent(llm_service=llm_service)


def load_book_from_file(file):
    """Load and parse a book file"""
    initialize_agent()
    
    # Save uploaded file
    upload_dir = Path(Config.UPLOAD_FOLDER)
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.name
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    # Load book
    with st.spinner("Parsing book file..."):
        result = st.session_state.agent.load_book(str(file_path))
    
    if result['success']:
        st.session_state.book_loaded = True
        book_info = st.session_state.agent.get_book_info()
        st.session_state.book_info = book_info
        if book_info['success']:
            st.session_state.chapters = book_info['chapters']
        st.success(f"✅ {result['message']}")
        return True
    else:
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        return False


def load_book_from_url(url):
    """Load and parse a book from URL"""
    initialize_agent()
    
    # Load book from URL
    with st.spinner("Downloading book from URL..."):
        result = st.session_state.agent.load_book(url)
    
    if result['success']:
        st.session_state.book_loaded = True
        book_info = st.session_state.agent.get_book_info()
        st.session_state.book_info = book_info
        if book_info['success']:
            st.session_state.chapters = book_info['chapters']
        st.success(f"✅ {result['message']}")
        return True
    else:
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        return False


# Header
st.markdown('<h1 class="main-header">📚 EBookReaderAgent</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">AI-Powered eBook Reader and Analyzer</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # LLM Selection
    llm_choice = st.selectbox(
        "Select LLM",
        ["gemini", "openai"],
        index=0 if Config.DEFAULT_LLM == "gemini" else 1
    )
    
    if st.session_state.agent:
        st.session_state.agent.llm_service.set_llm(llm_choice)
    
    st.divider()
    
    # API Status
    st.subheader("🔑 API Status")
    if st.session_state.agent:
        gemini_available = st.session_state.agent.llm_service.gemini_client is not None
        openai_available = st.session_state.agent.llm_service.openai_client is not None
        
        if gemini_available:
            st.success("✅ Gemini API: Available")
        else:
            st.warning("⚠️ Gemini API: Not configured")
        
        if openai_available:
            st.success("✅ OpenAI API: Available")
        else:
            st.warning("⚠️ OpenAI API: Not configured")
    
    st.divider()
    
    # Instructions
    st.subheader("📖 How to Use")
    st.markdown("""
    1. **Upload** a PDF or ePub file
    2. **View** book information
    3. **Select** an action:
       - Summarize chapters
       - Get key takeaways
       - Extract quotes
       - Ask questions
    4. **Export** results if needed
    """)


# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "📖 Book Info", "⚡ Actions", "❓ Q&A"])

# Tab 1: Upload
with tab1:
    st.header("Upload Book")
    
    # Option selection
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload File", "🔗 Enter URL"],
        horizontal=True
    )
    
    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Choose a PDF or ePub file",
            type=['pdf', 'epub'],
            help="Upload a PDF or ePub file to analyze"
        )
        
        if uploaded_file is not None:
            if st.button("📚 Load Book", type="primary"):
                load_book_from_file(uploaded_file)
    
    else:  # URL input
        book_url = st.text_input(
            "Enter book URL",
            placeholder="https://example.com/book.pdf",
            help="Enter a public URL to a PDF or ePub file"
        )
        
        if book_url:
            if st.button("📚 Load Book from URL", type="primary"):
                if book_url.startswith(('http://', 'https://')):
                    load_book_from_url(book_url)
                else:
                    st.error("❌ Please enter a valid URL starting with http:// or https://")
    
    if st.session_state.book_loaded:
        st.success("✅ Book loaded successfully!")

# Tab 2: Book Info
with tab2:
    if not st.session_state.book_loaded:
        st.info("👆 Please upload a book file first")
    else:
        st.header("Book Information")
        
        if st.session_state.book_info and st.session_state.book_info['success']:
            metadata = st.session_state.book_info['metadata']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Title", metadata['title'])
                st.metric("Author", metadata['author'])
            
            with col2:
                st.metric("Pages", metadata['total_pages'])
                st.metric("Chapters", metadata['total_chapters'])
            
            with col3:
                st.metric("Word Count", f"{metadata['word_count']:,}")
                st.metric("Reading Time", metadata['estimated_reading_time']['formatted'])
            
            st.divider()
            
            st.subheader("📑 Chapters")
            for chapter in st.session_state.chapters:
                with st.expander(f"Chapter {chapter['number']}: {chapter['title']}"):
                    st.write(f"**Word Count:** {chapter['word_count']:,} words")

# Tab 3: Actions
with tab3:
    if not st.session_state.book_loaded:
        st.info("👆 Please upload a book file first")
    else:
        st.header("Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Summarize All Chapters", type="primary", use_container_width=True):
                with st.spinner("Generating summaries for all chapters..."):
                    result = st.session_state.agent.summarize_all_chapters()
                    
                    if result['success']:
                        st.subheader("Chapter Summaries")
                        for summary in result['summaries']:
                            with st.expander(f"Chapter {summary['chapter_number']}: {summary['chapter_title']}"):
                                st.write(summary['summary'])
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
            
            if st.button("💡 Get Key Takeaways", type="primary", use_container_width=True):
                num_takeaways = st.slider("Number of takeaways", 5, 20, 10, key="takeaways_slider")
                
                with st.spinner("Extracting key takeaways..."):
                    result = st.session_state.agent.get_key_takeaways(num_takeaways)
                    
                    if result['success']:
                        st.subheader("Key Takeaways")
                        if result.get('takeaways') and len(result['takeaways']) > 0:
                            for i, takeaway in enumerate(result['takeaways'], 1):
                                st.markdown(f"**{i}.** {takeaway}")
                        else:
                            st.markdown(result.get('formatted_text', 'No takeaways available'))
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
        
        with col2:
            if st.button("💬 Get Important Quotes", type="primary", use_container_width=True):
                num_quotes = st.slider("Number of quotes", 3, 10, 5, key="quotes_slider")
                
                with st.spinner("Extracting important quotes..."):
                    result = st.session_state.agent.get_important_quotes(num_quotes=num_quotes)
                    
                    if result['success']:
                        st.subheader("Important Quotes")
                        if result.get('quotes') and len(result['quotes']) > 0:
                            for i, quote in enumerate(result['quotes'], 1):
                                st.markdown(f'**{i}.** "{quote["quote"]}"')
                                if quote.get('context'):
                                    st.caption(f"Context: {quote['context']}")
                        else:
                            st.markdown(result.get('formatted_text', 'No quotes available'))
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
            
            if st.button("🔍 Full Book Analysis", type="primary", use_container_width=True):
                with st.spinner("Performing full book analysis..."):
                    result = st.session_state.agent.analyze_book(
                        include_summaries=True,
                        include_takeaways=True,
                        include_quotes=True
                    )
                    
                    if result['success']:
                        st.success("✅ Analysis complete!")
                        
                        # Display summaries
                        if result.get('chapter_summaries') and result['chapter_summaries']['success']:
                            st.subheader("Chapter Summaries")
                            for summary in result['chapter_summaries']['summaries']:
                                with st.expander(f"Chapter {summary['chapter_number']}: {summary['chapter_title']}"):
                                    st.write(summary['summary'])
                        
                        # Display takeaways
                        if result.get('key_takeaways') and result['key_takeaways']['success']:
                            st.subheader("Key Takeaways")
                            takeaways = result['key_takeaways']
                            if takeaways.get('takeaways'):
                                for i, takeaway in enumerate(takeaways['takeaways'], 1):
                                    st.markdown(f"**{i}.** {takeaway}")
                            else:
                                st.markdown(takeaways.get('formatted_text', ''))
                        
                        # Display quotes
                        if result.get('important_quotes') and result['important_quotes']['success']:
                            st.subheader("Important Quotes")
                            quotes = result['important_quotes']
                            if quotes.get('quotes'):
                                for i, quote in enumerate(quotes['quotes'], 1):
                                    st.markdown(f'**{i}.** "{quote["quote"]}"')
                            else:
                                st.markdown(quotes.get('formatted_text', ''))
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
        
        # Chapter-specific summary
        st.divider()
        st.subheader("📑 Summarize Specific Chapter")
        
        if st.session_state.chapters:
            chapter_options = {f"Chapter {ch['number']}: {ch['title']}": ch['number'] 
                              for ch in st.session_state.chapters}
            selected_chapter = st.selectbox("Select Chapter", list(chapter_options.keys()))
            
            if st.button("📝 Summarize Chapter", type="secondary"):
                chapter_num = chapter_options[selected_chapter]
                with st.spinner(f"Generating summary for {selected_chapter}..."):
                    result = st.session_state.agent.summarize_chapter(chapter_num)
                    
                    if result['success']:
                        st.subheader(f"Chapter {result['chapter_number']}: {result['chapter_title']}")
                        st.write(result['summary'])
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")

# Tab 4: Q&A
with tab4:
    if not st.session_state.book_loaded:
        st.info("👆 Please upload a book file first")
    else:
        st.header("Ask Questions")
        st.markdown("Ask questions about the book content and get AI-powered answers.")
        
        # Chapter selection for context
        chapter_context = st.selectbox(
            "Chapter Context (Optional)",
            ["All Chapters"] + [f"Chapter {ch['number']}: {ch['title']}" 
                               for ch in st.session_state.chapters],
            help="Select a specific chapter for context, or 'All Chapters' for general questions"
        )
        
        # Question input
        question = st.text_input(
            "Enter your question",
            placeholder="e.g., What is the main theme of this book?",
            help="Ask any question about the book content"
        )
        
        if st.button("❓ Ask Question", type="primary"):
            if question:
                # Parse chapter number if selected
                chapter_num = None
                if chapter_context != "All Chapters":
                    try:
                        chapter_num = int(chapter_context.split(":")[0].replace("Chapter", "").strip())
                    except:
                        pass
                
                with st.spinner("Thinking..."):
                    result = st.session_state.agent.ask_question(question, chapter_num)
                    
                    if result['success']:
                        st.subheader("Answer")
                        st.write(result['answer'])
                        if result.get('chapter_context'):
                            st.caption(f"Context: {result['chapter_context']}")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
            else:
                st.warning("Please enter a question")
        
        # Example questions
        st.divider()
        st.subheader("💡 Example Questions")
        example_questions = [
            "What is the main theme of this book?",
            "What are the key concepts discussed?",
            "What is the author's main argument?",
            "What are the most important lessons?",
            "What is the conclusion of the book?"
        ]
        
        for i, example in enumerate(example_questions, 1):
            if st.button(f"💬 {example}", key=f"example_{i}", use_container_width=True):
                st.session_state[f"question_input"] = example
                st.rerun()

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: #666;'>Made with ❤️ as part of #100DaysOfAI-Agents</p>",
    unsafe_allow_html=True
)

