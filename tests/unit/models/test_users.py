import pytest

from project.models import Users
from sqlalchemy.exc import IntegrityError

from tests.helpers import generate_user, create_user


def test_can_create_new_users(inc, ut_reset_before):
    create_user(
        [
            generate_user(inc, confirm_field=False),
            generate_user(inc, confirm_field=False),
        ]
    )


def test_user_must_be_unique(inc, ut_reset_before):
    user = generate_user(inc, confirm_field=False)
    create_user(user)
    assert Users.query.filter_by(email=user["email"]).first() is not None
    with pytest.raises(IntegrityError):
        create_user(user)
