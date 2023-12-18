from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from myapp.models import interaction, Users, Item  # Adjusted import statement
from .forms import createRequestForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

idcount = 1
def get_recommendations(user_profile):
    # Get all users and items
    all_users = list(Users.objects.all())
    all_items = list(Item.objects.all())
    l = []
    k = []
    for i in all_users:
        l.append(i.name)
    for i in all_items:
        k.append(i.title)
    # Create a user-item matrix
    user_item_matrix = np.zeros((len(all_users), len(all_items)))

    # Fill in the matrix with user interactions
    for i in interaction.objects.all():
        user_index = l.index(i.user.name)
        item_index = k.index(i.item.title)
        user_item_matrix[user_index, item_index] = 1
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(user_item_matrix, user_item_matrix)

    # Get the user's index
    user_index = l.index(user_profile)
    # Get similarity scores for all users
    user_similarity_scores = similarity_matrix[user_index]

    # Find users with high similarity scores
    similar_users_indices = np.argsort(user_similarity_scores)[::-1]

    # Get items that similar users liked but the current user hasn't interacted with
    recommendations = []
    for i in similar_users_indices:
        if i != user_index:  # Exclude the current user
            for item_index in range(len(k)):
                if user_item_matrix[i, item_index] == 1 and user_item_matrix[user_index, item_index] == 0:
                    recommendations.append(k[item_index])

    return list(set(recommendations))

def home(request, c_id = 0):
    # user : puneeth pass: 123
    if request.user.is_anonymous:
        return redirect('/login')
    #all 
    cat = categories.objects.all()
    if c_id == 0 :
        p = Item.objects.exclude(category_id = c_id)
    # if c_id == 3:
    #     order_history_data = orderdetails.objects.all()

    #     oh_list = []
    #     for i in order_history_data:
    #         oh_list.append([i.item.item_id,i.orders.user.id,i.item.category,i.item.description])

    #     # Convert data to a pandas DataFrame
    #     order_history_df = pd.DataFrame.from_records(oh_list)
    #     order_history_df.columns = ['item_id','user_id','category','description']
    #     # Fetch data from the Item model
    #     item_data = Item.objects.all()
    #     it_list = []

    #     for i in item_data:
    #         it_list.append([i.item_id,i.description,i.category])
    #     # Convert data to a pandas DataFrame
    #     item_df = pd.DataFrame.from_records(it_list)
    #     item_df.columns = ['item_id','description','category']
    #     print(order_history_df,item_df)
    #     # Merge order history with item descriptions
    #     merged_df = pd.merge(order_history_df, item_df, on='item_id', how='inner')
    #     print(merged_df.columns,'test')
    #     # Choose a category for recommendation
    #     target_category = 3

    #     # Filter items in the target category
    #     target_category_items = item_df[item_df['item_id'] == target_category]

    #     # Create TF-IDF vectors for item descriptions
    #     vectorizer = TfidfVectorizer(stop_words='english')
    #     description_matrix = vectorizer.fit_transform(merged_df['description_x'].fillna(''))

    #     # Create TF-IDF vectors for target category items
    #     target_category_matrix = vectorizer.transform(target_category_items['description'].fillna(''))

    #     # Calculate similarity between order history descriptions and target category items
    #     similarity_scores = linear_kernel(description_matrix, target_category_matrix)

    #     # Get the most similar items
    #     similar_items_indices = similarity_scores.argmax(axis=1)
    #     recommended_items = target_category_items.iloc[similar_items_indices]

    #     # Remove items already in the user's order history
    #     recommended_items = recommended_items[~recommended_items['item_id'].isin(order_history_df['item_id'])]

    #     # Display or return recommended items
    #     print(recommended_items,'rec items for clothes')
    #     p = recommended_items
    else:
        p = Item.objects.filter(category_id = c_id)
    #recommended products
    user_id = request.user# Fetch from the page
    
    recommendations  = get_recommendations(request.user.username)
    checkobs = checkout.objects.filter(user_id = request.user.id)
    leng = 0
    for i in checkobs:
        leng += i.qty
    u = Users.objects.filter(user_id = request.user.id).first()
    c = u.coins
    return render(request, 'index.html',context = {'catlist' : cat, 
                                                   'plist' : p,
                                                   "recoms" : recommendations , 'l' : leng ,'c' : c} )

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home/0')
        else:
            print('user not found')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')


def checkoutfun(request):
    checkobs = checkout.objects.all()
    suma = 0 
    for i in checkobs:
        if i.user == request.user:
            suma += i.item.price
    checkobs = checkout.objects.filter(user_id = request.user.id)
    leng = 0
    for i in checkobs:
        leng += i.qty
    u = Users.objects.filter(user_id = request.user.id).first()
    c = u.coins
    disc = 0
    if suma > 100:
        disc = min(50,c)
    return render(request, 'checkout.html', context = {"checkobs" : checkobs , 'totalsum' : suma , 'l' : leng , 'c' : c , 'disc' : disc})

def contact(request):
    return render(request, 'contact.html')

def addToCart(request, item):
    i = Item.objects.filter(item_id = item).first()
    check = checkout.objects.filter(user = request.user , item = i).first()
    if check:
        check.qty += 1
        check.save()
    else:
        ck = checkout(user = request.user , item = i , qty = 1)
        ck.save()
    return redirect('/home/0')

def placeOrder(request):
    checkobs = checkout.objects.filter(user = request.user)
    if(len(checkobs)!=0):
        suma = 0
        global idcount
        newOrder = orders(user = request.user , order_id = idcount)
        idcount += 1
        newOrder.save()
        for i in checkobs:
            od = orderdetails(orders = newOrder, item = i.item)
            suma += i.item.price*i.qty
            od.save()
        checkobs.delete()
        u = Users.objects.filter(user_id = request.user.id).first()
        u.coins += int(suma*(0.1))
        u.save()
        c = u.coins
        disc = 0
        if suma > 100:
            disc = min(50,c)
            u.coins -= disc
            u.save()
    return redirect('/home/0')

def addrequest(request):
    if request.method == "POST":
        form = createRequestForm(request.POST)
        if form.is_valid():
            productname = request.POST['productname']
            productdesc = request.POST['description']
            p = productsrequests(productname=productname,description=productdesc)
            p.save()
            return redirect('/home/0')
    else:
        form = createRequestForm()
    return render(request,'requestsform.html',context={'form' : form})

