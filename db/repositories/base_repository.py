from typing import Generic, TypeVar, Type, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, obj_id: int) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).all()

    def create(self, obj: ModelType) -> ModelType:
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
        """
        if not objects:
            return []

        try:
            self.db.add_all(objects)
            if commit:
                self.db.commit()
                for obj in objects:
                    self.db.refresh(obj)
            return objects
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(
        self, obj_id: int, update_data: Dict[str, Any], commit: bool = True
    ) -> ModelType | None:
        """
        Partially update an existing record by ID.
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
        obj = self.get(obj_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
