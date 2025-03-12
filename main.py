import easyocr
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from langchain_ollama import OllamaLLM
import chromadb
import os
import threading

# Configurar ChromaDB
llm_model = "mistral"
chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))
collection_name = "rag_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name, metadata={"description": "OCR Text Storage"}
)

def extract_text(image_path):
    reader = easyocr.Reader(['pt'])
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)

def add_text_to_db(text):
    collection.add(documents=[text], ids=["ocr_text"])

def query_ollama(question):
    llm = OllamaLLM(model=llm_model)
    return llm.invoke(question)

def rag_pipeline(query_text):
    retrieved_docs = collection.query(query_texts=[query_text], n_results=1)
    context = " ".join(retrieved_docs["documents"][0]) if retrieved_docs["documents"] else "Sem contexto disponível."
    augmented_prompt = f"Contexto: {context}\n\nPergunta: {query_text}\nResposta:"
    return query_ollama(augmented_prompt)

def on_send_message(event=None):
    user_input = chat_input.get()
    if user_input.strip():
        chat_box.insert(tk.END, f"Você: {user_input}\n", "user")
        chat_input.delete(0, tk.END)
        response = rag_pipeline(user_input)
        chat_box.insert(tk.END, f"Ollama: {response}\n", "ollama")
    if user_input.lower().strip() == "sair":
        root.quit()

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        loading_label.pack()
        threading.Thread(target=process_image, args=(file_path,), daemon=True).start()

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        threading.Thread(target=process_folder, args=(folder_path,)).start()

def process_image(file_path):
    text = extract_text(file_path)
    collection.delete(ids=["ocr_text"])  # Limpa base anterior
    add_text_to_db(text)
    loading_label.pack_forget()
    chat_box.insert(tk.END, "Nova imagem processada. Agora você pode fazer perguntas.\n", "system")

def process_folder(folder_path):
    loading_label.pack()
    root.update_idletasks()
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(folder_path, filename)
            text = extract_text(image_path)
            collection.add(documents=[text], ids=[filename])
    loading_label.pack_forget()
    chat_box.insert(tk.END, "Pasta processada. Agora você pode fazer perguntas.\n", "system")


# Criar interface gráfica
# Criar interface gráfica
root = ctk.CTk()
root.title("OCR-Rag-OllamaChat")
root.geometry("500x600")

frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

button_frame = ctk.CTkFrame(frame)
button_frame.pack(pady=5, fill=tk.X)

select_button = ctk.CTkButton(button_frame, text="Selecionar Imagem", command=select_image)
select_button.pack(side=tk.LEFT, padx=5)

folder_button = ctk.CTkButton(button_frame, text="Selecionar Pasta", command=select_folder)
folder_button.pack(side=tk.LEFT, padx=5)

loading_label = ctk.CTkLabel(frame, text="Processando...", fg_color="transparent")

chat_box = ctk.CTkTextbox(frame, wrap=tk.WORD, height=400, state=tk.NORMAL)
chat_box.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
chat_box.insert(tk.END, "Bem-vindo! Envie uma imagem e depois pergunte sobre ela.\n", "system")
chat_box.tag_config("system", foreground="gainsboro")
chat_box.tag_config("user", foreground="turquoise")
chat_box.tag_config("ollama", foreground="khaki1")

chat_input = ctk.CTkEntry(frame)
chat_input.pack(pady=5, padx=5, fill=tk.X)
chat_input.bind("<Return>", on_send_message)

send_button = ctk.CTkButton(frame, text="Enviar", command=on_send_message)
send_button.pack(pady=5)

root.mainloop()