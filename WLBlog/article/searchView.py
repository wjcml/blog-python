from django.db.models import Q
from haystack.generic_views import SearchView
from haystack.models import SearchResult

from article.models import Article

from django.core.cache import cache

from package import pagination


class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset.all()

    def get_context_data(self, *args, **kwargs):

        # songs = Song.objects.filter(name=kwargs['q'])
        # for song in songs:
        #     print(song.name)
        mySearchView = super(MySearchView, self)

        form_data = mySearchView.get_form_kwargs()['data']
        # search_method = form_data['search-method']
        self.ordering = '-updated'
        context = dict()

        page = form_data.get('page', None)
        articles = Article.objects.filter(Q(title__icontains=form_data['q']) | Q(body__icontains=form_data['q']), is_secret=0, deleted=0).order_by("-updated")

        # 分页
        paginations, current_page = pagination(articles, page=page, num=None)
        # context['articles'] = paginations
        context['page'] = current_page

        context['articles'] = paginations
        context['search'] = form_data['q']

        cache.set('host:'+self.request.get_host()+'url', self.request.get_host()+self.request.get_full_path(), 60*10)
        context['query'] = True if context['articles'] else False
        return context
