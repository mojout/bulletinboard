from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from board.forms import AddAnnouncementForm
from board.models import Announcement, Category
from board.utils import DataMixin


class PostList(ListView):
    model = Announcement
    template_name = 'announcement/list.html'
    context_object_name = 'announcements'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostCategory(DataMixin, ListView):
    model = Announcement
    template_name = 'announcement/list.html'
    context_object_name = 'announcements'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Announcement.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# def AnnouncementList(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     announcements = Announcement.objects.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         announcements = announcements.filter(category=category)
#     return render(request, 'announcement/list.html', {'announcements': announcements,
#                                                       'category': category,
#                                                       'categories': categories})
#
#
class PostDetail(DetailView):
    model = Announcement
    template_name = 'announcement/detail.html'

    def get_success_url(self):
        return reverse('announcement_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category
        return context


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = AddAnnouncementForm
    model = Announcement
    template_name = 'announcement/announcement_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            post.author, created = User.objects.get_or_create(id=self.request.user.id)
            post.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AddAnnouncementForm
    template_name = 'announcement/announcement_update.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


