from flask import Flask, render_template, request, redirect
from config import Config
from models import db,URL
import random
import string
from sqlalchemy import or_
from sqlalchemy import func
from datetime import date
import qrcode
import os
from flask import flash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(length))

def generate_qr(short_url, short_code):

    qr = qrcode.make(short_url)

    path = os.path.join("static", "qr", f"{short_code}.png")

    qr.save(path)

@app.route("/dashboard")
def dashboard():

    total_urls = URL.query.count()

    total_clicks = db.session.query(
        func.sum(URL.clicks)
    ).scalar() or 0

    today_urls = URL.query.filter(
        func.date(URL.created_at) == date.today()
    ).count()

    recent_urls = URL.query.order_by(
        URL.created_at.desc()
    ).limit(5).all()

    most_clicked = URL.query.order_by(
        URL.clicks.desc()
    ).first()

    return render_template(
        "dashboard.html",
        total_urls=total_urls,
        total_clicks=total_clicks,
        today_urls=today_urls,
        recent_urls=recent_urls,
        most_clicked=most_clicked
    )

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        original_url = request.form["original_url"]
        custom_code = request.form["custom_code"].strip()

        existing_url = URL.query.filter_by(original_url=original_url).first()

        if existing_url:
            return render_template(
            "index.html",
            error="This URL has already been shortened!",
            existing_short_url=request.host_url + existing_url.short_code
        )

        if custom_code:

            existing = URL.query.filter_by(short_code=custom_code).first()

            if existing:
               return "This Short URL already exists."

            short_code = custom_code

        else:

           while True:

              short_code = generate_short_code()

              existing = URL.query.filter_by(short_code=short_code).first()

              if not existing:
                break

        new_url = URL(
            original_url=original_url,
            short_code=short_code
        )

        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_code

        generate_qr(short_url, short_code)  

        return render_template(
            "result.html",
            original_url=original_url,
            short_url=short_url,
            qr_image=f"/static/qr/{short_code}.png"
         )

    return render_template("index.html")

@app.route("/<short_code>")
def redirect_url(short_code):

    url = URL.query.filter_by(short_code=short_code).first()

    if url:

     
        url.clicks += 1

        db.session.commit()

        return redirect(url.original_url)

    return render_template("404.html"), 404

@app.route("/history")
def history():

    search = request.args.get("search")

    if search:

        urls = URL.query.filter(

            or_(

                URL.original_url.ilike(f"%{search}%"),

                URL.short_code.ilike(f"%{search}%")

            )

        ).order_by(URL.created_at.desc()).all()

    else:

        urls = URL.query.order_by(URL.created_at.desc()).all()

    return render_template(
        "history.html",
        urls=urls,
        search=search
    )

@app.route("/delete/<int:id>")
def delete_url(id):

    url = URL.query.get_or_404(id)

 
    qr_path = os.path.join("static", "qr", f"{url.short_code}.png")

  
    if os.path.exists(qr_path):
        os.remove(qr_path)

   
    db.session.delete(url)
    db.session.commit()

    flash("URL deleted successfully!", "success")

    return redirect("/history")

@app.errorhandler(404)
def page_not_found(e):

    return render_template("404.html"), 404

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)


    # http://127.0.0.1:5000/