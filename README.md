# CSV ML Playground

Proyecto minimal que incluye:
- Backend: FastAPI para subir CSV, entrenar modelos básicos y predecir.
- Frontend: React + Vite (simple) para subir CSV y ver una previsualización.
- Dockerfiles y docker-compose para ejecutar localmente.

## Cómo ejecutar localmente (con Docker)
1. Construir y levantar:
   ```bash
   docker-compose up --build
   ```
2. Frontend: http://localhost:3000
   Backend API: http://localhost:8000

## Notas
- Los archivos subidos y modelos se guardan en la carpeta `./data` dentro del proyecto (montada como volumen).
- El endpoint `/train` espera `job_name`, `file_id`, `target`, `model_type` y devuelve métricas y ruta del modelo.

