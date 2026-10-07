import asyncio

from app.services.company_data import CompanyDataService


async def main():

    service = CompanyDataService()

    data = await service.get_company("NVDA")

    print("Company:", data.get("Name"))
    print("Symbol:", data.get("Symbol"))
    print("Industry:", data.get("Industry"))
    print("Sector:", data.get("Sector"))


asyncio.run(main())