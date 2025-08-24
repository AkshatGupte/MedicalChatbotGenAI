from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

# Initialize everything (your existing chain.ipynb setup)
load_dotenv()
api_key1 = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key1)
index = pc.Index("medibot")

embeddings = HuggingFaceEmbeddings(model='sentence-transformers/all-MiniLM-L6-v2')

index_name = 'medibot'
vector_store = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 4})

prompt = PromptTemplate(
    template='''You are a helpful assistant. Respond to the user queries only using the following context provided,
    context: {context}, query: {query}
    If there is not specific answer then respond I dont know.
    ''',
    input_variables=['context','query']
)

def format_docs(retrieved_docs):
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'query': RunnablePassthrough()
})

llm = HuggingFaceEndpoint(
    repo_id='openai/gpt-oss-20b',
    task='text-generation',
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_ACCESS_TOKEN")
)

model = ChatHuggingFace(llm=llm)
parser = StrOutputParser()
main_chain = parallel_chain | prompt | model | parser

# Function to process medical queries (your existing chain.ipynb logic)
def process_medical_query(query):
    # This is exactly your chain.ipynb cell 10 logic
    return main_chain.invoke(query)
