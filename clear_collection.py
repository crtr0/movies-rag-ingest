import os
from astrapy import DataAPIClient
from dotenv import load_dotenv

load_dotenv()

client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
collection = database.get_collection("movies")

result = collection.delete_all()