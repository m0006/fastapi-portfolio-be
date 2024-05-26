from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_validator


class TaxiIdSchema(BaseModel):
    driver_id: int


class TaxiLocationSchema(BaseModel):
    driver_id: int
    time: str
    geom: dict[str, float]

    @field_validator("geom", mode="before")
    def turn_geom_into_wkt(cls, value):
        shape = to_shape(value)
        return {
            "latitude": shape.x,
            "longitude": shape.y
        }
