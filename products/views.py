from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Sum
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProductReview(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product).data
        return Response(serializer)


class OrderDetails(APIView):
    def get(self, request, order_id):
        orders = Orders.objects.get(id=order_id)
        serializer = OrderSerializer(orders).data
        return Response(serializer)


class SearchView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = request.GET.get("query", None)
        page_no = request.GET.get("page", None)
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by(
            "id",
        )
        paginate = Paginator(products, 5)
        page = paginate.get_page(page_no)
        serializer = ProductSerializer(page.object_list, many=True).data
        return Response(
            {
                "data": serializer,
                "total_page": paginate.num_pages,
                "count": paginate.count,
            }
        )


class FilterView(APIView):
    def get(self, request):
        category = request.GET.get("cat", None)
        brand = request.GET.get("brand", None)
        minPrice = request.GET.get("min", None)
        maxPrice = request.GET.get("max", None)
        query = request.GET.get("query", None)
        page_no = request.GET.get("page", None)
        products = Product.objects.all().order_by("id")
        if query:
            products = products.filter(name__icontains=query)
        if category:
            products = products.filter(category__iexact=category)
        if brand:
            products = products.filter(brand__iexact=brand)
        if minPrice:
            products = products.filter(price__gte=int(minPrice))
        if maxPrice:
            products = products.filter(price__lte=int(maxPrice))
        paginate = Paginator(products, 5)
        page = paginate.get_page(page_no)
        serializer = ProductSerializer(page.object_list, many=True).data
        return Response(
            {
                "data": serializer,
                "total_page": paginate.num_pages,
                "count": paginate.count,
            }
        )


class PaginatedView(APIView):
    def get(self, request):
        page_no = request.GET.get("page", 1)
        products = Product.objects.all().order_by("-name")
        paginate = Paginator(products, 5)
        page = paginate.get_page(page_no)
        serializer = ProductSerializer(page.object_list, many=True).data
        return Response(
            {
                "data": serializer,
                "total_page": paginate.num_pages,
                "count": paginate.count,
            }
        )


class PriceRangeView(APIView):
    def get(self, request):
        minPrice = request.GET.get("min", None)
        maxPrice = request.GET.get("max", None)
        if maxPrice and minPrice:
            product = Product.objects.filter(Q(price__gt=int(minPrice)) & Q(price__lt=int(maxPrice)))
            serializer = ProductSerializer(product, many=True).data
            return Response(serializer, status=200)
        return Response({"message": "min and max parameters are required"}, status=400)


class MultipleView(APIView):
    def get(self, request):
        para = request.GET.get("para", None)
        products = Product.objects.filter(Q(name__icontains=para) | Q(description__icontains=para))
        serializer = ProductSerializer(products, many=True).data
        return Response(serializer, status=200)


class AddReview(APIView):
    def post(self, request):
        data = request.data
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            product = obj.product
            avg = Review.objects.filter(product=product.id).aggregate(test=Avg("rate"))
            product.avg_review = avg["test"]
            product.save()
            return Response({"message": "Review added"}, status=201)
        return Response(serializer.errors, status=400)


class SignupView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created succesfully"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login succesfull",
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                }
            )
        return Response(serializer.errors, status=401)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        if user.check_password(data["old_password"]):
            user.set_password(data["new_password"])
            user.save()
            return Response({"message": "Password has been changed"}, status=200)
        return Response({"message": "Password does not match"}, status=400)


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        print(request.user.id)
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=401)

    def get(self, request):
        invoice = Invoice.objects.filter(user=request.user.id)
        serializer = InvoiceSerializer(invoice, many=True).data
        return Response(serializer, status=200)
