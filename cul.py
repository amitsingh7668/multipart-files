import requests
from typing import List, Optional

class TradingAccountServiceClient:
    BASE_CUMULUS_TRADING_ACCOUNT_URL = "http://10.197.213.87/trading-account-service/v1/tradingaccounts/query"
    QUERY_PARAM = "systemId"
    
    def __init__(self, username: str, password: str):
        self.auth = (username, password)  # Basic authentication credentials
    
    def find_trading_account_by_system_id(self, system_id: str) -> Optional[List[dict]]:
        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Request body payload
            payload = {
                self.QUERY_PARAM: [system_id]
            }
            
            # Make the POST request
            response = requests.post(
                self.BASE_CUMULUS_TRADING_ACCOUNT_URL,
                json=payload,
                headers=headers,
                auth=self.auth
            )
            
            # Check response status
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse and return the response JSON
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    username = "your_username"
    password = "your_password"
    system_id = "exampleSystemId"
    
    client = TradingAccountServiceClient(username, password)
    trading_accounts = client.find_trading_account_by_system_id(system_id)
    
    if trading_accounts:
        print("Trading Accounts:", trading_accounts)
    else:
        print("No trading accounts found or an error occurred.")
