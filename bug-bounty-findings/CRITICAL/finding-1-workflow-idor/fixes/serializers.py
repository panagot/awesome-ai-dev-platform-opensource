# Fix: Ensure workflow user is set from authenticated user

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ['id', 'name', 'steps', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Always set user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)