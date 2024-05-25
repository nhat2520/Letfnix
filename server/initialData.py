import random
import pandas as pd
import ast
from app.models import Movie, MovieCategory, Category
import uuid

# Thêm category
categories = [
    'Action',
    'Adventure', 
    'Animation',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Family',
    'Fantasy',
    'History',
    'Horror',
    'Music',
    'Mystery',
    'Romance', 
    'Science Fiction',
    'TV Movie',
    'Thriller',
    'War',
    'Western'
]

for category_name in categories:
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        category.save()
        print(f"Created new category: {category.name}")
    else:
        print(f"Category {category.name} already exists")

 


#add movie, moviecategory
df = pd.read_csv('data.csv')
genre_json = []
for i in df['genres']:
    i_json = ast.literal_eval(i)
    names = []
    for name in i_json:
        names.append(name['name'])
    genre_json.append(names)
df['genres'] = genre_json
for index, row in df.iterrows():
    # Tạo một đối tượng Movie mới
    price = round(random.uniform(10.00, 99.99), 2)
    movie = Movie(
        movie_id=uuid.uuid4(),
        name=row['title'],
        description=row['overview'],
        price=price,
        trailer_url=row['url'],
        vote_average=row['vote_average'],
        poster_path=row['poster_path'],
        backdrop_path=row['backdrop_path'],
        nation=row['origin_country'],
        run_time=row['runtime']
    )
    movie.save()

    for genre in row['genres']:
        category = Category.objects.get(name=genre)
        moviecategory = MovieCategory(
            movie = movie,
            category = category
        )
        moviecategory.save()
print()



