from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Zone(Base):
    __tablename__ = "zones"
    __table_args__ = (
        CheckConstraint("capacity >= 0", name="ck_zones_capacity_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(160))
    code: Mapped[str] = mapped_column(String(60))
    floor_label: Mapped[str | None] = mapped_column(String(60), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=0)
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

    site: Mapped["Site"] = relationship(back_populates="zones")
    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="zone",
        cascade="all, delete-orphan",
    )
    alert_rules: Mapped[list["AlertRule"]] = relationship(
        back_populates="zone",
        cascade="all, delete-orphan",
    )