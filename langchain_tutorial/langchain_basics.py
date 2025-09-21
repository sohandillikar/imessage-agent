"""
LangChain Tutorial for Beginners
===============================

This tutorial teaches you the fundamentals of LangChain through practical examples.
We'll build a personal AI assistant that can answer questions about your life.

Author: AI Assistant
Purpose: Educational LangChain tutorial
"""

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS  # Free alternative to Pinecone
from langchain.chains import RetrievalQA
from langchain.schema import Document

# Load environment variables
load_dotenv()

# =============================================================================
# STEP 1: BASIC LLM USAGE
# =============================================================================

def step1_basic_llm():
    """
    Step 1: Learn how to use LangChain with basic LLM calls.
    
    This shows the foundation - how to make simple calls to language models.
    """
    print("=" * 60)
    print("STEP 1: BASIC LLM USAGE")
    print("=" * 60)
    
    # Initialize the LLM
    llm = OpenAI(temperature=0.7)  # temperature controls randomness (0-1)
    
    # Simple text generation
    print("\n1. Simple text generation:")
    response = llm.invoke("Tell me a fun fact about cats.")
    print(f"Response: {response}")
    
    # Multiple prompts
    print("\n2. Multiple prompts:")
    prompts = [
        "What's the capital of France?",
        "Explain photosynthesis in one sentence.",
        "What's 2+2?"
    ]
    
    for prompt in prompts:
        response = llm.invoke(prompt)
        print(f"Q: {prompt}")
        print(f"A: {response}\n")

def step2_chat_models():
    """
    Step 2: Learn about chat models and message types.
    
    Chat models are more structured and support conversation history.
    """
    print("=" * 60)
    print("STEP 2: CHAT MODELS AND MESSAGES")
    print("=" * 60)
    
    # Initialize chat model
    chat = ChatOpenAI(temperature=0.7)
    
    # Single message
    print("\n1. Single message:")
    message = HumanMessage(content="Hello! What's your name?")
    response = chat.invoke([message])
    print(f"Human: {message.content}")
    print(f"AI: {response.content}")
    
    # Conversation with system message
    print("\n2. Conversation with system message:")
    messages = [
        SystemMessage(content="You are a helpful assistant that loves to teach."),
        HumanMessage(content="What is machine learning?"),
        AIMessage(content="Machine learning is a subset of AI that enables computers to learn from data."),
        HumanMessage(content="Can you give me an example?")
    ]
    
    response = chat.invoke(messages)
    print(f"AI: {response.content}")
    
    # Multiple messages at once
    print("\n3. Multiple messages:")
    conversation = [
        HumanMessage(content="Hi there!"),
        AIMessage(content="Hello! How can I help you today?"),
        HumanMessage(content="I'm learning about LangChain. What should I know?"),
        AIMessage(content="LangChain is a framework for building AI applications. It helps you connect different AI tools together."),
        HumanMessage(content="That sounds interesting! Can you tell me more?")
    ]
    
    response = chat.invoke(conversation)
    print(f"AI: {response.content}")

# =============================================================================
# STEP 3: PROMPT TEMPLATES
# =============================================================================

def step3_prompt_templates():
    """
    Step 3: Learn about prompt templates for consistent, reusable prompts.
    
    Prompt templates help you create structured prompts with variables.
    """
    print("=" * 60)
    print("STEP 3: PROMPT TEMPLATES")
    print("=" * 60)
    
    # Basic prompt template
    print("\n1. Basic prompt template:")
    template = "You are a {role}. Explain {topic} in a {style} way."
    
    prompt = PromptTemplate(
        input_variables=["role", "topic", "style"],
        template=template
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(
        role="science teacher",
        topic="gravity",
        style="simple"
    )
    
    print(f"Formatted prompt: {formatted_prompt}")
    
    # Use with LLM
    llm = OpenAI(temperature=0.7)
    response = llm.invoke(formatted_prompt)
    print(f"Response: {response}")
    
    # Chat prompt template
    print("\n2. Chat prompt template:")
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a {role}."),
        ("human", "Explain {topic} in a {style} way.")
    ])
    
    chat = ChatOpenAI(temperature=0.7)
    messages = chat_template.format_messages(
        role="friendly tutor",
        topic="photosynthesis",
        style="fun and engaging"
    )
    
    response = chat.invoke(messages)
    print(f"Response: {response.content}")
    
    # Template with examples
    print("\n3. Template with examples:")
    example_template = """
    You are a {role}. Here are some examples of how to explain things:
    
    Example 1: {example1}
    Example 2: {example2}
    
    Now explain {topic} in the same style.
    """
    
    prompt_with_examples = PromptTemplate(
        input_variables=["role", "example1", "example2", "topic"],
        template=example_template
    )
    
    formatted = prompt_with_examples.format(
        role="math tutor",
        example1="2+2=4 because you have 2 apples and add 2 more apples, giving you 4 apples total.",
        example2="5×3=15 because you have 5 groups of 3 items each, which equals 15 items total.",
        topic="division"
    )
    
    print(f"Formatted prompt: {formatted}")
    response = llm.invoke(formatted)
    print(f"Response: {response}")

