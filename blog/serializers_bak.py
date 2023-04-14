from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model

User = get_user_model()


# class ArticleSerializer(serializers.ModelSerializer):
#     author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Article
#         fields = '__all__'
#         read_only_fields = ('id', 'create_date')
#
class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=90)
    body = serializers.CharField(required=True, allow_blank=True)
    author = serializers.ReadOnlyField(source="author.id")
    status = serializers.ChoiceField(choices=Article.STATUS_CHOICES, default="p")
    create_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    def to_representation(self, instance):
        # 这里面的 instance 就是模型类的一个实例
        # type(instance) <class 'blog.models.Article'>
        ret = super().to_representation(instance)
        print(ret)
        return ret


