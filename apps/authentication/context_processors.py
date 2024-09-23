from apps.authentication.models import Profile, Contact
from apps.products.models import Product
from apps.orders.models import Order
from django.db.models import F

from django.contrib.auth.decorators import login_required


def guest_profiles_context(request):
    # Fetch all profiles with the role "guest"
    guest_profiles = Profile.objects.filter(role="guest")

    # Calculate the number of guest profiles
    guest_count = guest_profiles.count()

    # Return context dictionary
    return {
        "guest_profiles": guest_profiles,
        "guest_count": guest_count,
    }


def guest_user_feedback_context(request):
    # Fetch all invalid feedback entries
    user_feedback = Contact.objects.filter(is_valid=False)

    # Calculate the count of invalid feedback entries
    feedback_count = user_feedback.count()

    # Return context dictionary
    return {
        "user_feedback": user_feedback,
        "feedback_count": feedback_count,
    }


def low_stock_alerts_context(request):
    # Fetch all products along with their inventory
    products = Product.objects.select_related("inventory").all()

    # Filter products with low stock based on inventory
    low_stock_products = products.filter(
        inventory__quantity__lte=F("inventory__low_stock_threshold")
    )

    # Count of low stock products
    low_stock_count = low_stock_products.count()

    return {
        "low_stock_products": low_stock_products,
        "low_stock_count": low_stock_count,
    }


def pending_orders_context(request):
    # Fetch orders with statuses "Pending" or "Shipped"
    pending_and_shipped_orders = Order.objects.filter(
        status__in=["Pending", "Shipped"]
    ).select_related("customer")

    # Count the total number of pending and shipped orders
    pending_and_shipped_count = pending_and_shipped_orders.count()

    return {
        "pending_and_shipped_orders": pending_and_shipped_orders,
        "pending_orders_count": pending_and_shipped_count,
    }
