# python3
# Import Modules
from flask import Flask, render_template, request,\
               redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response

# Importing sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
# Importing db _setup from db_setup.py file
from db_setup import Base, User, Category, Items
import os
import random
import string
import httplib2
import json
import requests
# Import login_decorator from login_decorator.py file
from login_decorator import login_required


# Database
engine = create_engine("sqlite:///electronic.db",
                       connect_args={'check_same_thread': False},
                       echo=True)
Base.metadata.bind = engine
#  DBCreate Sessions
DBSession = sessionmaker(bind=engine)
session = DBSession()

category = session.query(Category).order_by(Category.name)
# Flask Instance
app = Flask(__name__)
app.secret_key = 'super_secret_key'


# google client secret
secret_file = json.loads(open('client_secrets.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']
APPLICATION_NAME = 'ItemCatlog'

# create Sessions
DBSession = sessionmaker(bind=engine)
session = DBSession()


# login routing
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# it helps the user to loggedin and display flash profile


# GoogleConnect
@app.route('/gconnect', methods=['POST', 'GET'])
def gConnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    request.get_data()
    code = request.data.decode('utf-8')

    # Obtain authorization code

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade
                                            the authorisation code"""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    my_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
              % access_token)
    header = httplib2.Http()
    result = json.loads(header.request(my_url, 'GET')[1].decode('utf-8'))

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is'
                                            'already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    login_session['name'] = data['name']
    login_session['img'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<center><h2>Welcome '
    output += login_session['name']
    output += '!</font></h1></center>'
    output += '<center><img src="'
    output += login_session['img']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    ' -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['name'])
    print('done..!')
    return output


# Create User in database
def createUser(login_session):
    name = login_session['name']
    email = login_session['email']
    url = login_session['img']
    newUser = User(user_name=name, user_email=email, user_picture=url)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(user_email=email).first()
    return user.id


# Getting UserInfornation
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Getting UserId
def getUserID(user_email):
    try:
        user = session.query(User).filter_by(user_email=email).one()
        return user.id
    except Exception as e:
        print(e)
        return None


# Googledisconnect
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user'
                                            'not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.

        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['name']
        del login_session['email']
        del login_session['img']
        response = redirect(url_for('showcategory'))
        response.headers['Content-Type'] = 'application/json'
        flash("successfully Logout", "success")
        return response
    else:

        # if given token is invalid, unable to revoke token
        response = make_response(json.dumps('Failed to revoke token for user'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# Display the Categories
@app.route('/')
@app.route('/category/')
def showcategory():
    category = session.query(Category).all()
    items = session.query(Items).all()
    return render_template('category.html',
                           categories=category,
                           items=items)


@app.route('/items/<int:item_id>', methods=["POST", "GET"])
def items(item_id):
    """
    this method displays details about the electronics which related to the id
    """
    category = session.query(Category).all()
    item = session.query(Items).get(item_id)
    return render_template('itemview.html',
                           item=item,
                           categories=category)


#  Show Category Items
@app.route('/category/<int:category_id>/items/')
def showcategories(category_id):
    category1 = session.query(Category).filter_by(id=category_id).one()
    category = session.query(Category).all()
    items = session.query(Items).filter_by(
            category_id=category_id).all()
    if len(items) == 0:
        datas = "NoData"
    else:
        datas = "Data"
    print(items)
    admin_1 = getUserInfo(category1.user_id)
    return render_template('publicitems.html',
                           category_id=category_id,
                           categories=category,
                           items=items,
                           datas=datas)


# Create New Category
@app.route('/category/addCategory', methods=['GET', 'POST'])
@login_required
def addCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('new Category is Successfully Created..!')
        return redirect(url_for('showcategory'))
    else:
        return render_template('addcategory.html', categories=category)


# Edit the Category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    editCategory = session.query(Category).filter_by(id=category_id).one()
    category = session.query(Category).filter_by(name=category_id).all()
    # See if user is  login
    admin_1 = getUserInfo(editCategory.user_id)
    user = getUserInfo(login_session['user_id'])
    if admin_1.id != login_session['user_id']:
        flash("You cannot edit this Category."
              "This Category belongs to %s" % admin_1.id)
        return redirect(url_for('showcategory'))
    # POST Methods
    if request.method == 'POST':
        if request.form['name']:
            editCategory.name = request.form['name']
            session.add(editCategory)
            session.commit()
            flash("category is successfully edited..!")
            return redirect(url_for('showcategory'))
    else:
        return render_template('editcategory.html',
                               category=editCategory,
                               categories=category)


# Delete the Category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    # See if the user is login
    admin_1 = getUserInfo(categoryToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if admin_1.id != login_session['user_id']:
        flash("You cannot delete this Category."
              "This Category belongs to %s" % admin_1.id)
        return redirect(url_for('showcategory'))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash('category is successfully deleted.!')
        return redirect(url_for('showcategory'))
    else:
        return render_template('deletecategory.html',
                               category=categoryToDelete,
                               categories=category)


# Add the Items
@app.route('/category/addItem/', methods=['GET', 'POST'])
@login_required
def addItem():
    category = session.query(Category).all()
    if request.method == 'POST':
        addItem = Items(
            brandname=request.form['brandname'],
            model=request.form['model'],
            image=request.form['image'],
            color=request.form['color'],
            price=request.form['price'],
            description=request.form['description'],
            userid=login_session['user_id'],
            category=session.query(
                Category).filter_by(name=request.form['category']).one()
        )
        session.add(addItem)
        session.commit()
        flash("Add new %s Item  is Successfully Created" % (addItem.brandname))
        return redirect(url_for('showcategory'))
    else:
        return render_template('additem.html', categories=category)


# Edit the Item
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    editItem = session.query(Items).filter_by(id=item_id).one()
    category = session.query(Category).all()
    admin_1 = getUserInfo(editItem.userid)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item user redirect them
    if admin_1.id != login_session['user_id']:
        flash("You cannot edit this item. "
              "This item belongs to %s" % admin_1.id)
        return redirect(url_for('showcategory'))
    # POST Methods
    if request.method == 'POST':
        if request.form['brandname']:
            editItem.brandname = request.form['brandname']
        if request.form['model']:
            editItem.model = request.form['model']
        if request.form['color']:
            editItem.color = request.form['color']
        if request.form['image']:
            editItem.image = request.form['image']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['description']:
            editItem.description = request.form['description']
            category = session.query(Category).filter_by(
                name=request.form['category']).one()
            editItem.category = category
        session.commit()
        flash("Item has been edited")
        return redirect(url_for('showcategory',
                                category_id=editItem.category.id))
    else:
        return render_template('edititem.html',
                               categories=category,
                               item=editItem)
# return str(category_id)+"items"+str(item_id)


# Delete  the Item
@app.route('/category/<int:category_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    category = session.query(Category).all()
    # See if the logged in user is the owner of the item
    admin_1 = getUserInfo(itemToDelete.userid)
    user = getUserInfo(login_session['user_id'])
    if admin_1.id != login_session['user_id']:
        flash("You cannot delete this item. "
              "This item belongs to %s" % admin_1.id)
        return redirect(url_for('showcategory'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('showcategories',
                                category_id=category_id))
    else:
        return render_template('deleteitem.html',
                               item=itemToDelete,
                               categories=category)

# JSON Endpoints


@app.route('/category/JSON')
def allItemsJSON():
    category = session.query(Category).all()
    category_dict = [b.serialize for b in category]
    for b in range(len(category_dict)):
        items = [j.serialize for j in session.query(
            Items).filter_by(category_id=category_dict[b]["id"]).all()]
        if items:
            category_dict[b]["Item"] = items
    return jsonify(Category=category_dict)


@app.route('/category/category/JSON')
def categoryJSON():
    category = session.query(Category).all()
    return jsonify(category=[b.serialize for b in category])


@app.route('/category/items/JSON')
def itemsJSON():
    items = session.query(Items).all()
    return jsonify(items=[j.serialize for j in items])


@app.route('/category/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category=category).all()
    return jsonify(items=[j.serialize for j in items])


@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def ItemJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Items).filter_by(
           id=item_id, category=category).one()
    return jsonify(item=[item.serialize])


# !Important! Always block should be last ! Important!
if __name__ == '__main__':
    app.secret_key = 'APP_SECRET_KEY'
    app.debug = True
    app.run(host='', port=5000)
