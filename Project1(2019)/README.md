# Project 1

After a long time reading and looking for strategies for this project is finally done.
I did not put my 100% into making it look good because I want to learn better solutions for styling.
In the files, you will find application.py that has all the python code for this project. 
There is also the provided csv file and the requirements,txt(has the databse URL).
The import.py is a separate code I write to fill the heroku postgres database with the provided book list.
In the templates I will mention in order how the html files work:
Layout: all the other html follow this layout with some tweaks and styling.
Index-login screen, logout gets you here with a different message as well as bad login attempts.
Register- this is for user registration after registration is successfully complete it redirects to index with a success message
Search-after successful login user gets to this search( I used as an example the book Brida by Paulo Cohelo for testing.
Books- this is a list of links of the search results
Mybook- this is the unique page of a book with the comments.

The layout has a logout button so every template has a logout, register and home button.
