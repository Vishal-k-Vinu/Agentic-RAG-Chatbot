from ollama import chat
from retriever import search_document


model = "llama3.2:1b"


def search_med_document(query):
    result = search_document(query)
    return "\n\n".join(result)



def run_agent(question):

    resp = chat(
        model=model,
        messages=[
            {
                "role" : "system",
                "content" : """
                    You are a medical knowledge assistant.

                    You can answer questions using the medical knowledge
                    base.

                    If the question is related to a medical condition,
                    symptoms, treatment, or medication, you should use
                    the medical search tool.

                    If the question is not related to medicine, do not
                    use the tool.

                    Only answer questions related to the medical domain.
                    """
            },
            {
                "role" : "user",
                "content" : question
            }
        ],

        tools=[
            {
               "type": "function",
                "function": {
                    "name": "search_medical_documents",
                    "description": "Search the medical knowledge base for information about diseases, symptoms, treatments, and medications.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The medical question to search for"
                            } 
                        },
                    "required": ["query"]
                        }
                }
            }
        ]
    )

    if resp.message.tool_calls:

        print("Agent decided to use medical search tool")
        tool_calls = resp.message.tool_calls[0]
        argument = tool_calls.function.arguments
        query = argument.get("query", question)
        search_result = search_med_document(query)
        
        final_resp = chat(
            model=model,
            messages=[
                {
                     "role": "system",
                    "content": """
                        You are a medical knowledge assistant.

                        Answer the user's question using ONLY the
                        information returned by the medical search tool.

                        Do not invent medical information.

                        Give a clear and simple answer.

                        This information is educational and is not
                        a personalized medical diagnosis or prescription.
                        """
                },
                {
                    "role": "user",
                    "content": question
                },
                resp.message,
                {
                    "role": "tool",
                    "content": search_result
                }
            ]
        )
        return final_resp.message.content


    else:
        return "Sorry, I can only answer questions related to the medical knowledge base."

if __name__ == "__main__":

    question = "symptoms of common cold?"

    answer = run_agent(question)

    print("\nFinal Answer:")
    print(answer)