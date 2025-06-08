
# 🚀 INSTRUCCIONES DE DEPLOYMENT

## 1. Estructura de archivos:
```
mi-proyecto/
├── index.html          # Tu interfaz web
├── vercel.json         # Configuración de Vercel
├── requirements.txt    # Dependencias Python
├── .env               # Variables locales (no subir a Git)
└── api/
    └── generate-report.py  # Tu función serverless
```

## 2. Pasos para deployar:

### A. Preparar el proyecto:
```bash
# Crear directorio del proyecto
mkdir asistente-publicidad-uade
cd asistente-publicidad-uade

# Crear estructura
mkdir api
```

### B. Copiar archivos:
- Copia `index.html` (tu interfaz)
- Copia `vercel.json` 
- Copia `requirements.txt`
- Copia `api/generate-report.py`

### C. Configurar Git:
```bash
git init
git add .
git commit -m "Initial commit"
```

### D. Subir a GitHub:
```bash
# En GitHub, crea un nuevo repositorio
git remote add origin https://github.com/tu-usuario/asistente-publicidad-uade.git
git push -u origin main
```

## 3. Deploy en Vercel:

### A. Conectar repositorio:
1. Ve a https://vercel.com
2. Haz clic en "Add New Project"
3. Conecta tu repositorio de GitHub
4. Selecciona el repositorio `asistente-publicidad-uade`

### B. Configurar variables de entorno:
1. En el dashboard de Vercel → Settings → Environment Variables
2. Agrega: `GROQ_API_KEY` = `tu_api_key_real`
3. Marca "Production", "Preview", y "Development"

### C. Deploy:
1. Haz clic en "Deploy"
2. Espera a que termine el build
3. ¡Tu API estará en: `https://tu-proyecto.vercel.app/api/generate-report`!

## 4. Actualizar la interfaz web:

En tu `index.html`, cambia esta línea:
```javascript
// De esto:
endpoint: 'https://tu-api.vercel.app/generate-report',
useMock: true

// A esto:
endpoint: 'https://tu-proyecto-real.vercel.app/api/generate-report',
useMock: false
```

## 5. Testing local:

```bash
# Instalar Vercel CLI
npm i -g vercel

# Instalar dependencias
pip install -r requirements.txt

# Testear localmente
vercel dev

# Tu API local estará en: http://localhost:3000/api/generate-report
```

## 6. Activar GitHub Pages:

1. En tu repositorio → Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: "main" → / (root)
4. Save
5. Tu sitio estará en: `https://tu-usuario.github.io/asistente-publicidad-uade`

## 7. Troubleshooting:

### Si hay errores de build:
- Verifica que `requirements.txt` tenga las versiones correctas
- Revisa los logs en el dashboard de Vercel
- Asegúrate de que `GROQ_API_KEY` esté configurada

### Si hay errores de CORS:
- La función ya incluye headers CORS
- Verifica que el endpoint sea correcto

### Para debugging:
```python
# Agregar logs en generate-report.py
print(f"Contexto recibido: {contexto}")
print(f"Teoria recibida: {teoria}")
```

## 8. Urls finales:
- **Interfaz web:** `https://tu-usuario.github.io/asistente-publicidad-uade`
- **API backend:** `https://tu-proyecto.vercel.app/api/generate-report`
- **Dashboard Vercel:** `https://vercel.com/dashboard`