from langchain_community.vectorstores import Qdrant
from langchain_together import Together
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
print("api key: ", TOGETHER_API_KEY, type(TOGETHER_API_KEY))


# load the embedding model
model_name = "BAAI/bge-large-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)
print("embeddings loaded.............")

url = "http://localhost:6333"
collection_name = "shopintel100v3"

client = QdrantClient(url=url, prefer_grpc=False)

vector_store = Qdrant(
    client=client, 
    collection_name=collection_name, 
    embeddings=embeddings
)

print("qdrant embeddings from docker were loaded.............")


llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.2,
    max_tokens=10000,
    top_k=50,
    together_api_key=TOGETHER_API_KEY
)


# query = "ASUS VivoBook 15 (2021)"
# result = vector_store.similarity_search_with_score(query=query, k=5)

# for i in result:
#     doc, score = i
#     print({"score": score, "content": doc.page_content, "metadata": doc.metadata["source"]})
#     print("---------------------------------")

# function to retrieve products from qdrant

def retrieve_product(user_input, vector_store, k = 25):
    result = vector_store.similarity_search_with_score(
      query=user_input,
      k=k
    )

    return result


# function to create context from user query

def create_context(user_input, vector_store):
    result = retrieve_product(user_input, vector_store)

    context = ""
    for index, value in enumerate(result):
        product = value
        product_title = product[0].page_content # Extracting the page_content for each result which is a string
        product_metadata = product[0].metadata["source"] # Extracting the metadata for each result which is a dictionary with key values

        context += f"""
        * Product {index + 1} -
          - Product name : {product_metadata["name"]}
          - Product price: {product_metadata["discount_price"]}
          - Brief description of the product: {product_metadata["product_desc"]}
          - Detailed description of the product: {product_metadata["about_this_item"]}
          - Rating value (1.0 - 5.0): {product_metadata["ratings"]}
          - Overall review: {product_metadata["overall_review"]}


        """
        # print(f"product_title: {type(product_title)}", product_title)
        # print(f"product_metadata: {type(product_metadata)}", product_metadata)

    return context



# prompt template for the mistral model

template = """You are a friendly, conversational AI ecommerce assistant. The context includes 5 ecommerce products.
Use only the following context, to find the answer to the questions from the customer.

Its very important that you follow the below instructions.
 -Dont use general knowledge to answer the question
 -If you dont find the answer from the context or the question is not related to the context, just say that you don't know the answer.
 -By any chance the customer should not know you are referring to a context. 


Context:

{context}


Question:
{question}


Helpful Answer:"""


import random
import gradio as gr

chat_history = []
def respond(message, chat_history):
    global  vector_store, template, llm
    chatbot_response = ""
    try:
        context = create_context(message, vector_store)
        print("context:-------------------------\n", context)
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        prompt_formatted_str = prompt.format(
            context=context,
            question=message
        )
        output = llm.invoke(prompt_formatted_str)
        chat_history.append((message, output))
        return "", chat_history
    except Exception as e:
        print("Error:", e)
        error_responses = [
            "Sorry, I encountered an error while processing your request.",
            "Oops, something went wrong. Please try again later.",
            "I'm having trouble understanding that. Can you please rephrase?",
            "It seems there was an issue. Let's try something else."
        ]
        error_message = random.choice(error_responses)
        output = error_message
        chat_history.append((message, output))
        return "", chat_history

# Define the Gradio interface
# chatbot = gr.Chatbot(height=450)
# msg = gr.Textbox(label="What would you like to know?")
# gr.Interface(
#     fn=respond,
#     inputs=msg,
#     outputs=gr.Textbox(label="Response"),
#     title="Conversational AI Chatbot",
# ).launch(
#     share=True,
# )

# # Define Gradio components
with gr.Blocks() as demo:
    chat_history = []
    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(label="What would you like to know?")
    btn = gr.Button("Submit")
    clear = gr.ClearButton(value="Clear Console", components=[msg, chatbot])

    # Button click event to respond to the message
    btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

    # Clear button event to clear the console
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

# Define the Gradio interface
gr.close_all()

demo.launch(share=True)