# =============================================================================
# STEP 4: CHAINS
# =============================================================================

def step4_chains():
    """
    Step 4: Learn about chains - connecting LLMs with prompts and other components.
    
    Chains are the building blocks of LangChain applications.
    """
    print("=" * 60)
    print("STEP 4: CHAINS")
    print("=" * 60)
    
    # Basic LLM chain
    print("\n1. Basic LLM chain:")
    template = "You are a {role}. Explain {topic} in a {style} way."
    prompt = PromptTemplate(
        input_variables=["role", "topic", "style"],
        template=template
    )
    
    llm = OpenAI(temperature=0.7)
    chain = prompt | llm  # Modern RunnableSequence syntax
    
    # Run the chain
    result = chain.invoke({"role": "science teacher", "topic": "DNA", "style": "simple"})
    print(f"Result: {result}")
    
    # Chain with multiple inputs
    print("\n2. Chain with multiple inputs:")
    multi_template = """
    You are a {role} helping a {student_level} student.
    
    Topic: {topic}
    Key points to cover: {key_points}
    Style: {style}
    
    Provide a clear explanation.
    """
    
    multi_prompt = PromptTemplate(
        input_variables=["role", "student_level", "topic", "key_points", "style"],
        template=multi_template
    )
    
    multi_chain = multi_prompt | llm  # Modern RunnableSequence syntax
    
    result = multi_chain.invoke({
        "role": "biology teacher",
        "student_level": "high school",
        "topic": "cell division",
        "key_points": "mitosis, meiosis, chromosomes",
        "style": "engaging and visual"
    })
    print(f"Result: {result}")
    
    # Chain with different LLM
    print("\n3. Chain with different LLM:")
    chat_llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")
    chat_chain = prompt | chat_llm  # Modern RunnableSequence syntax
    
    result = chat_chain.invoke({"role": "poet", "topic": "sunset", "style": "beautiful and lyrical"})
    print(f"Result: {result}")

# =============================================================================
# STEP 5: MEMORY
# =============================================================================

def step5_memory():
    """
    Step 5: Learn about memory in LangChain.
    
    Memory allows your AI to remember previous parts of the conversation.
    """
    print("=" * 60)
    print("STEP 5: MEMORY")
    print("=" * 60)
    
    # Conversation with memory
    print("\n1. Conversation with memory:")
    
    # Initialize chat model
    llm = ChatOpenAI(temperature=0.7)
    
    # Create a simple chain with memory
    def get_session_history(session_id: str):
        return InMemoryChatMessageHistory()
    
    # Create conversation with memory
    conversation_with_memory = RunnableWithMessageHistory(
        llm,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    
    # First message
    print("First message:")
    response1 = conversation_with_memory.invoke(
        {"input": "Hi! My name is Alex and I love pizza."},
        config={"configurable": {"session_id": "test-session"}}
    )
    print(f"AI: {response1.content}")
    
    # Second message (AI should remember the name)
    print("\nSecond message:")
    response2 = conversation_with_memory.invoke(
        {"input": "What's my name and what do I love?"},
        config={"configurable": {"session_id": "test-session"}}
    )
    print(f"AI: {response2.content}")
    
    # Third message (AI should remember the conversation)
    print("\nThird message:")
    response3 = conversation_with_memory.invoke(
        {"input": "Can you recommend a pizza place?"},
        config={"configurable": {"session_id": "test-session"}}
    )
    print(f"AI: {response3.content}")
    
    # Show memory contents
    history = get_session_history("test-session")
    print(f"\nMemory contents: {len(history.messages)} messages")
    for i, msg in enumerate(history.messages):
        print(f"  {i+1}. {msg.type}: {msg.content}")
    
    print("Memory cleared!")

# =============================================================================
# STEP 6: DOCUMENT LOADING AND PROCESSING
# =============================================================================

def step6_document_processing():
    """
    Step 6: Learn how to load and process documents.
    
    This is essential for building RAG systems that can answer questions about your documents.
    """
    print("=" * 60)
    print("STEP 6: DOCUMENT PROCESSING")
    print("=" * 60)
    
    # Create a sample document
    sample_text = """
    Personal Information about Alex:
    
    Alex is a 25-year-old software engineer who lives in San Francisco.
    Alex works at TechCorp as a senior developer, focusing on Python and machine learning.
    Alex loves hiking, photography, and cooking Italian food.
    Alex has a golden retriever named Max who loves to play fetch.
    Alex is planning a trip to Japan next year to learn about Japanese culture.
    Alex's favorite programming language is Python, and they enjoy building AI applications.
    Alex is currently learning about LangChain and wants to build a personal AI assistant.
    """
    
    # Save sample document
    with open("./sample_document.txt", "w") as f:
        f.write(sample_text)
    
    # Load document
    print("\n1. Loading document:")
    loader = TextLoader("./sample_document.txt")
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s)")
    print(f"Document content: {documents[0].page_content[:100]}...")
    
    # Split document into chunks
    print("\n2. Splitting document into chunks:")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # Split into chunks of 200 characters
        chunk_overlap=50  # Overlap 50 characters between chunks
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk.page_content[:100]}...")
    
    return chunks

