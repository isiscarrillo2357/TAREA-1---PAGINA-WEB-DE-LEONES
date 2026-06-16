#!/usr/bin/env python3
"""
Cliente para invocar el agente con OpenTelemetry Tracing
"""

import os
import json
from typing import Generator
from datetime import datetime

# Importar OpenTelemetry
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

# Configuración del agente
PROJECT_ENDPOINT = "https://isiscarrillo235-6872-resource.services.ai.azure.com/api/projects/isiscarrillo235-6872"
AGENT_NAME = "programming-support-agent"
DEPLOYMENT_NAME = "gpt-4.1-mini"
OTLP_ENDPOINT = "http://localhost:4319"

def setup_tracing():
    """Configura OpenTelemetry para tracing distribuido"""
    print(f"📊 Configurando tracing en {OTLP_ENDPOINT}...")
    
    # Crear exportador OTLP para traces
    otlp_exporter = OTLPSpanExporter(
        endpoint=OTLP_ENDPOINT,
        insecure=True
    )
    
    # Crear proveedor de traces
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(tracer_provider)
    
    # Instrumentar librerías HTTP
    RequestsInstrumentor().instrument()
    URLLib3Instrumentor().instrument()
    
    # Crear proveedor de métricas
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    )
    meter_provider = MeterProvider(metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    print("✅ Tracing configurado correctamente")
    return tracer_provider

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

def invoke_agent_with_tracing(user_message: str, tracer) -> Generator[str, None, None]:
    """
    Invoca el agente con un mensaje y tracing
    
    Args:
        user_message: Mensaje del usuario
        tracer: Tracer de OpenTelemetry
        
    Yields:
        Respuestas del agente
    """
    client = get_agent_client()
    if not client:
        yield "Error: No se pudo conectar con Azure Foundry"
        return
    
    with tracer.start_as_current_span("invoke_agent") as main_span:
        main_span.set_attribute("agent.name", AGENT_NAME)
        main_span.set_attribute("user.message", user_message)
        main_span.set_attribute("model", DEPLOYMENT_NAME)
        main_span.set_attribute("timestamp", datetime.utcnow().isoformat())
        
        try:
            with tracer.start_as_current_span("create_session") as session_span:
                session = client.agents.create_session()
                session_span.set_attribute("session.id", session.id)
                print(f"✅ Sesión creada: {session.id}")
            
            with tracer.start_as_current_span("send_message") as msg_span:
                msg_span.set_attribute("message.length", len(user_message))
                print(f"\n📤 Usuario: {user_message}\n")
                
                response = client.agents.create_message(
                    thread_id=session.id,
                    agent_name=AGENT_NAME,
                    message=user_message
                )
                msg_span.set_attribute("response.received", True)
            
            with tracer.start_as_current_span("process_response") as resp_span:
                resp_span.set_attribute("agent.processing", True)
                
                response_text = ""
                for event in response:
                    if hasattr(event, 'message_content'):
                        response_text += event.message_content
                        yield event.message_content
                
                resp_span.set_attribute("response.length", len(response_text))
                resp_span.set_attribute("response.complete", True)
                    
        except Exception as e:
            main_span.set_attribute("error", True)
            main_span.set_attribute("error.message", str(e))
            main_span.set_attribute("error.type", type(e).__name__)
            yield f"Error al invocar agente: {str(e)}"

def main():
    """Función principal con tracing"""
    import sys
    
    tracer_provider = setup_tracing()
    tracer = tracer_provider.get_tracer(__name__)
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("🔹 ¿Cuál es tu pregunta sobre programación? ")
    
    print("\n" + "="*60)
    print("🤖 Agente de Soporte de Programación (con Tracing)")
    print(f"📊 OTLP Endpoint: {OTLP_ENDPOINT}")
    print("="*60 + "\n")
    
    for response_chunk in invoke_agent_with_tracing(user_input, tracer):
        print(f"📥 Agente: {response_chunk}\n")
    
    print("\n✅ Consulta completada. Las traces se envían a:")
    print(f"   {OTLP_ENDPOINT}")

if __name__ == "__main__":
    main()
