import time
from typing import Dict, Any
import httpx

async def check_http_status(url: str, timeout_seconds: float = 10.0) -> Dict[str, Any]:
    """
    Trimite o cerere HTTP GET către URL și măsoară timpul de răspuns.
    Gestionează redirect-urile și returnează starea site-ului.
    """
    start_time = time.perf_counter()
    
    # Adăugăm un User-Agent credibil pentru a evita blocajele de tip Cloudflare/WAF simple
    headers = {
        "User-Agent": "PulseGuard/1.0 (Uptime Monitor; Linux/x86_64)"
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds) as client:
            response = await client.get(url, headers=headers)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Un site este considerat UP dacă returnează coduri de succes (2xx) sau redirecționări finale (3xx)
            is_up = response.status_code < 400
            
            return {
                "is_up": is_up,
                "status_code": response.status_code,
                "response_time_ms": elapsed_ms,
                "error_message": None
            }
            
    except httpx.TimeoutException:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "is_up": False,
            "status_code": None,
            "response_time_ms": elapsed_ms,
            "error_message": f"Connection timed out after {timeout_seconds}s"
        }
        
    except httpx.ConnectError:
        return {
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error_message": "Failed to establish TCP connection (DNS resolution failure or host unreachable)"
        }
        
    except httpx.RequestError as exc:
        return {
            "is_up": False,
            "status_code": None,
            "response_time_ms": None,
            "error_message": f"HTTP request failed: {str(exc)}"
        }
