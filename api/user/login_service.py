from datetime import datetime
from typing import Any, Union

import jwt
from flask_jwt_extended import create_access_token, create_refresh_token

from core import config
from db import cache, db
from models import SuccessHistory, User


def generate_jwt_tokens(current_user: User, request=None) -> dict[str, str]:
    additional_claims: dict[str, list] = {
        "roles": [i.role.name for i in current_user.user_roles]
    }
    acc_token: str = create_access_token(
        identity=current_user.id, additional_claims=additional_claims
    )
    ref_token: str = create_refresh_token(
        identity=current_user.id, additional_claims=additional_claims
    )
    # put refresh token in REDIS
    jti: Union[str, Any] = jwt.decode(
        jwt=ref_token, key=config.JWT_SECRET_KEY, algorithms="HS256"
    ).get("jti")
    # add refresh token in black list
    cache.add_token(
        key=jti, expire=config.JWT_REFRESH_TOKEN_EXPIRES, value=current_user.id
    )
    if request:
        # save history
        user_agent: str = request.user_agent.string
        ip_address: str = request.remote_addr
        check_platform: str = request.user_agent.platform
        browser: str = request.user_agent.browser
        if check_platform and "windows" in check_platform.lower():
            platform: str = "windows"
        elif check_platform and "linux" in check_platform.lower():
            platform: str = "linux"
        else:
            platform: str = "other"
        history = SuccessHistory(
            user_id=current_user.id,
            description=f"устройство: {user_agent}\nдата входа: {datetime.now()}",
            ip_address=ip_address,
            user_agent=user_agent,
            platform=platform,
            browser=browser,
        )
        db.session.add(history)
        db.session.commit()
    return {"access_token": acc_token, "refresh_token": ref_token}
