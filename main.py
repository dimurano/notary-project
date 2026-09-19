import os
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Notary Core Service")

# Configuration loaded via GCP Environment Variables
ADOBE_ACCESS_TOKEN = os.getenv("ADOBE_ACCESS_TOKEN")
ADOBE_API_BASE_URL = os.getenv("ADOBE_API_BASE_URL", "https://adobesign.com")

headers = {
    "Authorization": f"Bearer {ADOBE_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

class NotarySessionRequest(BaseModel):
    client_email: EmailStr
    document_name: str

def upload_transient_document(file_content: bytes, filename: str) -> str:
    """Uploads a PDF to Adobe Sign temporarily to get a transientDocumentId."""
    url = f"{ADOBE_API_BASE_URL}/transientDocuments"
    upload_headers = {"Authorization": f"Bearer {ADOBE_ACCESS_TOKEN}"}
    files = [('File', (filename, file_content, 'application/pdf'))]
    
    response = requests.post(url, headers=upload_headers, files=files)
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail=f"Adobe upload failed: {response.text}")
    
    return response.json()["transientDocumentId"]

@app.post("/api/v1/notary/create-session")
async def create_notary_session(
    client_email: str = Form(...),
    document_name: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 1. Read uploaded file and send to Adobe Sign
        file_content = await file.read()
        transient_id = upload_transient_document(file_content, file.filename)
        
        # 2. Build the Agreement Payload
        agreement_payload = {
            "fileInfos": [{"transientDocumentId": transient_id}],
            "name": document_name,
            "participantSetsInfo": [
                {
                    "memberInfos": [{"email": client_email}],
                    "order": 1,
                    "role": "SIGNER"
                }
            ],
            "signatureType": "ESIGN",
            "state": "IN_PROCESS" # Immediately sends out the document for signing
        }
        
        # 3. Create the agreement in Adobe Sign
        agreement_url = f"{ADOBE_API_BASE_URL}/agreements"
        response = requests.post(agreement_url, json=agreement_payload, headers=headers)
        
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail=f"Agreement creation failed: {response.text}")
            
        return {
            "status": "success",
            "agreement_id": response.json()["id"],
            "message": "Document successfully processed and sent via Adobe Sign."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
