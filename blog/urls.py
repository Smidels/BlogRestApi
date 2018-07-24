from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework.routers import DefaultRouter
from blog import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),

	url(r'^rest-auth/', include('rest_auth.urls')),
	url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
	
	url(r'^api-token-auth/', obtain_jwt_token),
	url(r'^api-token-refresh/', refresh_jwt_token),
	url(r'^api-token-verify/', verify_jwt_token),

	url(r'^like/', views.like),
	url(r'^unlike/', views.unlike),

	url(r'^bot/', views.run_bot),
]