import os

from unstructured.ingest.connector.local import SimpleLocalConfig
from unstructured.ingest.connector.astra import (
    AstraWriteConfig,
    AstraAccessConfig,
    SimpleAstraConfig,
)

from unstructured.ingest.interfaces import (
    ChunkingConfig,
    EmbeddingConfig,
    PartitionConfig,
    ProcessorConfig,
    ReadConfig,
)

from unstructured.ingest.runner import LocalRunner
from unstructured.ingest.runner.writers.base_writer import Writer
from unstructured.ingest.runner.writers.astra import (
    AstraWriter,
)

from unstructured_client.models import operations, shared

from dotenv import load_dotenv

load_dotenv()

def get_writer(api_endpoint, token) -> Writer:
    return AstraWriter(
        connector_config=SimpleAstraConfig(
           access_config=AstraAccessConfig(
               api_endpoint=api_endpoint,
               token=token,
           ),
           collection_name="unstructured",
           embedding_dimension=1536,
           requested_indexing_policy={"deny": ["metadata"]},
       ),
       write_config=AstraWriteConfig(batch_size=5),
    )


if __name__ == "__main__":
    writer = get_writer(
        api_endpoint=os.environ.get("ASTRA_DB_API_ENDPOINT"),
        token=os.environ.get("ASTRA_DB_APPLICATION_TOKEN"),
    )

    runner = LocalRunner(
        processor_config=ProcessorConfig(
            verbose=True,
            output_dir="./unstructured_output",
            num_processes=2,
        ),
        connector_config=SimpleLocalConfig(
            input_path='./temp.csv',
        ),
        read_config=ReadConfig(),
        partition_config=PartitionConfig(),
        chunking_config=ChunkingConfig(chunking_strategy=shared.ChunkingStrategy.BY_SIMILARITY),
        embedding_config=EmbeddingConfig(
            provider="langchain-openai",
            api_key=os.environ.get("OPENAI_API_KEY"),
        ),
        writer=writer,
    )

    runner.run()
