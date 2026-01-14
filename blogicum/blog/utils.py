from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone


def get_published_posts(queryset):
    queryset = queryset.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'category', 'author'
    ).annotate(comment_count=Count('comments'))

    return queryset


def paginate_queryset(queryset, request, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
