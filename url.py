from langchain_community.document_loaders import UnstructuredURLLoader

loaders = UnstructuredURLLoader(urls=["https://www.themoviedb.org/movie/62"], show_progress_bar=True)
docs = loaders.load()
print(docs)