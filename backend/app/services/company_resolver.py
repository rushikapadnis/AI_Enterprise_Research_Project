class CompanyResolver:
    
    COMPANY_TICKERS = {
        "nvidia": "NVDA",
        "microsoft": "MSFT",
        "apple": "AAPL",
        "amazon": "AMZN",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "meta": "META",
        "tesla": "TSLA",
    }

    def resolve(self, company_name: str) -> str:

        normalized_name = company_name.strip().lower()

        ticker = self.COMPANY_TICKERS.get(
            normalized_name
        )

        if not ticker:
            raise ValueError(
                f"Ticker not found for company: {company_name}"
            )

        return ticker