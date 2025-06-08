from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import json

# Importar tu función de CrewAI desde api/generate-report.py
sys.path.append('api')

app = Flask(__name__)

# CORS
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

# Servir archivos estáticos (CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('.', path)
    except:
        return send_from_directory('.', 'index.html')  # Fallback al index

# API endpoint para CrewAI
@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def api_generate_report():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        contexto = data.get('contexto', '')
        teoria = data.get('teoria', '')
        
        # Aquí llamarás a tu función de CrewAI
        # Por ahora, importemos desde tu archivo existente
        from generate_report import handler_logic
        
        informe = handler_logic(contexto, teoria)
        
        return jsonify({
            "success": True,
            "informe": informe
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

# Para Gunicorn
app.debug = False