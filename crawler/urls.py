from django.conf.urls import url, patterns
from . import views

# member_router = DefaultRouter()
# member_router.register(r'member', views.MemberViewSet)

urlpatterns = patterns('',
    url(r'^$',views.index,name="home"), 
    url(r'^crawl/',views.contest),
    )
