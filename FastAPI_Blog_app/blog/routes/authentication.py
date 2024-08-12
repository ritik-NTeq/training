# JWT - JSON Web Tokens
# It is a standard (or technique) to encode a JSON object into a long dense string without spaces.
# It is not encrypted. So anyone could recover info from it.
# But it is signed (digital signatures). So the user who emitted it, can verify when he receive the token.
# It comes with an expiration time. After which user has to sign in again.


from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, token
from ..models import User
from ..database import get_db
from ..hash import Hash


router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Username {request.username} doesn't exist!")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect credentials!")
    
    access_token = token.create_access_token(data={"sub":user.email})
    return {"access_token": access_token, "token_type": "bearer"}