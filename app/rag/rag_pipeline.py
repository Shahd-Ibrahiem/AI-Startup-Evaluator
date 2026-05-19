from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever):

    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(
                retriever.invoke(x["query"])
            )
        )
    )

    return rag_chain