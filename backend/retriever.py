import chromadb
from pathlib import Path


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="medical_documents")

def load_document():
    
    file_path = Path(__file__).parent / "document" / "medical_knowledge_base.txt"
    with open(file_path , "r" , encoding="utf-8") as f:
        return f.read() 


def split_document(text):

    sections = text.split("\n\n")
    chunks=[]
    current_chunk = ""

    for section in sections:

        if section.strip() == "":
            continue
        if section[0].isdigit() and "." in section :
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = section
        else:
            current_chunk += "\n\n" + section

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks



def add_document():

    text = load_document()
    chunks = split_document(text)
    print(f"Number of chunks : {len(chunks)}")
    ids = []

    for i in range (len(chunks)):
        ids.append(f"med-{i}")

    collection.add(
        ids=ids,
        documents=chunks
    )
    print("Medical document added to db")



def search_document (query , n_results = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]
