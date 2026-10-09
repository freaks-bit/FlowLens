from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(
        ForeignKey("zones.id", ondelete="CASCADE"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(160))
    serial_number: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(30), default="offline")
    installed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    zone: Mapped["Zone"] = relationship(back_populates="sensors")
    count_events: Mapped[list["CountEvent"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan",
    )