from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
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

        self.qa_template = qa_template = """
        You are an assistant name MVLU Bot for question-answering tasks for MVLU College, also known as Sheth Laherchand Uttamchand Jhaveri College of Arts & Sir Mathuradas Vissanji College of Science & Commerce. Using the provided context, please give a comprehensive and detailed answer to the following question. Ensure that you incorporate all relevant information from the context in your response. If you don't know the answer, simply state that "Sorry I am unable to answer that question at this time, we recommend you to visit mvlucollege.in for furhter information". 
        Question: {question} 
        Context: {context} 
        Answer:
        Do not mention that you are generating answers from context retrieved that you have recieved, **make sure that the user is not aware of the context**. Ensure all responses are formatted in markdown. Also make sure that whenever possible try to include images as well, only if the context includes any images.
        """

        self.qa_prompt = ChatPromptTemplate.from_template(self.qa_template)

        self.rag_chain  = (
            RunnableParallel(context=self.retriever | self.format_docs, question=RunnablePassthrough()) |
            self.qa_prompt |
            self.llm
        )

    def chat(self, message: str):
        output = self.rag_chain.invoke(message)
        return output.content

    def format_docs(self, docs):
        return "\n\n ------------".join(doc.page_content for doc in docs)

    def retrieve_answer(self, output):
        return output.content
