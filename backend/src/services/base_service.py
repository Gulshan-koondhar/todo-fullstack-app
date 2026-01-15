from sqlmodel import Session, select
from typing import TypeVar, Generic, List, Optional


# Generic type variable for models
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base service class providing common CRUD operations for all models.
    """
    def __init__(self, model: type):
        self.model = model

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        """
        Get a record by ID.
        """
        statement = select(self.model).where(self.model.id == id)
        return db.exec(statement).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get multiple records with pagination.
        """
        statement = select(self.model).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        """
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update an existing record.
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: str) -> ModelType:
        """
        Remove a record by ID.
        """
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj