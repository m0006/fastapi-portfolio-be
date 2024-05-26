from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db_common import Base


class TaxiLocation(Base):
    __tablename__ = "taxilocations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_id: Mapped[int] = mapped_column(Integer)
    time: Mapped[str] = mapped_column(String(40))
    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )

    def __str__(self):
        return f"TaxiLocation -- {self.driver_id} @ {self.time} & {self.geom}"
