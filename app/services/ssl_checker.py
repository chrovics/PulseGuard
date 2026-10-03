import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import Dict, Any

def get_ssl_expiry(url: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
    """
    Extrage data de expirare și emitentul certificatului SSL pentru un URL HTTPS dat.
    """
    parsed = urlparse(url)
    hostname = parsed.hostname or url
    port = parsed.port or 443

    # Protocolul SSL are sens doar pe HTTPS
    if parsed.scheme and parsed.scheme != "https":
        return {
            "valid": False,
            "days_remaining": None,
            "expires_at": None,
            "issuer": None,
            "error": "URL does not use HTTPS protocol"
        }

    # Creăm un context SSL standard cu verificare de autoritate de certificare (CA)
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=timeout_seconds) as sock:
            # SNI (Server Name Indication) este critic pentru serverele care găzduiesc mai multe domenii pe un singur IP
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                # Format standard OpenSSL date: 'May 15 12:00:00 2026 GMT'
                expire_str = cert["notAfter"]
                expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                
                days_remaining = (expire_date - now).days
                
                # Extragem Organization (O) sau Common Name (CN) al emitentului
                issuer_dict = dict(x[0] for x in cert.get("issuer", []))
                issuer_name = issuer_dict.get("organizationName", issuer_dict.get("commonName", "Unknown Issuer"))

                return {
                    "valid": days_remaining > 0,
                    "days_remaining": days_remaining,
                    "expires_at": expire_date.isoformat(),
                    "issuer": issuer_name,
                    "error": None
                }

    except ssl.SSLCertVerificationError as exc:
        return {
            "valid": False,
            "days_remaining": None,
            "expires_at": None,
            "issuer": None,
            "error": f"SSL Verification Failed: {exc.verify_message}"
        }
    except socket.timeout:
        return {
            "valid": False,
            "days_remaining": None,
            "expires_at": None,
            "issuer": None,
            "error": "SSL handshake timed out"
        }
    except Exception as exc:
        return {
            "valid": False,
            "days_remaining": None,
            "expires_at": None,
            "issuer": None,
            "error": f"Socket/SSL Error: {str(exc)}"
        }
