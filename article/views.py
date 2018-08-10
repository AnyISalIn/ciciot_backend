from article.models import Article, Category, Like

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404


def get_hot_articles(number):
    return Article.objects.filter(is_public=True)[:number]


def fetch_category_articles(category_name, number):
    return Category.objects.get(name=category_name). \
               article_set.filter(is_public=True).all()[:number]


class IndexView(TemplateView):
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


class DetailView(View):
    template_name = 'detail.html'

    def get(self, request, pk):
        article = get_object_or_404(Article, is_public=True, pk=pk)
        article.view += 1
        context = {
            'page_title': '{} - 物联网技术与应用'.format(article.title),
            'article': article,
            'category': article.categorise.first().name,
            'hot_articles': get_hot_articles(6),
            'recomment_articles': Article.objects.filter(is_public=True)[:5],
        }

        article.save()

        return render(request, self.template_name, context)


class ListView(View):
    template_name = 'list.html'

    def get(self, request):
        category_name = request.GET.get('category')
        category = get_object_or_404(Category, name=category_name)
        articles = category.article_set.filter(is_public=True).all()

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

        context = {
            'page_title': '{} - 物联网技术与应用'.format(category.name),
            'articles': articles,
            'hot_articles': get_hot_articles(6),
            'news_articles': Article.objects.filter(is_public=True)[:4],
            'tech_articles': fetch_category_articles('前沿科技', 4),
            'net_articles': fetch_category_articles('网络技术', 4),
        }

        context.update(get_next_categories(category))
        return render(request, self.template_name, context)


class SearchView(View):
    template_name = 'search.html'

    def get(self, request):
        keyword = request.GET.get('keyword', '')
        articles = Article.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword)).all()
        return render(request, self.template_name, {'articles': articles,
                                                    'keyword': keyword,
                                                    'count': articles.count(),
                                                    'hot_articles': get_hot_articles(6),
                                                    'recomment_articles': Article.objects.filter(is_public=True)[:5],
                                                    })


class LikeView(View):

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '需要登录才能喜欢这篇文章'}, status=401)
        article = Article.objects.get(pk=pk)
        if not article:
            return JsonResponse({'msg': '文章未找到'}, status=404)
        if request.user.like_set.filter(article__id=pk).first():
            return JsonResponse({'msg': '已经喜欢过这篇文章了'}, status=409)

        like = Like()
        like.user = request.user
        like.article = article
        like.save()
        return JsonResponse({'msg': 'success'}, status=201)
