# Fix Implementation: IDOR - User Data Access

## Solution

### 1. Authorization Check

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    # Verify user can only access their own data (unless admin)
    if request.user.id != int(user_id) and not request.user.is_staff:
        raise PermissionDenied(
            "You do not have permission to access this user's data."
        )
    
    # Proceed with user data access
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
```

### 2. Resource-Level Permissions

```python
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # Only return current user's data (unless admin)
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        # Additional check for extra security
        if user.id != request.user.id and not request.user.is_staff:
            raise PermissionDenied("Permission denied")
        return super().retrieve(request, *args, **kwargs)
```

## Security Impact

This fix:
- Prevents unauthorized access to other users' data
- Ensures users can only access their own information
- Maintains admin access for legitimate use cases
- Provides clear error messages

---

**Status**: Ready for PR submission

