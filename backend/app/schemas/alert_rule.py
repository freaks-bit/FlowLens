from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AlertRuleType = Literal[
    "utilization_percent",
    "occupancy",
]


class AlertRuleCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=160,
    )
    rule_type: AlertRuleType
    threshold: float = Field(ge=0)
    is_enabled: bool = True


class AlertRuleUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=160,
    )
    rule_type: AlertRuleType | None = None
    threshold: float | None = Field(
        default=None,
        ge=0,
    )
    is_enabled: bool | None = None


class AlertRuleRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    zone_id: int
    name: str
    rule_type: AlertRuleType
    threshold: float
    is_enabled: bool
    created_at: datetime
    updated_at: datetime