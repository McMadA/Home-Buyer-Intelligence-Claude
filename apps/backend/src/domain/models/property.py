from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Property:
    id: UUID = field(default_factory=uuid4)
    session_id: UUID | None = None
    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    square_meters: float | None = None
    year_built: int | None = None
    energy_label: str | None = None
    property_type: str | None = None
    asking_price: float | None = None
    hoa_monthly_cost: float | None = None
    num_rooms: int | None = None
    has_garden: bool | None = None
    has_parking: bool | None = None
    bag_id: str | None = None
