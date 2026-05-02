from models import db, Item

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
    return render_template("index.html")


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
            quantity=int(request.form.get("quantity")or 0),

            selling_price=float(request.form.get("selling_price")or 0),
            expiry_date=request.form.get("expiry_date")
        )

        db.session.add(item)
        db.session.commit()

        flash("Item added successfully!", "success")
        return redirect(url_for("items"))

    return render_template("new_items.html")


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
    return render_template("users.html")


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




