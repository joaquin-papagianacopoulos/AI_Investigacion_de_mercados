# main.py - Servidor principal para Railway
from flask import Flask, request, jsonify, send_from_directory
import os
import json
from crewai import Agent, Task, Crew, LLM

app = Flask(__name__)

# Configurar CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Servir tu index.html
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('.', path)
    except:
        return send_from_directory('.', 'index.html')

# Función principal de CrewAI
def generate_academic_report(contexto, teoria):
    """Genera informe académico usando CrewAI"""
    
    try:
        # Configurar LLM con Groq
        llm = LLM(
            model="groq/llama3-8b-8192",
            api_key=os.environ.get("GROQ_API_KEY")
        )

        # Agente Investigador Académico
        investigador = Agent(
            role='Investigador Académico de Publicidad',
            goal=f'Realizar investigación profunda sobre {contexto} aplicando la teoría de {teoria}',
            backstory="""Eres un investigador académico especializado en publicidad y marketing 
            de la Universidad Argentina de la Empresa (UADE). Tienes vasta experiencia en 
            análisis teórico y aplicación práctica de conceptos publicitarios.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # Agente Redactor Académico
        redactor = Agent(
            role='Redactor Académico',
            goal='Crear informes académicos estructurados y profesionales',
            backstory="""Eres un redactor académico experto en crear informes universitarios 
            con metodología UADE. Tu especialidad es transformar investigación en documentos 
            académicos claros, estructurados y profesionales.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # Tarea de investigación
        tarea_investigacion = Task(
            description=f"""
            Realiza una investigación exhaustiva sobre: "{contexto}"
            
            Aplicando la teoría de: {teoria}
            
            Tu investigación debe incluir:
            1. Marco teórico detallado de {teoria}
            2. Análisis conceptual del contexto dado
            3. Aplicaciones prácticas
            4. Casos de estudio relevantes
            5. Tendencias actuales en el campo
            6. Implicaciones estratégicas
            
            Enfócate en proporcionar información académica sólida y actualizada.
            """,
            agent=investigador,
            expected_output="Investigación detallada con marco teórico, análisis y casos prácticos"
        )

        # Tarea de redacción
        tarea_redaccion = Task(
            description=f"""
            Crea un informe académico profesional basado en la investigación realizada.
            
            El informe debe seguir esta estructura:
            
            # Informe Académico: {contexto}
            
            ## Introducción
            - Presentación del tema
            - Objetivos del análisis
            - Metodología aplicada
            
            ## Marco Teórico
            - Fundamentos de {teoria}
            - Conceptos clave
            - Evolución histórica
            
            ## Análisis Detallado
            - Aplicación de la teoría al contexto
            - Casos de estudio
            - Análisis crítico
            
            ## Hallazgos y Resultados
            - Principales descubrimientos
            - Patrones identificados
            - Insights relevantes
            
            ## Implicaciones Estratégicas
            - Aplicaciones prácticas
            - Recomendaciones
            - Oportunidades futuras
            
            ## Conclusiones
            - Síntesis de hallazgos
            - Aportes al campo académico
            - Líneas de investigación futura
            
            ## Referencias y Bibliografía
            - Fuentes académicas relevantes
            
            Usa formato Markdown, estilo académico universitario, y asegúrate de que 
            el contenido sea apropiado para el nivel universitario de UADE.
            """,
            agent=redactor,
            expected_output="Informe académico completo en formato Markdown con estructura universitaria profesional"
        )

        # Crear y ejecutar el crew
        crew = Crew(
            agents=[investigador, redactor],
            tasks=[tarea_investigacion, tarea_redaccion],
            verbose=True
        )

        # Ejecutar el crew
        resultado = crew.kickoff()
        
        return str(resultado)

    except Exception as e:
        return f"""# Error en la Generación del Informe

Ocurrió un error al generar el informe académico:

**Error:** {str(e)}

## Posibles causas:
- Problema con la API key de Groq
- Límite de rate excedido
- Error en el procesamiento de CrewAI

## Solución:
Intenta reformular tu consulta o espera unos minutos antes de intentar nuevamente.

---
*Sistema de Informes Académicos UADE*
"""

# API endpoint
@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def api_generate_report():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No se recibieron datos"
            }), 400
        
        contexto = data.get('contexto', '').strip()
        teoria = data.get('teoria', '').strip()
        
        if not contexto or not teoria:
            return jsonify({
                "success": False,
                "error": "Contexto y teoría son requeridos"
            }), 400
        
        print(f"🚀 Generando informe: {contexto} | Teoría: {teoria}")
        
        # Generar informe con CrewAI
        informe = generate_academic_report(contexto, teoria)
        
        print("✅ Informe generado exitosamente")
        
        return jsonify({
            "success": True,
            "informe": informe
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error interno: {str(e)}"
        }), 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "UADE Academic Report Generator",
        "groq_configured": bool(os.environ.get("GROQ_API_KEY"))
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)