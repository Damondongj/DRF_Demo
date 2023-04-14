from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    # 创建两个可读字段 author 和 status 字段，用以覆盖原来Article 模型默认的字段
    # 其中指定 author 字段的来源 source 为单个 author对象的username
    # status 字段为 get_status_display 方法返回的完整状态
    # 这样会出现一个问题，我们定义了一个仅可读的status字段把原来的status字段覆盖掉了
    # 这样反序列化时候用户将不能再对文章发表状态进行修改，原来的status字段是可读可修改的
    # 一个更好的方式在 ArticleSerializer 新增一个为 full_status 的可读字段，而不是简单覆盖原本可读可写的字段
    author = serializers.ReadOnlyField(source="author.username")
    status = serializers.ReadOnlyField(source="get_status_display")
    # full_status = serializers.ReadOnlyField(source="get_statis_display")
    cn_status = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')

    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''

    def to_representation(self, instance):
        # 返回出去的结果
        data = super().to_representation(instance)
        data["aaa"] = "bbb"
        return data
