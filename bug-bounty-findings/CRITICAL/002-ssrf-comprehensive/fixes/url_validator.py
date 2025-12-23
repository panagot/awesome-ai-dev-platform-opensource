# SSRF Protection: Comprehensive URL Validation
# This module provides URL validation to prevent Server-Side Request Forgery (SSRF) attacks

from urllib.parse import urlparse
import ipaddress
import re
from django.core.exceptions import ValidationError


# Configure allowed domains (should be in environment config)
ALLOWED_DOMAINS = [
    # Add approved domains here
    # Example: 'api.example.com', 'cdn.example.com'
]

# Blocked hostnames/IPs
BLOCKED_HOSTNAMES = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '::1',
    '[::1]',
    'metadata.google.internal'
]


def is_internal_ip(hostname):
    """
    Check if hostname resolves to internal IP address
    
    Args:
        hostname: Hostname or IP address string
    
    Returns:
        bool: True if hostname is internal, False otherwise
    """
    try:
        ip = ipaddress.ip_address(hostname)
        return (
            ip.is_loopback or      # 127.0.0.0/8, ::1
            ip.is_private or       # 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
            ip.is_link_local or    # 169.254.0.0/16
            ip.is_reserved or      # Reserved IP ranges
            str(ip) == '0.0.0.0'
        )
    except ValueError:
        # Not a valid IP address, check if it's a blocked hostname
        return hostname.lower() in [h.lower() for h in BLOCKED_HOSTNAMES]


def is_cloud_metadata_endpoint(hostname):
    """
    Check if hostname is a cloud metadata endpoint
    
    Args:
        hostname: Hostname string
    
    Returns:
        bool: True if hostname is a cloud metadata endpoint
    """
    cloud_patterns = [
        r'^169\.254\.',                    # AWS metadata
        r'^metadata\.google\.internal',     # GCP metadata
        r'^169\.254\.169\.254',             # AWS metadata IP
        r'^100\.100\.100\.200',             # Alibaba Cloud metadata
    ]
    
    for pattern in cloud_patterns:
        if re.match(pattern, hostname, re.IGNORECASE):
            return True
    return False


def validate_url(url, parameter_name='url', require_whitelist=False):
    """
    Comprehensive URL validation for SSRF protection
    
    Args:
        url: URL string to validate
        parameter_name: Name of the parameter (for error messages)
        require_whitelist: Whether to enforce domain whitelist
    
    Returns:
        str: Validated URL string
    
    Raises:
        ValidationError: If URL is invalid or blocked
    """
    if not url:
        raise ValidationError(f"{parameter_name} cannot be empty")
    
    if not isinstance(url, str):
        raise ValidationError(f"{parameter_name} must be a string")
    
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValidationError(f"Invalid URL format in {parameter_name}: {e}")
    
    # Validate scheme
    if parsed.scheme not in ['http', 'https']:
        raise ValidationError(
            f"Only http and https schemes are allowed in {parameter_name}. "
            f"Found: {parsed.scheme}"
        )
    
    # Extract hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValidationError(f"URL in {parameter_name} must include a hostname")
    
    # Normalize hostname (remove brackets from IPv6)
    hostname = hostname.strip('[]')
    
    # Block internal IPs
    if is_internal_ip(hostname):
        raise ValidationError(
            f"Internal IP addresses are not allowed in {parameter_name}. "
            f"Blocked: {hostname}"
        )
    
    # Block cloud metadata endpoints
    if is_cloud_metadata_endpoint(hostname):
        raise ValidationError(
            f"Cloud metadata endpoints are not allowed in {parameter_name}. "
            f"Blocked: {hostname}"
        )
    
    # Enforce whitelist if required
    if require_whitelist and ALLOWED_DOMAINS:
        if hostname not in ALLOWED_DOMAINS:
            raise ValidationError(
                f"Domain '{hostname}' in {parameter_name} is not in the allowed list. "
                f"Allowed domains: {', '.join(ALLOWED_DOMAINS)}"
            )
    
    # Additional validation: Check for suspicious patterns
    suspicious_patterns = [
        r'^0+\.',           # Leading zeros in IP
        r'\.0+\.',          # Zeros in IP octets
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, hostname):
            raise ValidationError(
                f"Suspicious URL pattern detected in {parameter_name}: {hostname}"
            )
    
    return url


def validate_url_parameter(data, param_name='url', require_whitelist=False):
    """
    Validate URL parameter in request data with SSRF protection
    
    Args:
        data: Request data dictionary
        param_name: Name of the URL parameter to validate
        require_whitelist: Whether to enforce domain whitelist
    
    Returns:
        str: Validated URL string, or None if parameter not present
    
    Raises:
        ValidationError: If URL is invalid or blocked
    """
    url = data.get(param_name)
    if not url:
        return None
    
    return validate_url(url, param_name, require_whitelist)


# Example usage in Django REST Framework view
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .url_validator import validate_url_parameter

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_url_endpoint(request):
    # Validate all URL parameters
    url_params = ['url', 'link', 'image', 'src', 'redirect', 'next', 
                  'return', 'callback', 'webhook', 'endpoint', 'api', 
                  'target', 'destination', 'fetch', 'load', 'import', 
                  'include', 'file', 'path']
    
    for param in url_params:
        if param in request.data:
            try:
                validated = validate_url_parameter(
                    request.data, 
                    param, 
                    require_whitelist=True  # Set based on endpoint requirements
                )
                request.data[param] = validated
            except ValidationError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    # Process request with validated URLs
    # ... rest of endpoint logic ...
    
    return Response({"status": "success"})
"""

