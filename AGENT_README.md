# Agente de Soporte de Programación

Agente especializado que apoya a usuarios en procesos de programación, integrado con **Azure AI Foundry**.

## 🎯 Características

- ✅ Soporte especializado en programación
- ✅ Generación de código
- ✅ Revisión de código
- ✅ Debugging y resolución de problemas
- ✅ Sugerencias de mejores prácticas
- ✅ Basado en modelo `gpt-4.1-mini`

## 🔗 Conexión con Azure Foundry

### Configuración

**Punto de Conexión Foundry:**
```
https://isiscarrillo235-6872-resource.services.ai.azure.com/api/projects/isiscarrillo235-6872
```

**Resource ID:**
```
/subscriptions/68d91b3d-2000-4df4-b23c-33bb950f8d58/resourceGroups/agentes-103/providers/Microsoft.CognitiveServices/accounts/isiscarrillo235-6872-resource/projects/isiscarrillo235-6872
```

**Modelo:** `gpt-4.1-mini`

### Archivos de Configuración

- **`agent.yaml`** - Configuración del agente
- **`.foundry/agent-metadata.yaml`** - Metadatos y ambiente (dev/prod)
- **`agent_client.py`** - Cliente Python para invocar el agente

## 📝 Instalación

### 1. Instalar dependencias

```bash
pip install azure-ai-projects azure-identity
```

### 2. Autenticación con Azure

```bash
az login
# o
azd auth login
```

### 3. Clonar/usar el repositorio

```bash
git clone https://github.com/isiscarrillo2357/TAREA-1---PAGINA-WEB-DE-LEONES.git
cd "TAREA-1---PAGINA-WEB-DE-LEONES"
```

## 🚀 Uso

### Invocar el agente (CLI)

```bash
python agent_client.py "¿Cómo puedo optimizar mi función Python?"
```

### Invocar desde Python

```python
from agent_client import invoke_agent

for response in invoke_agent("Ayúdame con este error de JavaScript"):
    print(response)
```

### Desde VS Code (Foundry Toolkit)

1. Abre el proyecto en VS Code
2. Instala la extensión **AI Toolkit for Azure AI Foundry**
3. En la paleta de comandos: `AI: Open Agent Panel`
4. Selecciona `programming-support-agent`
5. Comienza a chatear

## 📊 Estructura del Proyecto

```
.
├── agent.yaml                          # Configuración principal del agente
├── agent_client.py                     # Cliente Python
├── .foundry/
│   └── agent-metadata.yaml             # Metadatos de Foundry
├── index.html                          # (Proyecto web existente)
├── script.js
└── styles.css
```

## 🔄 Despliegue

Para desplegar cambios en Foundry:

```bash
# Con Azure Developer CLI
azd ai agent deploy

# O usando GitHub Actions (CI/CD automático)
```

Revisa `.github/workflows/` para la configuración de CI/CD.

## 📚 Recursos

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Hosted Agents Guide](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)
- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)

## 🤝 Soporte

Para problemas o preguntas sobre el agente:
1. Revisa los logs en Azure Portal
2. Usa `az logs` para debugging
3. Consulta la documentación de Foundry

---

**Versión:** 1.0.0  
**Estado:** ✅ Conectado con Azure Foundry  
**Última actualización:** 2026-06-16
