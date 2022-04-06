import pytest

from project.models import Users
from sqlalchemy.exc import IntegrityError

from tests.helpers.unit import create_user
from tests.helpers.all import generate_user, make_id
from tests.helpers.all import run_parallel


@pytest.mark.asyncio
async def test_can_create_new_users(fp, ut_reset_before, event_loop):
    ids = [make_id(fp=fp) for _ in range(2)]
    for _id in ids:
        create_user(generate_user(_id, confirm_field=False))


@pytest.mark.asyncio
async def test_user_must_be_unique(fp, ut_reset_before, event_loop):
    _id = make_id(fp=fp)
    user = generate_user(_id, confirm_field=False)
    create_user(user)
    assert Users.query.filter_by(email=user["email"]).first() is not None
    with pytest.raises(IntegrityError):
        create_user(user)
