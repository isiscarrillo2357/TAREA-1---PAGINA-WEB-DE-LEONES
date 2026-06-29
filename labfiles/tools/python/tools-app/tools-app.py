import os
from dotenv import load_dotenv
import glob

# Import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        script_dir = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(os.path.join(script_dir, ".env"))
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        model_deployment = os.getenv("MODEL_DEPLOYMENT", "gpt-4.1")

        if not azure_openai_endpoint:
            raise ValueError("Falta AZURE_OPENAI_ENDPOINT en el archivo .env")

        # Initialize the OpenAI client
        # If AZURE_OPENAI_KEY is provided in the .env file, use it; otherwise use DefaultAzureCredential
        azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
        if azure_openai_key:
            openai_client = OpenAI(
                base_url=azure_openai_endpoint,
                api_key=azure_openai_key
            )
        else:
            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(), "https://ai.azure.com/.default"
            )

            openai_client = OpenAI(
                base_url=azure_openai_endpoint,
                api_key=token_provider
            )

        # Create vector store and upload files
        print("Creating vector store and uploading files...")
        vector_store = openai_client.vector_stores.create(
            name="travel-brochures"
        )

        brochures_dir = os.path.join(script_dir, "brochures")
        file_paths = glob.glob(os.path.join(brochures_dir, "*.pdf"))
        if not file_paths:
            print(f"No PDF files found in the brochures folder: {brochures_dir}")
            return

        file_streams = [open(path, "rb") for path in file_paths]

        file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )

        for f in file_streams:
            f.close()

        print(f"Vector store created with {file_batch.file_counts.completed} files.")

        # Track conversation state
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a question (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a question.")
                continue

            # Get a response using tools
            response = openai_client.responses.create(
                model=model_deployment,
                instructions="""
                Eres un asistente útil y preciso para temas de Azure, IA y Microsoft Learn.
                Prioriza Microsoft Learn y la documentación oficial de Microsoft cuando sea posible.
                Usa los archivos cargados como fuente de conocimiento local y consulta la web para información actualizada o complementaria.
                Responde en español y, cuando sea relevante, menciona la fuente o el recurso consultado.
                """,
                input=input_text,
                previous_response_id=last_response_id,
                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id]
                    },
                    {
                        "type": "web_search"
                    }
                ]
            )

            print(response.output_text)
            last_response_id = response.id

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