# =============================================================================
# STEP 7: EMBEDDINGS AND VECTOR STORES
# =============================================================================

def step7_embeddings_and_vectorstore(chunks):
    """
    Step 7: Learn about embeddings and vector stores.
    
    This is the core of RAG - converting text to vectors and storing them for similarity search.
    """
    print("=" * 60)
    print("STEP 7: EMBEDDINGS AND VECTOR STORES")
    print("=" * 60)
    
    # Create embeddings
    print("\n1. Creating embeddings:")
    embeddings = OpenAIEmbeddings()
    
    # Create vector store (using FAISS - free alternative to Pinecone)
    print("\n2. Creating vector store:")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print(f"Vector store created with {vectorstore.index.ntotal} vectors")
    
    # Search for similar documents
    print("\n3. Searching for similar documents:")
    query = "What does Alex do for work?"
    similar_docs = vectorstore.similarity_search(query, k=2)
    
    print(f"Query: {query}")
    print("Similar documents:")
    for i, doc in enumerate(similar_docs):
        print(f"  {i+1}. {doc.page_content}")
    
    # Search with scores
    print("\n4. Searching with similarity scores:")
    similar_docs_with_scores = vectorstore.similarity_search_with_score(query, k=2)
    
    for i, (doc, score) in enumerate(similar_docs_with_scores):
        print(f"  {i+1}. Score: {score:.3f} - {doc.page_content}")
    
    return vectorstore

# =============================================================================
# STEP 8: RAG (RETRIEVAL AUGMENTED GENERATION)
# =============================================================================

