from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Text, TIMESTAMP
from datetime import datetime

class Base(DeclarativeBase):
    pass


class AutoriaCar(Base):
    __tablename__ = "autoria_cars"

    url: Mapped[str] = mapped_column(Text, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    price_usd: Mapped[int] = mapped_column(Integer)
    odometer: Mapped[int] = mapped_column(Integer, nullable=True)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    images_count: Mapped[int] = mapped_column(Integer, nullable=True)
    car_number: Mapped[str] = mapped_column(Text, nullable=True)
    car_vin: Mapped[str] = mapped_column(Text, nullable=True)
    datetime_found: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
