from sqlalchemy.orm import Session
from app.models.audit import AuditLog


def create_audit_log(db: Session, user_id: int, action: str):
    log = AuditLog(
        user_id=user_id,
        action=action
    )

    db.add(log)
    db.commit()
