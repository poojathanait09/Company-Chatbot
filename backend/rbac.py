from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from auth import verify_token

security = HTTPBearer()

def get_current_user(token=Depends(security)):
    try:
        payload = verify_token(token.credentials)
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(allowed_roles):
    normalized_roles = [r.lower() for r in allowed_roles]

    def role_checker(user=Depends(get_current_user)):
        user_role = (user.get("role") or "").lower().strip()

        if user_role not in normalized_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker
