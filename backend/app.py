from models import db, Item, User

from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drug.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.secret_key = "drug-capstone-secret-key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Admin User"
ADMIN_ROLE = "Admin"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/create-db")
def create_db():
    db.create_all()
    return "Database created!"


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("index"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["username"] = username
            session["display_name"] = ADMIN_NAME
            session["role"] = ADMIN_ROLE
            flash("Login successful.", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password. Try admin / admin123.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@app.route("/index.html")
@app.route("/index")
@login_required
def index():

    items = Item.query.all()

    total_items = len(items)

    low_stock = 0

    for item in items:
        if item.quantity < 500:
            low_stock += 1

    dashboard_items = []

    for item in items:

        if item.quantity < 500:
            status = "Low Stock"
        else:
            status = "In Stock"

        dashboard_items.append({
            "id": item.item_code,
            "name": item.name,
            "category": item.category,
            "quantity": item.quantity,
            "status": status
        })

    stats = {
        "total_items": total_items,
        "low_stock": low_stock,
        "total_suppliers": 0,
        "total_transactions": 0
    }

    return render_template(
    "index.html",
    stats=stats,
    items=dashboard_items
)


@app.route("/categories")
@app.route("/categories.html")
@login_required
def categories():
    return render_template("categories.html")


@app.route("/items")
@app.route("/items.html")
@login_required
def items():
    items = Item.query.all()
    return render_template("items.html", items=items)





@app.route("/items/new", methods=["GET", "POST"])
@login_required
def new_item():
    if request.method == "POST":
        item = Item(
            item_code=request.form.get("item_code"),
            name=request.form.get("name"),
            generic_name=request.form.get("generic_name"),
            category=request.form.get("category"),
            form=request.form.get("form"),
            quantity=int(request.form.get("quantity")or 0),
            selling_price=float(request.form.get("selling_price")or 0),
            expiry_date=request.form.get("expiry_date")
        )

        db.session.add(item)
        db.session.commit()

        flash("Item added successfully!", "success")
        return redirect(url_for("items"))

    return render_template("new_items.html")

@app.route("/items/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_item(id):

    item = Item.query.get_or_404(id)

    if request.method == "POST":

        item.item_code = request.form.get("item_code")
        item.name = request.form.get("name")
        item.generic_name = request.form.get("generic_name")
        item.category = request.form.get("category")
        item.form = request.form.get("form")
        item.quantity = int(request.form.get("quantity") or 0)
        item.selling_price = float(request.form.get("selling_price") or 0)
        item.expiry_date = request.form.get("expiry_date")

        db.session.commit()

        flash("Item updated successfully!", "success")

        return redirect(url_for("items"))

    return render_template("new_items.html", item=item)

@app.route("/items/delete/<int:id>")
@login_required
def delete_item(id):

    item = Item.query.get_or_404(id)

    db.session.delete(item)

    db.session.commit()

    flash("Item deleted successfully!", "success")

    return redirect(url_for("items"))


@app.route("/suppliers")
@app.route("/suppliers.html")
@login_required
def suppliers():
    return render_template("suppliers.html")


@app.route("/transactions")
@app.route("/transactions.html")
@login_required
def transactions():
    return render_template("transactions.html")


@app.route("/users")
@app.route("/users.html")
@login_required
def users():
    users = User.query.all()

    last_user = User.query.order_by(User.id.desc()).first()

    if last_user:
        last_number = int(last_user.user_code.split("-")[1])
        new_user_code = f"USR-{last_number + 1:03d}"
    else:
        new_user_code = "USR-001"

    return render_template(
        "users.html",
        users=users,
        new_user_code=new_user_code
    )
@app.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):

    user = User.query.get_or_404(id)

    if request.method == "POST":

        user.full_name = request.form.get("full_name")
        user.email = request.form.get("email")
        user.password = request.form.get("password")
        user.role = request.form.get("role")
        user.department = request.form.get("department")
        user.status = request.form.get("status")

        db.session.commit()

        flash("User updated successfully!", "success")

        return redirect(url_for("users"))

    users = User.query.all()

    return render_template(
        "users.html",
        users=users,
        edit_user=user,
        new_user_code=user.user_code
    )
@app.route("/users/add", methods=["POST"])
@login_required
def add_user():


    user = User(
        user_code=request.form.get("user_code"),
        full_name=request.form.get("full_name"),
        email=request.form.get("email"),
        password=request.form.get("password"),
        role=request.form.get("role"),
        department=request.form.get("department"),
        status=request.form.get("status"),
        last_login="Never"
    )
    db.session.add(user)
    db.session.commit()

    flash("User added successfully!", "success")

    return redirect(url_for("users"))

@app.route("/users/delete/<int:id>")
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    flash("User deleted successfully!", "success")

    return redirect(url_for("users"))



@app.route("/audit-log")
@app.route("/auditlog.html")
@login_required
def audit_log():
    return render_template("audit_log.html")


@app.route("/export-data")
@app.route("/exportdata.html")
@login_required
def export_data():
    return render_template("exportdata.html")




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



