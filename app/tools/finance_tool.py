from langchain_core.tools import tool

from app.services.finance_service import FinanceService


finance_service = FinanceService()


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

    return finance_service.calculate_emi(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
    )