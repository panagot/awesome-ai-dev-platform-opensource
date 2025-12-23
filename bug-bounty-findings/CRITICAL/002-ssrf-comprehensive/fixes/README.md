# SSRF Fix Implementation

## Files

- `url_validator.py` - Comprehensive URL validation module for SSRF protection

## Usage

### Basic Usage

```python
from url_validator import validate_url

try:
    validated_url = validate_url(
        url="http://example.com/api",
        parameter_name="url",
        require_whitelist=False
    )
    # Use validated_url safely
except ValidationError as e:
    # Handle validation error
    print(f"Invalid URL: {e}")
```

### In Django REST Framework View

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from url_validator import validate_url_parameter

@api_view(['POST'])
def my_endpoint(request):
    try:
        validated_url = validate_url_parameter(
            request.data,
            param_name='url',
            require_whitelist=True
        )
        # Process validated URL
    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
```

## Configuration

Update `ALLOWED_DOMAINS` list in `url_validator.py` with approved domains for your environment.

## Testing

After implementing:
- ✅ Internal IPs are blocked (127.0.0.1, 10.0.0.0/8, etc.)
- ✅ Cloud metadata endpoints are blocked
- ✅ Whitelisted domains work correctly
- ✅ Non-whitelisted domains are rejected
- ✅ Clear error messages for blocked requests

