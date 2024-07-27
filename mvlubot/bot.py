from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from .message import Message
from langchain_core.messages import HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
import os


class MVLUBot():
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001")

        self.mongo_client = MongoClient(os.environ["MONGODB_URI"])
        self.db = self.mongo_client["RAG"]
        self.collection = self.db["documents"]

        self.vector_store = MongoDBAtlasVectorSearch(
            self.collection, self.embeddings, index_name="chatbot_index", text_key="content", embedding_key="summary_embeddings")

        self.retriever = self.vector_store.as_retriever()

        # For chat history
        self.contextualize_q_system_prompt = """
        Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.
        """
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        

        


        
    def generate_query_without_history(self, message:Message):
        qa_template = """
        You are an assistant name MVLU Bot for question-answering tasks for MVLU College, also known as Sheth Laherchand Uttamchand Jhaveri College of Arts & Sir Mathuradas Vissanji College of Science & Commerce. Using the provided context, please give a comprehensive and detailed answer to the following question. Ensure that you incorporate all relevant information from the context in your response. If you don't know the answer, simply state that "Sorry I am unable to answer that question at this time, we recommend you to visit mvlucollege.in for furhter information". 
        Question: {question} 
        Context: {context} 
        Answer:
        Do not mention that you are generating answers from context retrieved that you have recieved, **make sure that the user is not aware of the context**. Ensure all responses are formatted in markdown. Also make sure that whenever possible try to include images as well, only if the context includes any images.
        """

        qa_prompt = ChatPromptTemplate.from_template(qa_template)

        rag_chain  = (
            RunnableParallel(context=self.retriever | self.format_docs, question=RunnablePassthrough()) |
            qa_prompt |
            self.llm
        )

        output = rag_chain.invoke(message.message)

        return Message(role="MVLUBOT", message=output.content)

    def generate_query_with_history(self, message:Message):
        chat_history = [HumanMessage(content=msg.message) if msg.role == "USER" else msg.message for msg in message.history]
        chat_history.reverse()
        print(chat_history)

        contextualize_q_system_prompt = """
        Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.
        """

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        qa_system_prompt  = """
            You are an assistant name MVLU Bot for question-answering tasks for MVLU College, also known as Sheth Laherchand Uttamchand Jhaveri College of Arts & Sir Mathuradas Vissanji College of Science & Commerce. Using the provided context, please give a comprehensive and detailed answer to the following question. Ensure that you incorporate all relevant information from the context in your response. If you don't know the answer, simply state that "Sorry I am unable to answer that question at this time, we recommend you to visit mvlucollege.in for furhter information". 
            Context: {context} 
            Answer:
            Do not mention that you are generating answers from context retrieved that you have recieved, **make sure that the user is not aware of the context**. Ensure all responses are formatted in markdown. Also make sure that whenever possible try to include images as well, only if the context includes any images.
        """

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )


        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        output = rag_chain.invoke({"input": message.message, "chat_history": chat_history})


        return Message(
            role="MVLUBOT",
            message=output["answer"]            
        )


    def chat(self, message: Message):
        print(message)
        if message.history:
            return self.generate_query_with_history(message)

        return self.generate_query_without_history(message)

    def format_docs(self, docs):
        return "\n\n ------------".join(doc.page_content for doc in docs)

    def retrieve_answer(self, output):
        return output.content
