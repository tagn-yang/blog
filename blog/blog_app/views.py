from datetime import date
from django.db.models import Q, F
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .models import Post, Tag, Category
from comment_app.forms import CommentForm
from comment_app.models import Comment


# function view
# def post_list(request, category_id=None, tag_id=None):
#     # content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
#     #     category_id=category_id,
#     #     tag_id=tag_id,
#     # )
#     # return HttpResponse(content)
#     tag = None
#     category = None
#     if tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except Tag.DoseNotExist:
#             post_list = []
#         else:
#             post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category = Category.objects.get(id=category_id)
#                 # post_list = post_list.filter(category_id=category_id)
#             except Category.DoseNotExist:
#                 category = None
#             else:
#                 post_list = post_list.filter(category_id=category_id)
#
#     from config_app.models import Sidebar
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': Sidebar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id=None):
#     # return HttpResponse('detail')
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoseNotExist:
#         post = None
#
#     return render(request, 'blog/detail.html', context={'post': post})


# class-based view


class CommentViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from blog.config_app.models import SideBar
        context.update({
            'sidebar': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """rewrite queryset, classification filtering"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """rewrite queryset, classification tag"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommentViewMixin, DetailView):
    # model = Post
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path),
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # One minute

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 24 hours

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.objects.id).update(pv=F('pv') + 1,
                                                           uv=F('uv') + 1)

        if increase_pv:
            Post.objects.filter(pk=self.objects.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.objects.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', ' ')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
