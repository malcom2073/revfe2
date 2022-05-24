from dataclasses import dataclass
from dataclasses import field, asdict
import db
from typing import List
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

@db.mapper_registry.mapped
@dataclass
class GroupPermissions:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "grouppermissions"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    permission_id: int = field(
        init=False, metadata={"sa": Column(ForeignKey("permissions.id"))}
    )
    group_id: int = field(
        init=False, metadata={"sa": Column(ForeignKey("groups.id"))}
    )

db.main_table_list[GroupPermissions.__tablename__] = GroupPermissions