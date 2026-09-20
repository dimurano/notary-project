import os
import logging
from fastapi import FastAPI, Request, Response, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Assuming your SQLAlchemy models and engine are configured
# from database import get_db, NotarySession, SessionStatus

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# Load your Adobe Application Client ID from Environment Variables
ADOBE_CLIENT_ID = os.getenv("ADOBE_CLIENT_ID")

@app.get("/api/v1/adobe-webhook")
async def validate_adobe_webhook(
    request: Request, 
    x_adobesign_clientid: str = Header(None, alias="X-AdobeSign-ClientId")
):
    """
    Step 1: Webhook Registration Verification
    Adobe verifies ownership of this URL by checking if your app returns the client ID.
    """
    if not x_adobesign_clientid:
        raise HTTPException(status_code=400, detail="Missing X-AdobeSign-ClientId header")
        
    # Security Check: Match against your configured Client ID
    if x_adobesign_clientid != ADOBE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Unauthorized Client ID")

    # Respond with the client ID back in the headers as required by Adobe
    response_headers = {"X-AdobeSign-ClientId": x_adobesign_clientid}
    return Response(status_code=200, headers=response_headers)


@app.post("/api/v1/adobe-webhook")
async def handle_adobe_webhook_events(request: Request):
    """
    Step 2: Processing Live Webhook Events (AGREEMENT_WORKFLOW_COMPLETED)
    """
    # 1. Verify header to ensure integrity
    client_id = request.headers.get("X-AdobeSign-ClientId")
    if client_id != ADOBE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Unauthorized webhook payload source")

    payload = await request.json()
    event_type = payload.get("event")
    
    # 2. Filter for completed agreements
    if event_type == "AGREEMENT_WORKFLOW_COMPLETED":
        agreement_id = payload.get("agreement", {}).get("id")
        logger.info(f"Received completed agreement webhook for ID: {agreement_id}")
        
        # Open your PostgreSQL Session to update tracking state
        # db: Session = next(get_db())
        # session_record = db.query(NotarySession).filter(NotarySession.adobe_agreement_id == agreement_id).first()
        
        # if session_record:
        #     session_record.status = SessionStatus.SIGNED
        #     db.commit()
        #     
        #     # Trigger Background Task here: 
        #     # 1. Download finalized PDF from Adobe API 
        #     # 2. Write file streaming array into Google Cloud Storage
            
    return Response(status_code=200)
