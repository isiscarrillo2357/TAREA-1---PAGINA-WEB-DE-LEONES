#!/usr/bin/env python3
"""
Cliente para invocar el agente de soporte de programación en Azure Foundry
"""

import os
import json
from typing import Generator

# Configuración del agente
PROJECT_ENDPOINT = "https://isiscarrillo235-6872-resource.services.ai.azure.com/api/projects/isiscarrillo235-6872"
AGENT_NAME = "programming-support-agent"
DEPLOYMENT_NAME = "gpt-4.1-mini"

def get_agent_client():
    """Obtiene el cliente del agente desde Azure Foundry"""
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
        
        credential = DefaultAzureCredential()
        client = AIProjectClient.from_connection_string(
            credential=credential,
            conn_str=PROJECT_ENDPOINT
        )
        return client
    except ImportError:
        print("⚠️  Azure AI SDK no está instalado")
        print("Instala con: pip install azure-ai-projects azure-identity")
        return None

def invoke_agent(user_message: str) -> Generator[str, None, None]:
    """
    Invoca el agente con un mensaje del usuario
    
    Args:
        user_message: Mensaje del usuario
        
    Yields:
        Respuestas del agente
    """
    client = get_agent_client()
    if not client:
        yield "Error: No se pudo conectar con Azure Foundry"
        return
    
    try:
        # Crear sesión de conversación
        session = client.agents.create_session()
        print(f"✅ Sesión creada: {session.id}")
        
        # Enviar mensaje al agente
        print(f"\n📤 Usuario: {user_message}\n")
        response = client.agents.create_message(
            thread_id=session.id,
            agent_name=AGENT_NAME,
            message=user_message
        )
        
        # Procesar respuesta
        for event in response:
            if hasattr(event, 'message_content'):
                yield event.message_content
                
    except Exception as e:
        yield f"Error al invocar agente: {str(e)}"

def main():
    """Función principal - demostración"""
    import sys
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("🔹 ¿Cuál es tu pregunta sobre programación? ")
    
    print("\n" + "="*60)
    print("🤖 Agente de Soporte de Programación")
    print("="*60 + "\n")
    
    for response_chunk in invoke_agent(user_input):
        print(f"📥 Agente: {response_chunk}\n")

if __name__ == "__main__":
    main()
