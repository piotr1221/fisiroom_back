from rest_framework import serializers


class ExtraFieldsModelSerializer(serializers.ModelSerializer):
    '''
    Model Serializer modification that allows for extra fields
    beyond the __all__ keyword, hence avoiding boilerplate code
    when including all fields from model plus calculated ones.
    Requires variable <extra_fields> as list with the extra fields.
    '''
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldsModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields