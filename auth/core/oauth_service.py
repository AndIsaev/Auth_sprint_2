import http

from api.user.login_service import generate_jwt_tokens
from api.user.registration_service import create_new_user
from models import SocialAccount, User


def register_social_account(
    social_name: str,
    social_id: str,
    email: str,
    username: str,
    request: "Request" = None,
) -> tuple[dict[str, str], int]:
    # search user in db by email
    current_user = User.find_by_email(email=email)
    # by username
    if not current_user:
        current_user = User.find_by_username(username=username)
    # if user not, create them
    if not current_user:
        current_user = create_new_user(
            username=username, email=email, password="Qwerty123"
        )
    # write social account in db
    if not SocialAccount.raw_exists(
        user_id=current_user.id, social_id=social_id, social_name=social_name
    ):
        SocialAccount(
            user_id=current_user.id, social_id=social_id, social_name=social_name
        ).save_to_db()
    # get jwt tokens for user
    jwt_tokens: dict[str, str] = generate_jwt_tokens(
        current_user=current_user, request=request
    )
    return {
        "message": f"Logged in as {current_user.username} - {current_user.email}",
        "access_token": jwt_tokens.get("access_token"),
        "refresh_token": jwt_tokens.get("refresh_token"),
    }, http.HTTPStatus.OK
