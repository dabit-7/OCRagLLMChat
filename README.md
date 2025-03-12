# OCR-RAG-OllamaChat

Este projeto é um chatbot baseado em OCR (Reconhecimento Óptico de Caracteres) e RAG (Retrieval-Augmented Generation), permitindo ao usuário carregar imagens contendo texto e interagir com um modelo de linguagem para fazer perguntas sobre o conteúdo extraído.

## 🚀 Funcionalidades
- **Reconhecimento de texto em imagens** usando EasyOCR
- **Armazenamento do texto extraído** em um banco de dados vetorial ChromaDB
- **Interação via chat** com o modelo de linguagem Ollama (Mistral)
- **Interface gráfica intuitiva** com CustomTkinter
- **Suporte a múltiplas imagens**: carregar imagens individuais ou processar uma pasta inteira
- **Execução assíncrona** com threading para melhor experiência do usuário

## 📦 Dependências
Certifique-se de instalar as bibliotecas necessárias antes de executar o projeto. Você pode instalar todas as dependências usando:

```sh
pip install -r requirements.txt
```

Caso precise listar os requisitos manualmente, o projeto utiliza as seguintes bibliotecas:
```sh
easyocr
customtkinter
tkinter
langchain_ollama
chromadb
ollama
threading
os
```

## 🔧 Como Usar
1. **Clone o repositório**
```sh
git clone https://github.com/seu-usuario/OCR-RAG-OllamaChat.git
cd OCR-RAG-OllamaChat
```

2. **Instale as dependências**
```sh
pip install -r requirements.txt
```

3. **Execute o programa**
```sh
python main.py
```

4. **Utilize a interface gráfica:**
   - Clique em **Selecionar Imagem** para escolher uma imagem
   - Ou clique em **Selecionar Pasta** para processar todas as imagens de uma pasta
   - Após o processamento, envie perguntas no chat para interagir com o conteúdo extraído
   - Digite "sair" para encerrar a conversa

## 🎨 Interface Gráfica
A interface conta com:
- Botões para selecionar imagens e pastas
- Indicador de carregamento durante o processamento das imagens
- Área de chat para interação com o modelo Ollama
- Entrada de texto com envio por **botão** ou tecla **Enter**

## 📷 Exemplos de Uso
### 🔹 Perguntas após processar uma imagem
> **Usuário**: O que está escrito na imagem?
>
> **Ollama**: O texto extraído é "Relatório de vendas - 2023".

### 🔹 Perguntas sobre várias imagens processadas
> **Usuário**: Há alguma menção a datas nas imagens?
>
> **Ollama**: Sim, encontrei a data "12/08/2023" em um dos documentos.

## 🛠️ Tecnologias Utilizadas
- **EasyOCR** para reconhecimento de texto em imagens
- **ChromaDB** para armazenamento e recuperação de contexto
- **Langchain + Ollama** para conversação com IA
- **CustomTkinter** para a interface gráfica

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usar, modificar e contribuir!

---
Feito com ❤️ por [David Martans](https://github.com/dabit-7)
