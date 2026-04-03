from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_role
from app.models.audit import AuditLog

router = APIRouter()

# get all audit logs -- only admin can access


@router.get("/logs")
def get_logs(db: Session = Depends(get_db),
             current_user=Depends(require_role(["admin"]))):
    return db.query(AuditLog).all()
