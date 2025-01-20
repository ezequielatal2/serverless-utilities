import os
import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GitHub Webhook Triggered...")

    try:
        payload = req.get_json()
        logging.info(f"Payload recibido: {payload}")

        # Extraer datos del payload de GitHub
        ref = payload.get("ref", "refs/heads/main")
        repository = payload.get("repository", {}).get("full_name", "")
        
        # Procesar los valores personalizados
        repository_name = repository.split("/")[-1]
        environment = ref.replace("refs/heads/", "")  # Limpiar el prefijo para obtener solo el nombre de la rama
        
        # Obtener el pipelineId de la query string de la URL
        pipeline_id = req.params.get("pipelineId", "93")  # Valor por defecto si no se proporciona

        # Obtener el token de autorización desde una variable de entorno
        azure_devops_pat = os.getenv("AZURE_DEVOPS_PAT")
        if not azure_devops_pat:
            logging.error("Token de autorización no encontrado en las variables de entorno.")
            return func.HttpResponse(
                "Error: Token de autorización no configurado.",
                status_code=500
            )

        # Configurar la llamada a Azure DevOps
        azure_devops_url = (
            f"https://dev.azure.com/AL2DevOps/AL2%20microservicios/_apis/pipelines/{pipeline_id}/runs?api-version=6.0-preview.1"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {azure_devops_pat}"
        }

        # Construir el cuerpo de la solicitud con parámetros personalizados
        data = {
            "resources": {
                "repositories": {
                    "self": {
                        "refName": 'main'
                    }
                }
            },
            "templateParameters": {
                "repository_name": repository_name,
                "environment": environment  # Parámetro adicional
            }
        }

        # Enviar solicitud a Azure DevOps
        response = requests.post(azure_devops_url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            logging.info("Pipeline triggered successfully!")
            return func.HttpResponse("Pipeline triggered successfully!", status_code=200)
        else:
            logging.error(f"Error triggering pipeline: {response.text}")
            return func.HttpResponse(f"Error triggering pipeline: {response.text}", status_code=400)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error processing payload: {str(e)}", status_code=500)
