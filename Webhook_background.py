import httpx
from fastapi import BackgroundTasks
from google.cloud import storage

# Configure your storage bucket environment variables
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def download_and_upload_to_gcs(agreement_id: str, document_name: str):
    """Downloads the combined signed PDF from Adobe and pushes it directly to GCS."""
    adobe_url = f"{ADOBE_API_BASE_URL}/agreements/{agreement_id}/combinedDocument"
    adobe_headers = {"Authorization": f"Bearer {ADOBE_ACCESS_TOKEN}"}
    
    # 1. Fetch file byte stream from Adobe Sign
    with httpx.Client() as client:
        response = client.get(adobe_url, headers=adobe_headers)
        if response.status_code != 200:
            logger.error(f"Failed to fetch completed PDF from Adobe: {response.text}")
            return

    # 2. Initialize GCS Client and select your destination folder paths
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    
    # Clean up filename and set an archive destination string
    safe_filename = "".join([c if c.isalnum() else "_" for c in document_name])
    gcs_blob_path = f"finalized_contracts/{agreement_id}_{safe_filename}.pdf"
    
    # 3. Stream data straight into the secure bucket
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_string(response.content, content_type="application/pdf")
    logger.info(f"Successfully archived completed notary doc to GCS: {gcs_blob_path}")

    # 4. Update your database entry status
    # db: Session = next(get_db())
    # session_record = db.query(NotarySession).filter(NotarySession.adobe_agreement_id == agreement_id).first()
    # if session_record:
    #     session_record.gcs_signed_file_path = gcs_blob_path
    #     session_record.status = SessionStatus.COMPLETED
    #     db.commit()


@app.post("/api/v1/adobe-webhook")
async def handle_adobe_webhook_events(request: Request, background_tasks: BackgroundTasks):
    client_id = request.headers.get("X-AdobeSign-ClientId")
    if client_id != ADOBE_CLIENT_ID:
         raise HTTPException(status_code=401)

    payload = await request.json()
    if payload.get("event") == "AGREEMENT_WORKFLOW_COMPLETED":
        agreement_id = payload.get("agreement", {}).get("id")
        doc_name = payload.get("agreement", {}).get("name", "signed_document")
        
        # Dispatch file processing to a background thread so the webhook returns 200 immediately
        background_tasks.add_task(download_and_upload_to_gcs, agreement_id, doc_name)
            
    return Response(status_code=200)
