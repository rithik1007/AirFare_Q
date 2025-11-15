# agent/tools_client.py
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

MCP_BASE = os.getenv("MCP_BASE", "http://localhost:8000")

class ToolsClient:
    def __init__(self, base_url: str = None):
        self.base = base_url or MCP_BASE
        self.client = httpx.AsyncClient(timeout=15.0)

    async def search_flights(self, origin, destination, date, passengers=1):
        payload = {"origin": origin, "destination": destination, "date": date, "passengers": passengers}
        r = await self.client.post(f"{self.base}/search_flights", json=payload)
        r.raise_for_status()
        return r.json()

    async def search_hotels(self, city, checkin, checkout, max_price=None):
        payload = {"city": city, "checkin": checkin, "checkout": checkout, "guests": 1, "max_price_inr": max_price}
        r = await self.client.post(f"{self.base}/search_hotels", json=payload)
        r.raise_for_status()
        return r.json()

    async def compare_fares(self, flight_ids):
        r = await self.client.post(f"{self.base}/compare_fares", json=flight_ids)
        r.raise_for_status()
        return r.json()

    async def book_flight(self, flight_id, passenger_name, email):
        payload = {"flight_id": flight_id, "passenger_name": passenger_name, "email": email}
        r = await self.client.post(f"{self.base}/book_flight", json=payload)
        r.raise_for_status()
        return r.json()

    async def book_hotel(self, hotel_id, guest_name, email):
        payload = {"hotel_id": hotel_id, "guest_name": guest_name, "email": email}
        r = await self.client.post(f"{self.base}/book_hotel", json=payload)
        r.raise_for_status()
        return r.json()
    async def close(self):
        await self.client.aclose()      