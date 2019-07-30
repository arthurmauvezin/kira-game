from fastapi import Depends, APIRouter
from pydantic.types import EmailStr

from api.utils.security import get_current_active_superuser
from models.msg import Msg
from models.user import UserInDB
from utils import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr, current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
