import stripe
from typing import Optional, List
from core.config import settings


class Payment:
    STRIPE_SECRET_KEY = settings.payment.PAYMENT_SECRET_KEY

    @staticmethod
    def initialize():
        stripe.api_key = Payment.STRIPE_SECRET_KEY

    @staticmethod
    def create_customer(email: str) -> stripe.Customer:
        try:
            customer = stripe.Customer.create(email=email)
            return customer
        except stripe.error.StripeError as e:
            raise Exception(f"Error creating customer: {str(e)}")

    @staticmethod
    def create_subscription(
        customer_id: str, price_id: str, trial_days: Optional[int] = None
    ) -> stripe.Subscription:
        try:
            subscription_args = {
                "customer": customer_id,
                "items": [{"price": price_id}],
            }
            if trial_days:
                subscription_args["trial_period_days"] = trial_days

            subscription = stripe.Subscription.create(**subscription_args)
            return subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Error creating subscription: {str(e)}")

    @staticmethod
    def cancel_subscription(subscription_id: str) -> stripe.DeletedSubscription:
        try:
            canceled_subscription = stripe.Subscription.delete(subscription_id)
            return canceled_subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Error canceling subscription: {str(e)}")

    @staticmethod
    def retrieve_customer(customer_id: str) -> stripe.Customer:
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return customer
        except stripe.error.StripeError as e:
            raise Exception(f"Error retrieving customer: {str(e)}")

    @staticmethod
    def retrieve_subscription(subscription_id: str) -> stripe.Subscription:
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Error retrieving subscription: {str(e)}")

    @staticmethod
    def update_subscription(
        subscription_id: str,
        items: Optional[List[dict]] = None,
        trial_days: Optional[int] = None,
    ) -> stripe.Subscription:
        try:
            subscription_args = {}
            if items:
                subscription_args["items"] = items
            if trial_days:
                subscription_args["trial_period_days"] = trial_days

            updated_subscription = stripe.Subscription.modify(
                subscription_id, **subscription_args
            )
            return updated_subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Error updating subscription: {str(e)}")
