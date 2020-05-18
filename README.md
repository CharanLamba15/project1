# Project 1

Web Programming with Python and JavaScript

                                                                                Info about the Project:

This website is about books allows users to search about books, review them, and rate them. It also contains and api for books.

                                                                                Info about files:

styles.scss contains the styling for html pages.

access_denied.html shows the user that they don't have access to website unless they are logged in.

book.html shows the book details, allows the user to write the review, rate the book, and shows all the reviews.

error_register.html shows the user what error occured that didn't allow them to register.

error404.html tells the user the book is not in database.

home.html is the home page of the website it contains three search boxes foruser to search for books in the database.

index.html is log in page of the website.

layout.html is the layout for all the other html pages.

register.html allows user to register for the website.

results.html shows all the books found in the database based on the search results.

application.py does all the backend for the website such as access database, goodreads api, storing username, password, reviews, etc.

books.csv is used to import books data to the database.

import.py imports all the book data from books.csv to the database.

README.md tells info about the project and what each file contains.

requirements.txt contains all the libraries that are needed in order to run the program.

                                                                                Info needed in order for this program to run:

In order to run the program, two enviornment variables must be set first FLASK_APP=application.py and 
DATABASE_URL="postgres://xubkdvbrgqczzc:cb830299984265bf5c117c2fc106125fbb84dad19aa247c9f122f66eccacd9bc@ec2-54-80-184-43.compute-1.amazonaws.com:5432/dd3l7kd9dsmihl".