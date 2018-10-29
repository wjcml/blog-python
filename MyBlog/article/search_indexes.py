from haystack import indexes
# 修改此处，为你自己的model
from .models import ArticlePost

# 修改此处，类名为模型类的名称+Index，比如模型类为ArticlePost,则这里类名为ArticlePostIndex
class ArticlePostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 修改此处，为你自己的model
        return ArticlePost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()