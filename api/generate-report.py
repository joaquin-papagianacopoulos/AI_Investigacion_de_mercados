# api/generate-report.py
from http.server import BaseHTTPRequestHandler
import json
import os
from crewai import Agent, Task, Crew, LLM

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Configurar CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Leer el body del request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extraer contexto y teoria
            contexto = data.get('contexto', '').strip()
            teoria = data.get('teoria', 'publicidad digital').strip()
            
            if not contexto:
                raise ValueError("El contexto no puede estar vacío")
            
            # Generar informe usando CrewAI
            informe = generar_informe_crewai(contexto, teoria)
            
            # Respuesta exitosa
            response = {
                'success': True,
                'informe': informe,
                'contexto': contexto,
                'teoria': teoria
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            # Manejo de errores
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'success': False,
                'error': str(e),
                'message': 'Error al generar el informe académico'
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Manejar preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def get_llm():
    """Inicializar el LLM de CrewAI"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY no encontrada en las variables de entorno")
    
    return LLM(
        model="groq/deepseek-r1-distill-llama-70b",
        api_key=api_key,
        temperature=0.3,
    )

def agentes(contexto, teoria):
    """Tu función original de CrewAI con correcciones"""
    llm = get_llm()
    
    teorico = Agent(
        role="Sos un experto en Investigacion de mercados acerca de la Publicidad",
        goal=f"Aprender los conceptos de la teoria de {teoria}",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    contextoAgente = Agent(
        role=f"Sos un experto en {contexto}",
        goal=f"Basandote en el {teoria} debes proporcionar una respuesta a la pregunta: {contexto}",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tareas
    tarea1 = Task(
        description="Devolver un informe completo para un trabajo universitario de Publicidad en la UADE Argentina, usando el vocabulario adecuado",
        expected_output=f"Un informe con el contenido del {contexto} basado en la teoria publicista de {teoria} usando el vocabulario academico adecuado y con una solucion integral",
        agent=teorico, 
    )
    
    tarea2 = Task(
        description=f"Hacer una revisión del informe basandose en los conocimientos del {contextoAgente}",
        expected_output=f"Una solución integral con un informe, pensado paso a paso, basado en la {teoria} usando como referencia el {contexto}",
        agent=contextoAgente,  
        context=[tarea1],
    )
    
    crew = Crew(
        agents=[teorico, contextoAgente],
        tasks=[tarea1, tarea2],
        verbose=True,
        process="sequential"  
    )
    
    return crew

def generar_informe_crewai(contexto, teoria):
    """Función principal que ejecuta CrewAI y devuelve el informe"""
    try:
        # Crear y ejecutar el crew
        crew = agentes(contexto, teoria)
        result = crew.kickoff()
        
        # Convertir el resultado a string si es necesario
        informe = str(result)
        
        # Agregar metadatos del informe
        informe_final = f"""# Informe Académico de Publicidad - UADE

**Contexto:** {contexto}
**Marco Teórico:** {teoria}
**Fecha de generación:** {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}

---

{informe}

---

*Informe generado mediante sistema multi-agente especializado en investigación publicitaria académica.*
"""
        
        return informe_final
        
    except Exception as e:
        raise Exception(f"Error en CrewAI: {str(e)}")

# Función adicional para testing local
if __name__ == "__main__":
    # Para testing local
    import sys
    if len(sys.argv) > 2:
        contexto = sys.argv[1]
        teoria = sys.argv[2] if len(sys.argv) > 2 else "publicidad digital"
        
        print(f"Testing con contexto: {contexto}, teoria: {teoria}")
        try:
            result = generar_informe_crewai(contexto, teoria)
            print("✅ Resultado:")
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Uso: python generate-report.py 'contexto' 'teoria'")
        print("Ejemplo: python generate-report.py 'marketing digital' 'comunicación integrada'")