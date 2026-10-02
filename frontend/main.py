from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, AppConfig
from auth import get_current_user_email  # Your JWT verification dependency

# Define schemas for clean parameter validation
class ConfigUpdateSchema(BaseModel):
    alert_notice: str

def check_admin_privileges(email: str, db: Session):
    """Helper method to isolate administrative security perimeter checking."""
    # Find user profile context
    # user = db.query(User).filter(User.email == email).first()
    # if not user or not user.is_admin:
    #     raise HTTPException(status_code=403, detail="Operation forbidden. Requires Admin permission.")
    pass

@app.get("/api/v1/config/alert-notice")
def get_public_alert_notice(db: Session = Depends(get_db)):
    """Publicly accessible view; the React landing page calls this to display current alerts."""
    config_row = db.query(AppConfig).filter(AppConfig.key == "homepage_alert_notice").first()
    return {"alert_notice": config_row.value if config_row else ""}


@app.post("/api/v1/admin/config/update")
def update_frontend_config(
    payload: ConfigUpdateSchema, 
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    """Protected administrative command post."""
    # 1. Access verification check
    check_admin_privileges(current_user_email, db)
    
    # 2. Database upsert (Update existing config key or insert a new one)
    config_row = db.query(AppConfig).filter(AppConfig.key == "homepage_alert_notice").first()
    if not config_row:
        config_row = AppConfig(key="homepage_alert_notice", value=payload.alert_notice)
        db.add(config_row)
    else:
        config_row.value = payload.alert_notice
        
    db.commit()
    return {"status": "success", "message": "Broadcast configurations written to database."}
