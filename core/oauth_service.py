from models import SocialAccount, User, UserRole


def register_social_account(
    social_name: str, social_id: str, email: str, username: str
) -> dict:
    print(social_name, social_id, email, username)

    return {
        "message": f"Logged in as {current_user.username}",
        "access_token": acc_token,
        "refresh_token": ref_token,
    }, http.HTTPStatus.OK
