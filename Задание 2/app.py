from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, fields, marshal_with, Api
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '555e22fdfefe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cats_shop_user:4Tr0otuiQuU@db:5432/CatsShop'
db = SQLAlchemy(app)



admin = Admin(app, name='Админка', template_mode='bootstrap4', url='/admin')


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50))
    description = db.Column(db.String(200))
    age_months = db.Column(db.Integer)
    image = db.Column(db.String)

    def __repr__(self):
        return f'Cat {self.id}'



    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'description': self.description,
            'age_months': self.age_months,
            'image': self.image
        }



class CatModelView(ModelView):
    column_formatters_detail = ['id', 'name', 'breed', 'description', 'age_months']
    column_labels = dict(name='Название', breed='Порода', description='Описание', age_months='Возраст в месяцах')
    page_size = 5
    column_searchable_list = ['id', 'name', 'breed', 'description', 'age_months', 'image']
    column_sortable_list = ['id', 'name', 'breed', 'description', 'age_months', 'image']

    def render(self, template, **kwargs):
        if template == 'admin/model/edit.html':
            template = 'edit_cat.html'
        return super(CatModelView, self).render(template, **kwargs)

admin.add_view(CatModelView(Cat, db.session))


@app.route('/')
def index():
    cats = Cat.query.order_by(Cat.id).all()
    return render_template('index.html', cats=cats)

@app.route('/cat/<int:cat_id>')
def cat_detail(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    return render_template('cat_detail.html', cat=cat)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    sort_by = request.args.get('sort_by', 'relevance')

    cats_query = Cat.query

    numbers = re.findall(r'\d+', query)

    if numbers:
        age_query = int(numbers[0])
        cats_query = cats_query.filter(Cat.age_months == age_query)
    elif query:
        cats_query = cats_query.filter(or_(
            Cat.name.ilike(f'%{query}%'),
            Cat.breed.ilike(f'%{query}%'),
            Cat.description.ilike(f'%{query}%')
        ))

    if sort_by == 'name':
        cats_query = cats_query.order_by(Cat.name)
    elif sort_by == 'breed':
        cats_query = cats_query.order_by(Cat.breed)
    elif sort_by == 'age_months':
        cats_query = cats_query.order_by(Cat.age_months)
    elif sort_by == 'description':
        cats_query = cats_query.order_by(Cat.description)

    cats = cats_query.all()

    return render_template('index.html', query=query, sort_by=sort_by, cats=cats)


# ЧАСТЬ ДЛЯ РЕАЛИЗАЦИИ API


api = Api(app)

cat_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'breed': fields.String,
    'description': fields.String,
    'age_months': fields.Integer,
    'image': fields.String
}

class CatList(Resource):
    @marshal_with(cat_fields)
    def get(self):
        cats = Cat.query.all()
        return cats

class CatResource(Resource):
    @marshal_with(cat_fields)
    def get(self, cat_id):
        cat = Cat.query.get_or_404(cat_id)
        return cat

class CatSearch(Resource):
    @marshal_with(cat_fields)
    def get(self):
        query = request.args.get('query', '')
        sort_by = request.args.get('sort_by', 'name')
        cats_query = Cat.query

        numbers = re.findall(r'\d+', query)

        if numbers:
            age_query = int(numbers[0])
            cats_query = cats_query.filter(Cat.age_months == age_query)
        elif query:
            cats_query = cats_query.filter(or_(
                Cat.name.ilike(f'%{query}%'),
                Cat.breed.ilike(f'%{query}%'),
                Cat.description.ilike(f'%{query}%')
            ))

        if sort_by == 'name':
            cats_query = cats_query.order_by(Cat.name)
        elif sort_by == 'breed':
            cats_query = cats_query.order_by(Cat.breed)
        elif sort_by == 'age_months':
            cats_query = cats_query.order_by(Cat.age_months)
        elif sort_by == 'description':
            cats_query = cats_query.order_by(Cat.description)


        cats = cats_query.all()
        return cats

api.add_resource(CatList, '/api/cats')
api.add_resource(CatResource, '/api/cats/<int:cat_id>')
api.add_resource(CatSearch, '/api/cats/search')

# ---API---


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)