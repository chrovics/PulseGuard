import asyncio
from app.services.checker import check_http_status
from app.services.ssl_checker import get_ssl_expiry

async def main():
    test_url = "https://github.com"
    
    print(f"--- Verificare HTTP pentru {test_url} ---")
    http_res = await check_http_status(test_url)
    print(http_res)

    print(f"\n--- Verificare SSL pentru {test_url} ---")
    ssl_res = get_ssl_expiry(test_url)
    print(ssl_res)

if __name__ == "__main__":
    asyncio.run(main())
