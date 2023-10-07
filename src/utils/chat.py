from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import ConversationalRetrievalChain

class DocumentChat:
    def __init__(self, openai_api_key: str, chain_type: str = "stuff"):
        self._chain_type = chain_type 
        self._llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0
        )
        self._db = None 

    def load_db(self, docs):
        print("[INFO] Creating embeddings...")
        embeddings = OpenAIEmbeddings()
        print("[INFO] Successfully created embeddings.")

        self._db = DocArrayInMemorySearch.from_documents(docs, embeddings)

    def load_conv_qa_chain(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(docs)

        if not self._db:
            self.load_db(docs)

        retriever = self._db.as_retriever(search_type="similarity")

        conv_qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self._llm,
            chain_type=self._chain_type,
            retriever=retriever, 
            return_source_documents=True,
            return_generated_question=True,
        )

        return conv_qa_chain 
        