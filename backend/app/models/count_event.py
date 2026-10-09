from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CountEvent(Base):
    __tablename__ = "count_events"
    __table_args__ = (
        CheckConstraint("direction IN ('IN', 'OUT')", name="ck_count_events_direction"),
        CheckConstraint("count > 0", name="ck_count_events_count_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id", ondelete="CASCADE"),
        index=True,
    )

    direction: Mapped[str] = mapped_column(String(3))
    count: Mapped[int] = mapped_column(Integer, default=1)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    sensor: Mapped["Sensor"] = relationship(back_populates="count_events")