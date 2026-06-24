import socket
import ipaddress
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

ALLOWED_SCHEME = "https"
ALLOWED_DOMAINS = {"doe.gov.ph", "www.doe.gov.ph", "prod-cms.doe.gov.ph"}

def is_internal_ip(ip_str: str) -> bool:
    """Check if an IP address belongs to loopback, private or local ranges."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_loopback or 
            ip.is_private or 
            ip.is_link_local or 
            ip.is_unspecified or 
            ip.is_multicast or 
            ip.is_reserved
        )
    except ValueError:
        # Invalid IP address representation
        return True

def validate_and_resolve_url(url: str) -> bool:
    """
    Validates that a URL is:
    1. A valid URL with scheme HTTPS.
    2. Belongs strictly to ALLOWED_DOMAINS.
    3. Resolves to a public, non-internal/non-private IP address.
    """
    try:
        if not url:
            return False
            
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme.lower() != ALLOWED_SCHEME:
            logger.warning(f"URL validation failed: Invalid scheme {parsed.scheme} in URL {url}")
            return False
            
        # Check domain
        hostname = parsed.hostname
        if not hostname:
            logger.warning(f"URL validation failed: No hostname in URL {url}")
            return False
            
        hostname_lower = hostname.lower()
        if hostname_lower not in ALLOWED_DOMAINS:
            logger.warning(f"URL validation failed: Domain {hostname_lower} is not in ALLOWED_DOMAINS")
            return False
            
        # Resolve hostname to check for SSRF (internal IPs)
        try:
            # We fetch all address info for the host
            addr_info = socket.getaddrinfo(hostname_lower, None)
            for info in addr_info:
                ip_addr = info[4][0]
                if is_internal_ip(ip_addr):
                    logger.warning(f"URL validation failed: Hostname {hostname_lower} resolved to internal IP {ip_addr}")
                    return False
        except socket.gaierror as e:
            logger.warning(f"URL validation failed: DNS resolution failure for {hostname_lower}: {e}")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Error during URL validation of {url}: {e}")
        return False
