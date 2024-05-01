from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        """
        Define the table name for the SQLAlchemy model.
        :return: A string representing the table name.
        :rtype: str
        """
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession):
        """
        Save the current object to the database.

        Args:
            db_session (AsyncSession): The asynchronous database session to use for the save operation.

        Returns:
            None: If the save operation is successful.

        Raises:
            HTTPException: If there is an error during the save operation. The exception will have a status code of 422 and the detail will be the representation of the SQLAlchemyError.

        """
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def delete(self, db_session: AsyncSession):
        """
        Delete the current object from the database.

        :param db_session: The async session to use for the deletion.
        :type db_session: AsyncSession
        :raises HTTPException: If there is an error during the deletion.
        :return: None
        """
        try:
            db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex
