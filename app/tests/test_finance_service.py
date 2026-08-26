from app.services.finance_service import FinanceService



def test_calculate_emi():

    service = FinanceService()

    result = service.calculate_emi(
        principal=800000,
        annual_rate=8.5,
        months=60,
    )

    assert result["monthly_emi"] == 16403.68

    assert result["total_payment"] == 984220.80

    assert result["total_interest"] == 184220.80