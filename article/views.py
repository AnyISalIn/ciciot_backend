from article.models import Article, Category, Like

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import TemplateView, View, DetailView as DetailView, ListView
from django.shortcuts import render, get_object_or_404


def get_hot_articles(number):
    return Article.objects.order_by('-view').filter(is_public=True)[:number]


def fetch_category_articles(category_name, number):
    return Category.objects.get(name=category_name). \
               article_set.filter(is_public=True).all()[:number]


class HotRecommendMixin(object):
    hot_articles = get_hot_articles(6)
    recomment_articles = Article.objects.filter(is_public=True)[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'hot_articles': self.hot_articles,
                'recomment_articles': self.recomment_articles
            }
        )
        return context


class SiteIndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': '物联网技术与应用|物联网学报',
                'second_articles': Article.objects.filter(is_public=True)[:6],
                'paper_articles': fetch_category_articles('物联网学报', 3),
                'session_articles': fetch_category_articles('会展', 4),
                'boss_articles': fetch_category_articles('大咖视点', 4)
            }
        )
        return context


class ArticleDetailView(HotRecommendMixin, DetailView):
    template_name = 'detail.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': '{} - 物联网技术与应用'.format(context['article'].title)
        })
        return context


class ArticleListView(ListView):
    template_name = 'list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category_name = self.request.GET.get('category')
        self.category = get_object_or_404(Category, name=category_name)
        return self.category.article_set.filter(is_public=True).all()

    @staticmethod
    def get_next_categories(current_category):
        ret = dict()
        ret['current_category'] = current_category.name
        category_count = Category.objects.count()
        if current_category.id < category_count and (category_count - current_category.id) >= 2:
            ret['next_category'] = Category.objects.get(pk=current_category.id + 1).name
            ret['next_next_category'] = Category.objects.get(pk=current_category.id + 2).name
        elif current_category.id < category_count and (category_count - current_category.id) == 1:
            ret['next_category'] = Category.objects.get(pk=current_category.id + 1).name
            ret['next_next_category'] = Category.objects.get(pk=1).name
        else:
            ret['next_category'] = Category.objects.get(pk=1).name
            ret['next_next_category'] = Category.objects.get(pk=2).name
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': '{} - 物联网技术与应用'.format(self.category.name),
            'hot_articles': get_hot_articles(6),
            'news_articles': Article.objects.filter(is_public=True)[:4],
            'tech_articles': fetch_category_articles('前沿科技', 4),
            'net_articles': fetch_category_articles('网络技术', 4),
        })
        context.update(
            self.get_next_categories(self.category)
        )
        return context


class ArticleSearchView(HotRecommendMixin, ListView):
    template_name = 'search.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.keyword = self.request.GET.get('keyword', '')
        return Article.objects.filter(Q(title__contains=self.keyword) | Q(content__contains=self.keyword))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class ArticleLikeView(View):

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '需要登录才能喜欢这篇文章'}, status=401)
        article = Article.objects.get(pk=pk)
        if not article:
            return JsonResponse({'msg': '文章未找到'}, status=404)
        if request.user.like_set.filter(article__id=pk).first():
            return JsonResponse({'msg': '已经喜欢过这篇文章了'}, status=409)

        like = Like(user=request.user, article=article)
        like.save()
        return JsonResponse({'msg': 'success'}, status=201)