def step8_rag(vectorstore):
    """
    Step 8: Learn about RAG - combining retrieval with generation.
    
    This is the complete RAG pipeline that retrieves relevant documents and uses them to generate answers.
    """
    print("=" * 60)
    print("STEP 8: RAG (RETRIEVAL AUGMENTED GENERATION)")
    print("=" * 60)
    
    # Create RAG chain
    print("\n1. Creating RAG chain:")
    llm = ChatOpenAI(temperature=0.7)
    
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" means put all retrieved docs in the prompt
        retriever=retriever,
        return_source_documents=True
    )
    
    # Test the RAG chain
    print("\n2. Testing RAG chain:")
    questions = [
        "What does Alex do for work?",
        "What are Alex's hobbies?",
        "Tell me about Alex's pet.",
        "What is Alex planning for next year?",
        "What programming language does Alex like?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        result = qa_chain({"query": question})
        print(f"Answer: {result['result']}")
        print(f"Source documents: {len(result['source_documents'])}")

# =============================================================================
# STEP 9: BUILDING A COMPLETE AI ASSISTANT
# =============================================================================

def step9_complete_assistant():
    """
    Step 9: Build a complete AI assistant that combines everything we've learned.
    
    This creates a personal AI assistant that can answer questions about your life.
    """
    print("=" * 60)
    print("STEP 9: COMPLETE AI ASSISTANT")
    print("=" * 60)
    
    # Create personal knowledge base
    personal_facts = [
        "Sohan is a software engineer who loves building AI applications.",
        "Sohan has a girlfriend named Ishani who lives in San Francisco.",
        "Sohan works at TechCorp and recently started a new project using LangChain.",
        "Sohan enjoys hiking, photography, and learning about new technologies.",
        "Sohan is currently learning about RAG and vector databases.",
        "Sohan has a cat named Whiskers who loves to play with yarn.",
        "Sohan's favorite programming language is Python.",
        "Sohan is planning a trip to Japan next year with Ishani."
    ]
    
    # Convert to documents
    documents = [Document(page_content=fact) for fact in personal_facts]
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Create RAG chain
    llm = ChatOpenAI(temperature=0.7)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    # Interactive chat
    print("\nPersonal AI Assistant - Ask me anything about Sohan!")
    print("Type 'quit' to exit, 'help' for commands")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("- Ask any question about Sohan")
                print("- 'quit' to exit")
                print("- 'help' for this message")
                continue
            elif not user_input:
                continue
            
            # Get answer using RAG
            result = qa_chain({"query": user_input})
            print(f"\nAI: {result['result']}")
            
            # Show sources
            if result['source_documents']:
                print(f"\nSources used:")
                for i, doc in enumerate(result['source_documents'], 1):
                    print(f"  {i}. {doc.page_content}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

# =============================================================================
# STEP 10: ADVANCED FEATURES
# =============================================================================

def step10_advanced_features():
    """
    Step 10: Learn about advanced LangChain features.
    
    This covers more sophisticated features for building production applications.
    """
    print("=" * 60)
    print("STEP 10: ADVANCED FEATURES")
    print("=" * 60)
    
    # Custom prompt template with examples
    print("\n1. Custom prompt template with examples:")
    
    template = """
    You are a helpful assistant. Here are some examples of how to respond:
    
    Example 1:
    Human: What's the weather like?
    Assistant: I don't have access to real-time weather data, but I can help you find weather information online.
    
    Example 2:
    Human: Can you help me with my homework?
    Assistant: I'd be happy to help with your homework! What subject are you working on?
    
    Now respond to this question: {question}
    """
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template=template
    )
    
    llm = ChatOpenAI(temperature=0.3)
    chain = prompt | llm  # Modern RunnableSequence syntax
    
    response = chain.invoke({"question": "Can you help me learn Python?"})
    print(f"Response: {response}")
    
    # Chain with multiple steps
    print("\n2. Chain with multiple steps:")
    
    # Step 1: Analyze the question
    analyze_template = "Analyze this question and determine the topic: {question}"
    analyze_prompt = PromptTemplate(
        input_variables=["question"],
        template=analyze_template
    )
    analyze_chain = analyze_prompt | llm  # Modern RunnableSequence syntax
    
    # Step 2: Generate response based on topic
    response_template = "The topic is: {topic}. Now provide a helpful response to: {question}"
    response_prompt = PromptTemplate(
        input_variables=["topic", "question"],
        template=response_template
    )
    response_chain = response_prompt | llm  # Modern RunnableSequence syntax
    
    # Run the multi-step chain
    question = "How do I learn machine learning?"
    topic = analyze_chain.invoke({"question": question})
    final_response = response_chain.invoke({"topic": topic, "question": question})
    
    print(f"Question: {question}")
    print(f"Topic: {topic}")
    print(f"Response: {final_response}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main function that runs all the tutorial steps.
    """
    print("LangChain Tutorial for Beginners")
    print("===============================")
    print("\nThis tutorial will teach you LangChain step by step.")
    print("Each step builds on the previous one.")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\nERROR: Please set your OPENAI_API_KEY in the .env file")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    try:
        # Run all tutorial steps
        """
        step1_basic_llm()
        input("\nPress Enter to continue to Step 2...")
        
        step2_chat_models()
        input("\nPress Enter to continue to Step 3...")
        
        step3_prompt_templates()
        input("\nPress Enter to continue to Step 4...")
        
        step4_chains()
        """
        input("\nPress Enter to continue to Step 5...")
        
        step5_memory()
        """
        input("\nPress Enter to continue to Step 6...")
        
        chunks = step6_document_processing()
        input("\nPress Enter to continue to Step 7...")
        
        vectorstore = step7_embeddings_and_vectorstore(chunks)
        input("\nPress Enter to continue to Step 8...")
        
        step8_rag(vectorstore)
        input("\nPress Enter to continue to Step 9...")
        
        step9_complete_assistant()
        input("\nPress Enter to continue to Step 10...")
        
        step10_advanced_features()
        """
        
        print("\n" + "=" * 60)
        print("TUTORIAL COMPLETE!")
        print("=" * 60)
        print("\nYou've learned the fundamentals of LangChain!")
        print("You can now build your own AI applications.")
        print("\nNext steps:")
        print("1. Experiment with different models and parameters")
        print("2. Try building your own personal AI assistant")
        print("3. Explore more advanced features in the LangChain documentation")
        print("4. Consider using Pinecone for production vector storage")
        
    except Exception as e:
        print(f"\nError running tutorial: {e}")
        print("Make sure you have set your OPENAI_API_KEY correctly.")

if __name__ == "__main__":
    main()
