import stripe


def create_stripe_product(name):
    """Создает продукт в Stripe."""
    return stripe.Product.create(name=name)


def create_stripe_price(product_id, amount):
    """Создает цену в Stripe."""
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # в копейках
        currency="rub",
    )


def create_stripe_session(price_id):
    """Создает сессию оплаты в Stripe."""
    return stripe.checkout.Session.create(
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
