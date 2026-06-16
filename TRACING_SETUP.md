# 📊 Tracing Distribuido - Agente de Programación

Visualiza en tiempo real las traces de tu agente usando **OpenTelemetry** y **Jaeger**.

## 🚀 Inicio Rápido

### Paso 1: Levanta el stack OTLP + Jaeger

```bash
docker-compose up -d
```

Esto inicia:
- **OpenTelemetry Collector** en puerto 4319 (gRPC)
- **Jaeger UI** en `http://localhost:16686`

### Paso 2: Instala dependencias de tracing

```bash
pip install \
  opentelemetry-api \
  opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation \
  opentelemetry-instrumentation-requests \
  opentelemetry-instrumentation-urllib3 \
  opentelemetry-instrumentation-azure
```

### Paso 3: Ejecuta el agente con tracing

```bash
python agent_client_traced.py "¿Cómo optimizo mi función?"
```

### Paso 4: Visualiza en Jaeger

Abre: **http://localhost:16686**

- Busca por servicio: `agent_client_traced`
- Filtra por operación: `invoke_agent`
- Explora los spans (trazas detalladas)

---

## 📈 Qué Se Traza

El cliente captura automáticamente:

### Spans Principales
- `invoke_agent` - Invocación completa
- `create_session` - Creación de sesión
- `send_message` - Envío de mensaje
- `process_response` - Procesamiento de respuesta

### Atributos Capturados
- `agent.name` - Nombre del agente
- `user.message` - Mensaje del usuario
- `model` - Modelo usado
- `session.id` - ID de sesión
- `message.length` - Longitud del mensaje
- `response.length` - Longitud de respuesta
- `error.type` - Tipo de error (si aplica)
- `timestamp` - Marca de tiempo

---

## 🔍 Estructura de Traces

```
invoke_agent
├── create_session
│   └── session.id: "abc123"
├── send_message
│   ├── message.length: 45
│   └── response.received: true
└── process_response
    ├── response.length: 320
    └── response.complete: true
```

---

## 🛠️ Troubleshooting

### Jaeger no recibe datos
1. Verifica que Docker está corriendo: `docker ps`
2. Comprueba logs del collector: `docker logs otel-collector`
3. Asegúrate que el endpoint es correcto: `http://localhost:4319`

### Puertos ocupados
```bash
# Libera el puerto 16686 (Jaeger UI)
lsof -i :16686 | awk 'NR!=1 {print $2}' | xargs kill -9
```

### Ver logs del collector
```bash
docker logs -f otel-collector
```

---

## 📚 Referencia de Archivos

- **`agent_client_traced.py`** - Cliente con tracing integrado
- **`docker-compose.yml`** - Stack OTLP + Jaeger
- **`otel-collector-config.yml`** - Configuración del colector

---

## 🔗 Recursos

- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Azure AI SDK Tracing](https://learn.microsoft.com/azure/ai-foundry/)

---

**Última actualización:** 2026-06-16
