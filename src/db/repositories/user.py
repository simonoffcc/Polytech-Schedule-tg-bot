"""User repository file."""

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from ..models import User
from .abstract import Repository


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
        institute_id: int | None = None,
        group_id: int | None = None,
        institute_abbr: str | None = None,
        group_name: str | None = None,
    ) -> None:
        """ Insert a new user into the database.

        :param user_id:
        :param user_name:
        :param institute_id:
        :param group_id:
        :param institute_abbr:
        :param group_name:
        :return:
        """
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                institute_id=institute_id,
                group_id=group_id,
                institute_abbr=institute_abbr,
                group_name=group_name,
            )
        )

    async def get_institute_abbr(self, user_id: int) -> str | None:
        """Get user institute by telegram id."""
        return await self.session.scalar(
            select(User.institute_abbr).where(User.user_id == user_id).limit(1)
        )

    async def user_exists(self, user_id: int) -> bool:
        """Check if a user with the given user_id exists in the database."""
        query = select(User.exists())(User.user_id == user_id)
        return await self.session.scalar(query)
