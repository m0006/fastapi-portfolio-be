import json
import shapely

from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_validator


class PointToJson:
    @field_validator("geom", mode="before")
    def turn_point_to_json(cls, value):
        shape = to_shape(value)
        return {
            "x": shape.x,
            "y": shape.y
        }


class HousingAttribValSchema(BaseModel):
    """
    Schema to get option values for frontend components.
    """

    region:             list[str]
    type:               list[str]
    price_max:          int
    sqfeet_max:         int
    beds:               list[int]
    baths:              list[float]
    laundry_options:    list[str]
    parking_options:    list[str]


class ListingSchema(BaseModel, PointToJson):
    """
    Schema for listings resulting from querying.
    """
    id: int
    region: str
    price: int
    type: str
    sqfeet: int
    beds: int
    baths: float

    cats_allowed: int
    dogs_allowed: int
    smoking_allowed: int
    wheelchair_access: int
    electric_vehicle_charge: int
    comes_furnished: int

    laundry_options: str | None
    parking_options: str | None

    geom: dict[str, float]


class MbtaLineSchema(BaseModel):
    name: str
    type: str

    geom: dict[str, str | list]

    @field_validator("geom", mode="before")
    def turn_multiline_to_json(cls, value):
        geojson = json.loads(
            shapely.to_geojson(
                to_shape(value)
            )
        )

        return {
            "type": "MultiLineString",
            "coordinates": geojson["coordinates"]
        }


class MbtaStationSchema(BaseModel, PointToJson):
    name: str
    line: str
    type: str

    geom: dict[str, float]
