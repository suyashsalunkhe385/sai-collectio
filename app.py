from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import random

app = Flask(__name__)
app.secret_key = "sai_collection_super_secret_key"

# In-memory product catalog
PRODUCTS = [
    {
        "id": 1,
        "name": "Heavyweight Oversized Hoodie",
        "category": "Hoodies",
        "price": 1799,
        "original_price": 2499,
        "rating": 4.8,
        "reviews_count": 142,
        "image": "Hoodie.png",
        "badge": "Bestseller",
        "description": "500 GSM French terry cotton with relaxed dropped shoulders and double-layered hood."
    },
    {
        "id": 2,
        "name": "Urban Tech Bomber Jacket",
        "category": "Outerwear",
        "price": 2999,
        "original_price": 4199,
        "rating": 4.9,
        "reviews_count": 98,
        "image": "Jacket.png",
        "badge": "Trending",
        "description": "Water-resistant satin exterior with windproof ribbing and deep utility pockets."
    },
    {
        "id": 3,
        "name": "Classic Relaxed Fit Denim",
        "category": "Jeans",
        "price": 2199,
        "original_price": 2999,
        "rating": 4.7,
        "reviews_count": 210,
        "image": "Jeans.png",
        "badge": "Popular",
        "description": "100% durable raw washed cotton featuring traditional 5-pocket construction."
    },
    {
        "id": 4,
        "name": "Structured Minimalist Shirt",
        "category": "Shirts",
        "price": 1499,
        "original_price": 1999,
        "rating": 4.6,
        "reviews_count": 64,
        "image": "Shirt.png",
        "badge": "New Arrival",
        "description": "Breathable linen-cotton blend with tailored button-down cuffs and curved hemline."
    },
    {
        "id": 5,
        "name": "Essential Boxy Cut T-Shirt",
        "category": "T-Shirts",
        "price": 899,
        "original_price": 1299,
        "rating": 4.9,
        "reviews_count": 340,
        "image": "T-shirt.png",
        "badge": "Must Have",
        "description": "240 GSM pre-shrunk combed cotton designed with seamless ribbing and boxy silhouette."
    }
]

@app.before_request
def ensure_cart():
    if "cart" not in session:
        session["cart"] = []

@app.context_processor
def inject_cart_count():
    total_qty = sum(item.get("qty", 1) for item in session.get("cart", []))
    return {"cart_item_count": total_qty}

@app.route("/")
def index():
    featured = PRODUCTS[:3]
    return render_template("index.html", products=featured)

@app.route("/products")
def products():
    category = request.args.get("category")
    if category and category.lower() != "all":
        items = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
    else:
        items = PRODUCTS
    return render_template("products.html", products=items, current_cat=category or "all")

@app.route("/add-to-cart/<int:prod_id>", methods=["POST"])
def add_to_cart(prod_id):
    product = next((p for p in PRODUCTS if p["id"] == prod_id), None)
    if product:
        cart = session.get("cart", [])
        for item in cart:
            if item["id"] == prod_id:
                item["qty"] += 1
                break
        else:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "original_price": product["original_price"],
                "image": product["image"],
                "qty": 1
            })
        session["cart"] = cart
        session.modified = True
        flash(f"Added {product['name']} to your bag!", "success")
    return redirect(request.referrer or url_for("products"))

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    subtotal = sum(i["price"] * i["qty"] for i in cart_items)
    discount = sum((i["original_price"] - i["price"]) * i["qty"] for i in cart_items)
    shipping = 0 if subtotal >= 1999 or subtotal == 0 else 149
    tax = round(subtotal * 0.12)
    grand_total = subtotal + shipping + tax
    
    return render_template(
        "cart.html",
        cart=cart_items,
        subtotal=subtotal,
        discount=discount,
        shipping=shipping,
        tax=tax,
        grand_total=grand_total
    )

@app.route("/update-cart/<int:prod_id>/<action>")
def update_cart(prod_id, action):
    cart = session.get("cart", [])
    for item in cart:
        if item["id"] == prod_id:
            if action == "increase":
                item["qty"] += 1
            elif action == "decrease":
                item["qty"] -= 1
                if item["qty"] <= 0:
                    cart.remove(item)
            elif action == "remove":
                cart.remove(item)
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/track", methods=["GET", "POST"])
def track():
    order_info = None
    if request.method == "POST":
        order_id = request.form.get("order_id", "").strip().upper()
        if order_id:
            order_info = {
                "order_id": order_id,
                "status": "In Transit",
                "estimated_delivery": "Within 2 - 3 business days",
                "carrier": "BlueDart Express",
                "current_location": "Central Hub, Pune",
                "steps": [
                    {"label": "Order Confirmed", "date": "Yesterday, 4:20 PM", "done": True},
                    {"label": "Shipped from Warehouse", "date": "Today, 09:15 AM", "done": True},
                    {"label": "In Transit to Destination", "date": "Active Now", "done": True, "active": True},
                    {"label": "Out for Delivery", "date": "Pending", "done": False},
                    {"label": "Delivered", "date": "Estimated Oct 2", "done": False}
                ]
            }
        else:
            flash("Please enter a valid Order ID.", "danger")
    return render_template("track.html", order=order_info)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thank you! Your message has been routed to our customer support team.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)