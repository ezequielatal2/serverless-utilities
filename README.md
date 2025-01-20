# Azure DevOps Pipeline Trigger Webhook

This repository hosts an Azure Function written in Python that acts as a webhook to trigger pipelines in Azure DevOps. It processes incoming GitHub events, extracts necessary details, and triggers pipelines with custom parameters.

## Features

- **Webhook Listener:** Listens for incoming GitHub webhook events.
- **Branch-Specific Actions:** Processes the branch reference (`ref`) from the webhook payload.
- **Pipeline Triggering:** Sends requests to Azure DevOps to initiate pipeline runs.
- **Dynamic Parameters:** Passes `repository_name` and `environment` as pipeline parameters.
- **Secure Authentication:** Uses Azure DevOps PAT (Personal Access Token) for secure communication.

## Prerequisites

To use this project, ensure you have the following:

1. **Azure Account:** For deploying the Azure Function.
2. **Azure DevOps PAT:** A Personal Access Token with sufficient permissions to trigger pipelines.
3. **GitHub Webhook:** Configured in your GitHub repository to send events to the Azure Function.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```
### 2. Set Environment Variables

In your Azure Function app settings, configure the following environment variable:

- `AZURE_DEVOPS_PAT`: Your Azure DevOps Personal Access Token.

### 3. Deploy the Azure Function

Use the Azure Functions Core Tools or the Azure portal to deploy the function to your Azure environment.

```bash
func azure functionapp publish <YourFunctionAppName>
```
### 4. Configure GitHub Webhook

1. Go to your GitHub repository.
2. Navigate to **Settings > Webhooks > Add webhook**.
3. Set the payload URL to your Azure Function endpoint. The format should be:

```bash
https://<YourFunctionAppName>.azurewebsites.net/api/<FunctionName>
```
4. Choose the events to trigger the webhook (e.g., push events).

### 5. Trigger a Pipeline

Once configured, the Azure Function will process GitHub webhook payloads and trigger the specified Azure DevOps pipeline.

### How It Works

1. **Payload Processing:**
   - The function extracts the `ref` (branch) and `repository` details from the incoming GitHub webhook payload.

2. **Pipeline Triggering:**
   - Constructs a POST request to Azure DevOps with the required parameters, including `repository_name` and `environment`.

3. **Error Handling:**
   - Logs errors and returns appropriate HTTP responses for troubleshooting.

### Code Highlights

1. **Environment Variables:**
   - Securely fetches the PAT from the environment to ensure sensitive information is not hardcoded.

2. **Payload Parsing:**
   - Handles and processes JSON payloads received from GitHub webhooks.

3. **Error Handling:**
   - Implements robust error logging and responses to assist with debugging and troubleshooting.

```bash
# Example snippet from the function
if not azure_devops_pat:
    logging.error("Token de autorización no encontrado en las variables de entorno.")
    return func.HttpResponse(
        "Error: Token de autorización no configurado.",
        status_code=500
    )
```

### Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository, make your changes, and submit a pull request for review.

### License

This project is licensed under the [MIT License](LICENSE).
