from dataclasses import dataclass, field
from dataclasses import asdict
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean,UniqueConstraint
import db
from sqlalchemy.orm import relationship
from typing import List
#from .permission import Permission
@db.mapper_registry.mapped
@dataclass
class Group:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "groups"
    __table_args__ = (UniqueConstraint('name', name='_name_uc'),)
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    name: str = field(default=None, metadata={"sa": Column(String(256))})
    #permissions: List[Permission] = field(default_factory=list,metadata={ "sa": lambda: relationship("Permission",lazy="joined")})
