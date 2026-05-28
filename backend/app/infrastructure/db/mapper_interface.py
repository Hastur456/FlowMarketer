from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


DomainType = TypeVar("DomainType")
ModelType = TypeVar("ModelType")


class MapperInterface(ABC, Generic[DomainType, ModelType]):
    @staticmethod
    @abstractmethod
    def to_domain(model: ModelType) -> DomainType:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_model(domain: DomainType) -> ModelType:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_model(
        model: ModelType,
        updates: DomainType | dict[str, Any],
    ) -> ModelType:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_persistence_dict(
        domain: DomainType,
    ) -> dict[str, Any]:
        raise NotImplementedError
