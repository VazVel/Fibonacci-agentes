import autogen
import os
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "llama-3.1-8b-instant",  # cámbialo al modelo de Groq que quieras
        "api_key": os.environ.get("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }
]

# 1. Agente Asistente: El "Cerebro" que escribe el código.
# Su system_message es clave: le instruimos a usar Python para resolver problemas.
calculador_senior = autogen.AssistantAgent(
    name="Calculador_Senior",
    llm_config={"config_list": config_list},
    system_message="""
    Eres un programador Python senior. Tu tarea es resolver problemas matemáticos escribiendo código Python.
    No des la respuesta directamente. En su lugar, escribe el código necesario para calcular la respuesta.
    Asegúrate de que tu código incluya una sentencia `print()` con el resultado final.
    """
)

# 2. Agente Proxy: Las "Manos" que ejecutan el código.
# ¡Aquí está la configuración clave! Habilitamos la ejecución de código.
ejecutor_de_codigo = autogen.UserProxyAgent(
    name="Ejecutor_de_Codigo",
    human_input_mode="NEVER",
    # Esta es la configuración que le permite ejecutar código.
    code_execution_config={
        "work_dir": "coding",  # Directorio donde guardará y ejecutará los scripts. Se creará si no existe.
        "use_docker": False,   # Le decimos que no use Docker para simplificar la configuración.
    },
)

# 3. Inicio de la Conversación con el Problema
print("▶️  Iniciando la tarea de cálculo de números primos...")

ejecutor_de_codigo.initiate_chat(
    calculador_senior,
    message="Genera los primeros 10 números de la secuencia de Fibonacci. Luego, guarda estos números en un archivo de texto llamado fibonacci.txt, con cada número en una nueva línea."
)