from typing import Generic, TypeVar, Type, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from utils import get_logger

ModelType = TypeVar("ModelType")
logger = get_logger(__name__)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize the repository with a SQLAlchemy model and database session.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class.
            db (Session): The SQLAlchemy session instance.
        """
        self.model = model
        self.db = db

    def get(self, obj_id: int) -> ModelType | None:
        """
        Retrieve a single object by its primary key.

        Args:
            obj_id (int): The primary key of the object.

        Returns:
            ModelType | None: The retrieved object or None if not found.
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self) -> List[ModelType]:
        """
        Retrieve all objects of the model type.

        Returns:
            list[ModelType]: List of all objects in the table.
        """
        return self.db.query(self.model).all()

    def create(self, obj: ModelType) -> ModelType:
        """
        Add a new object to the database.

        Args:
            obj (ModelType): The object to add.

        Returns:
            ModelType: The created object.
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def bulk_create(
        self, objects: List[ModelType], commit: bool = True
    ) -> List[ModelType]:
        """
        Efficiently insert multiple objects in a single transaction.

        Args:
            objects (List[ModelType]): List of objects to add.
            commit (bool): Whether to commit after adding.

        Returns:
            List[ModelType]: List of created objects.
        """
        if not objects:
            return []

        try:
            logger.info("Adding %s objects to session.", len(objects))
            self.db.add_all(objects)
            if commit:
                self.db.commit()
                for obj in objects:
                    self.db.refresh(obj)
            logger.info("Bulk creation successful.")
            return objects
        except SQLAlchemyError as e:
            logger.info("SQLAlchemyError occurred: %s", e)
            self.db.rollback()
            raise

    def update(
        self, obj_id: int, update_data: Dict[str, Any], commit: bool = True
    ) -> ModelType | None:
        """
        Partially update an existing record by ID.

        Args:
            obj_id (int): The primary key of the object to update.
            update_data (Dict[str, Any]): Dictionary of fields to update.
            commit (bool): Whether to commit after updating.

        Returns:
            ModelType | None: The updated object or None if not found.
        """
        obj = self.get(obj_id)
        if not obj:
            return None

        try:
            for field, value in update_data.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)

            if commit:
                self.db.commit()
                self.db.refresh(obj)

            return obj
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, obj_id: int) -> bool:
        """
        Delete an object by its primary key.

        Args:
            obj_id (int): The primary key of the object to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        obj = self.get(obj_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
