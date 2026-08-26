evaluation_cases = [
    {
        "input": "Find Honda cars under 10 lakh.",
        "expected_tool": "search_vehicles",
    },
    {
        "input": "Tell me about vehicle 1.",
        "expected_tool": "get_vehicle_details",
    },
    {
        "input": (
            "Calculate EMI for an 8 lakh loan "
            "at 8.5% for 5 years."
        ),
        "expected_tool": "calculate_emi",
    },
    {
        "input": "What is an SUV?",
        "expected_tool": None,
    },
]