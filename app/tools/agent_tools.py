from langchain_core.tools import tool

from app.services.finance_service import FinanceService
from app.services.vehicle_service import VehicleService
from app.models.SearchRequest import SearchRequest
from app.models.vehicle import Vehicle


class AgentTools:

    def __init__(self):
        self.vehicle_service = VehicleService()
        self.finance_service = FinanceService()

    def get_tools(self):

        @tool
        def search_vehicles(request: SearchRequest) -> list[Vehicle]:
            """Search vehicles using the provided search criteria."""

            return self.vehicle_service.search(
                brand=request.brand,
                max_price=request.max_price,
                vehicle_type=request.vehicle_type,
            )

        @tool
        def get_vehicle_details(vehicle_id: int):
            """Get detailed information about a vehicle using its ID."""

            vehicle = self.vehicle_service.get_by_id(vehicle_id)

            if vehicle is None:
                return "Vehicle not found."

            return vehicle

        @tool
        def calculate_emi(
            principal: float,
            annual_rate: float,
            months: int,
        ):
            """
            Calculate monthly EMI and total loan cost.

            principal: loan amount, not vehicle price.
            annual_rate: annual interest rate as a percentage.
            months: loan duration in months.
            """

            return self.finance_service.calculate_emi(
                principal=principal,
                annual_rate=annual_rate,
                months=months,
            )

        return [
            search_vehicles,
            get_vehicle_details,
            calculate_emi,
        ]