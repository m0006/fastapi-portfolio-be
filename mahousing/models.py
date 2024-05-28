from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db_common import Base


MA_SRID = 26986


class HousingListing(Base):
    __tablename__ = "housinglisting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region: Mapped[str] = mapped_column(String(25))
    price: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(15))
    sqfeet: Mapped[int] = mapped_column(Integer)
    beds: Mapped[int] = mapped_column(Integer)
    baths: Mapped[float] = mapped_column(Float)

    cats_allowed: Mapped[int] = mapped_column(Integer)
    dogs_allowed: Mapped[int] = mapped_column(Integer)
    smoking_allowed: Mapped[int] = mapped_column(Integer)
    wheelchair_access: Mapped[int] = mapped_column(Integer)
    electric_vehicle_charge: Mapped[int] = mapped_column(Integer)
    comes_furnished: Mapped[int] = mapped_column(Integer)

    laundry_options: Mapped[str] = mapped_column(String(20))
    parking_options: Mapped[str] = mapped_column(String(20))

    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=MA_SRID, spatial_index=True)
    )

    def __str__(self):
        return f"Listing -- {self.type} in {self.region} for {self.price} @ {self.geom}"


class MbtaLine(Base):
    __tablename__ = "mbtaline"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    type: Mapped[str] = mapped_column(String(15))

    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="MULTILINESTRING", srid=MA_SRID, spatial_index=True)
    )

    def __str__(self):
        return f"MbtaLine -- {self.type}: {self.name}"


class MbtaStation(Base):
    __tablename__ = "mbtastation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    line: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(15))

    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=MA_SRID, spatial_index=True)
    )

    def __str__(self):
        return f"MbtaStation -- {self.type}: {self.name} on {self.line} @ {self.geom}"
