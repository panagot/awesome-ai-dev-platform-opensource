# Fix for WORKFLOW_IDOR vulnerability
# Add proper authorization check before returning workflow data

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class WorkflowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only return workflows belonging to the authenticated user
        return Workflow.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        workflow = self.get_object()
        
        # Additional authorization check
        if workflow.user != request.user:
            raise PermissionDenied(
                "You do not have permission to access this workflow."
            )
        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        workflow = self.get_object()
        
        # Verify ownership before update
        if workflow.user != request.user:
            raise PermissionDenied(
                "You do not have permission to modify this workflow."
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        workflow = self.get_object()
        
        # Verify ownership before deletion
        if workflow.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this workflow."
            )
        
        return super().destroy(request, *args, **kwargs)