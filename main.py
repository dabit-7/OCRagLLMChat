import easyocr
import os
import chromadb
from langchain_ollama import OllamaLLM

def setup_chromadb():
    chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))
    collection = chroma_client.get_or_create_collection(
        name="rag_collection", metadata={"description": "OCR Text Storage"}
    )
    return collection

collection = setup_chromadb()
llm_model = "mistral"

def extract_text(image_path):
    try:
        reader = easyocr.Reader(['pt'])
        result = reader.readtext(image_path, detail=0)
        return " ".join(result)
    except Exception as e:
        return f"Erro ao processar imagem: {str(e)}"

def add_text_to_db(text, doc_id="ocr_text"):
    collection.add(documents=[text], ids=[doc_id])

def clear_db():
    collection.delete(ids=["ocr_text"])

def query_ollama(question):
    llm = OllamaLLM(model=llm_model)
    return llm.invoke(question)

def rag_pipeline(query_text):
    retrieved_docs = collection.query(query_texts=[query_text], n_results=3)
    context = " ".join([" ".join(doc) for doc in retrieved_docs["documents"] if doc]) if retrieved_docs["documents"] else "Sem contexto disponível."
    return query_ollama(f"Contexto: {context}\n\nPergunta: {query_text}\nResposta:")
