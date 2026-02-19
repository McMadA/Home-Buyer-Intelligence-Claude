from pydantic import BaseModel


class MarketDataResponse(BaseModel):
    municipality: str | None = None
    avg_purchase_price: float | None = None
    num_transactions: int | None = None
    price_index: float | None = None
    period: str | None = None
    bag_data: dict | None = None
    energy_label_data: dict | None = None
