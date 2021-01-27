# Web-Series Recommendation with Review Sentiments

---

### Table of Contents
You're sections headers will be used to reference location of destination.

- [Demo](#demo)
- [Overview](#overview)
- [How To Use](#how-to-use)
- [Tool Used](#tool-used)
- [Author Info](#author-info)

---

### Demo

![GIF](./static/gif.gif)

---

### Overview

This application provides all the details of the requested web-series such as overview, genre, release date, rating,  top cast, reviews, recommended web-series, etc.

The details of the Web Series(title, genre,  rating, poster, etc) are fetched using an API by TMDB, https://www.themoviedb.org/documentation/api, and using the IMDB id of the web-series in the API, I did web scraping to get the reviews given by the user in the IMDB site using `beautifulsoup4` and performed sentiment analysis on those reviews.
Data Source :https://www.kaggle.com/amritvirsinghx/web-series-ultimate-edition

### How To Use

## How to get the API key?

Create an account in https://www.themoviedb.org/, click on the `API` link from the left hand sidebar in your account settings and fill all the details to apply for API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your `API` sidebar once your request is approved.

## How to run the project?

1. Clone this repository in your local system.
2. Install all the libraries mentioned in the [requirements.txt] file.
3. Replace YOUR_API_KEY in **both** the places (line no. 23 and 43) of `static/recommend.js` file.
4. Open your terminal/command prompt from your project directory and run the `main.py` file by executing the command `python main.py`.
5. Go to your browser and type `http://127.0.0.1:5000/` in the address bar.
6. Hurray! That's it.


### References
1.TMDB
2.Kaggle
3.Google
4.Stackoverflow

---

### Tool Used

![Python](https://img.shields.io/badge/Python-3.8-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Flask-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)
![API](https://img.shields.io/badge/API-TMDB-fcba03)


---

### Author's Info

- Twitter - [@taronic777](https://twitter.com/taronic777)
- linkedIn - [Tarun Yadav](https://www.linkedin.com/in/tarun-yadav-47442112b/)

[Back To The Top](#read-me-template)
