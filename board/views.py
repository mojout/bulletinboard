from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from board.models import Announcement, Category


class BoardCategory(ListView):
    pass
def AnnouncementList(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement/list.html', {'announcements': announcements})


def Announcement_detail(request, year, month, day, announcement):
    announcement = get_object_or_404(Announcement,
                                     status=Announcement.Status.PUBLISHED,
                                     slug=announcement,
                                     publish__year=year,
                                     publish__month=month,
                                     publish__day=day)

    return render(request, 'announcement/detail.html', {'announcement': announcement})
