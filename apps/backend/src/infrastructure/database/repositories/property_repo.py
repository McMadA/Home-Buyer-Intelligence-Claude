from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.property import Property
from src.domain.interfaces.property_repository import PropertyRepository
from src.infrastructure.database.models import PropertyModel

class SQLPropertyRepository(PropertyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, prop: Property) -> Property:
        result = await self._session.execute(
            select(PropertyModel).where(PropertyModel.id == str(prop.id))
        )
        model = result.scalar_one_or_none()

        if not model:
            model = PropertyModel(id=str(prop.id))
            self._session.add(model)

        model.session_id = str(prop.session_id) if prop.session_id else None
        model.address = prop.address
        model.postal_code = prop.postal_code
        model.city = prop.city
        model.square_meters = prop.square_meters
        model.year_built = prop.year_built
        model.energy_label = prop.energy_label
        model.property_type = prop.property_type
        model.asking_price = prop.asking_price
        model.hoa_monthly_cost = prop.hoa_monthly_cost
        model.num_rooms = prop.num_rooms
        model.has_garden = prop.has_garden
        model.has_parking = prop.has_parking
        model.bag_id = prop.bag_id

        await self._session.commit()
        return prop

    async def get_by_id(self, prop_id: UUID) -> Property | None:
        result = await self._session.execute(
            select(PropertyModel).where(PropertyModel.id == str(prop_id))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Property(
            id=UUID(model.id),
            session_id=UUID(model.session_id) if model.session_id else None,
            address=model.address,
            postal_code=model.postal_code,
            city=model.city,
            square_meters=model.square_meters,
            year_built=model.year_built,
            energy_label=model.energy_label,
            property_type=model.property_type,
            asking_price=model.asking_price,
            hoa_monthly_cost=model.hoa_monthly_cost,
            num_rooms=model.num_rooms,
            has_garden=model.has_garden,
            has_parking=model.has_parking,
            bag_id=model.bag_id,
        )
