from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate


class RAGHandler:
    def __init__(self):
        self.llm = Ollama(
            model="llama3.2:3b",
            temperature=0.7,
            top_k=10,
            top_p=0.9,
            repeat_penalty=1.1
        )

        self.embeddings = OllamaEmbeddings(
            model="llama3.2:3b"
        )
        self.vector_store = None

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        self.qa_template = """Tu es un assistant virtuel pour l'École d'Ingénieurs EIGSI, spécialisé dans les événements organisés par l'école. Ton rôle est d'aider les utilisateurs à trouver des informations précises et contextualisées sur ces événements.

                Contexte sur les événements :
                {context}

                Question de l'utilisateur : {question}

                Historique de la conversation :
                {chat_history}

                Instructions :
                - Réponds uniquement avec les informations fournies dans le contexte et évite de mentionner des sources externes comme des sites ou des réseaux sociaux.
                - Donne la date, le lieu et les informations spécifiques à l’événement sans reformuler des détails déjà donnés.
                - N'utilise pas de formule de politesse comme "Bonjour" ou "Je suis ravi de vous aider" dans les réponses, à moins que l'utilisateur ne commence la conversation.
                - Utilise un ton amical, précis, et professionnel. Reste concis et évite de répéter les informations identiques.
                - Si l'information demandée n'est pas dans le contexte, indique simplement que tu n'as pas cette information.

                Réponse :"""

        self.qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "question", "chat_history"]
        )

    def create_vector_store(self, events):
        documents = []
        for event in events:
            content = f"Titre: {event.title}\nDescription: {event.description}\n"
            content += f"Date: {event.date}\nLieu: {event.location}\n"
            documents.append(content)

        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator="\n"
        )
        split_docs = text_splitter.create_documents(documents)

        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory="db"
        )

    def get_response(self, query, chat_history=None):
        if chat_history is None:
            chat_history = []

        if self.vector_store is None:
            return "Je ne peux pas répondre pour le moment."

        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={'prompt': self.qa_prompt},
            verbose=True
        )

        try:
            response = chain({"question": query, "chat_history": chat_history})
            return response['answer']
        except Exception as e:
            print(e)
            return f"Désolé, je ne peux pas répondre pour le moment."