from flask import Flask, render_template, request
import pickle
import pandas as pd 
import numpy as np 
 
popular_df = pickle.load(open('./models/popular.pkl', 'rb'))
pt = pickle.load(open('./models/pt.pkl', 'rb'))
backup = pickle.load(open('./models/backup.pkl', 'rb'))
similarity_score = pickle.load(open('./models/similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend_books', methods=["GET", "POST"])
def recommend():
    error_message = None  # To store the error message
    index = None  # To store the index if found

    if request.method == "POST":
        user_input = request.form.get("user_input")  # Get user input from form

        if not user_input:
            error_message = "Input cannot be empty."
            return render_template("index.html", error_message=error_message)

        try:
            user_input_lower = user_input.lower()
            # Find the index if user_input exists in pt.index
            index_match = np.where(pt.index.str.lower() == user_input_lower)[0]
            if index_match.size == 0:
                raise ValueError(f"No matching data found for '{user_input}'.")
            index = index_match[0]  # Get the first matched index
        except ValueError as e:
            # Stop execution and send error to the frontend
            error_message = str(e)
            return render_template("index.html", error_message=error_message)


    # index =  np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:7]
    data = []
    for i in similar_item:
        item = []
        temp_df = backup[backup['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['avg-rating'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))

        data.append(item)

    return render_template('index.html',error_message=error_message, data=data, index=index)

@app.route('/trending')
def trending():
    return render_template('trending.html',
                           name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-L'].values),
                           votes = list(popular_df['num-rating'].values),
                           rating = list(popular_df['avg-rating'].values),
                           year = list(popular_df['Year-Of-Publication'].values)
                           )


if __name__ == '__main__':
    app.run(debug=True)
