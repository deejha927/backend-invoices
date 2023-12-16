from .views import *
from django.urls import path

urlpatterns = [
    path("review/<int:product_id>/", ProductReview.as_view(), name="Product-Review"),
    path("order/<int:order_id>/", OrderDetails.as_view(), name="Order-Details"),
    path("search/", SearchView.as_view(), name="Search-View"),
    path("paginate/", PaginatedView.as_view(), name="Paginated-View"),
    path("range/", PriceRangeView.as_view(), name="Price-Range-View"),
    path("filter/", MultipleView.as_view(), name="Multiple-View"),
    path("addreview/", AddReview.as_view(), name="Add-Review"),
    path("signup/", SignupView.as_view(), name="Signup-View"),
    path("login/", LoginView.as_view(), name="Login-View"),
    path("invoice/", InvoiceView.as_view(), name="Invoice-View"),
]
