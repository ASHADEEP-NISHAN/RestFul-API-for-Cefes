from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # dictionary={}
        # for column in self.__table__.columns:
        #     dictionary[column.name]=getattr(self,column.name)
        # return dictionary
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    record=db.session.execute(db.select(Cafe))
    all_cafes = record.scalars().all()
    random_cafe = random.choice(all_cafes)
    # return jsonify(cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    result=db.session.execute(db.select(Cafe))
    all_cafes=result.scalars().all()
    # cafe_list=[]
    # for cafe in all_cafes:
    #     cafe_list.append(cafe.to_dict())
    # return jsonify(cafes=cafe_list)
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    loc=request.args.get("loc")
    result=db.session.execute(db.select(Cafe).where(Cafe.location==loc))
    all_cafes=result.scalars().all()
    if all_cafes:
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}),404


@app.route("/add",methods=['POST'])
def add_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>",methods=["PATCH"])
def update_a_cafe_data(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price=request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}),200
    else:
        return jsonify(response={"error":"Sorry a cafe with that id was not found in the database."}),404


@app.route("/report-closed/<cafe_id>",methods=["DELETE"])
def delete_a_cafe(cafe_id):
    cafe=db.session.get(Cafe,cafe_id)
    api_key=request.args.get('api_key')
    if cafe:
        if api_key=="TopSecretAPIKey":
            cafe_to_delete=db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalar()
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the closed cafe from the database."}),200
        else:
            return jsonify(response={"error":"Sorry that's not allowed.Make sure you have the correct api_key."}),403
    else:
        return jsonify(response={"error":{"Not Found":"Sorry a cafe with that id not found in the database"}}),404



if __name__ == '__main__':
    app.run(debug=True)
