from haystack import indexes

# 引入你项目下的model（也就是你要将其作为检索关键词的models）
from article.models import Article


# 修改此处，类名为模型类的名称+Index，比如模型类为Article,则这里类名为ArticleIndex
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 修改此处，为你自己的model
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
