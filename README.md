# HealthCare_App

This Project was created for my CS125 project class. It was built for healthcare data management.

## Author

* [Zhiyuan Du](https://github.com/lYesterdaYl)
* [Yuming Fu](https://github.com/yumi519)
* [Zhicong Zhong](https://github.com/zhicz)
* [Yuhan Yao](https://github.com/yyhtudou)

## Built With

* [MySQL](https://www.mysql.com/) - Used to store the data.
* [Flask](http://flask.pocoo.org/) - Used to construct server side code.

## How it works(Database)
* Comments inside the source code
* Stores data and process data through recommendation
* Communicate with UI
## How it works(Recommendation System)
* First of all, the recommendation system filter the items with a context filter and a personal filter. The context filter matches the health state of user with items that are indexed in the database. The personal filter removes the items that are not in the category of user interest.
* Secondly, the recommendation engine construct a user-item ratings matrix, decomposite it into the user embedding matrix and item embedding matrix. We define the loss function as mean square loss of ground truth rating and predicted rating, and optimize our model by stochastic gradient descent. This machine learning model is called collaborative filtering.
* Finally, we predict the rating of all item given our user, rank the item based on predicted rating scores, and recommend the best rated one to user.

## How it works(Android Java UI)
* User begin with sign in activity, able to sign up or sign in
  * Sign in will require confirmation with API connected database to match username and password
  * Sign up will add new user(username and password along with user info at registration) onto databse
* If user chooses to sign up
  * New user data sent to database, complete basic survey for personal modeling purposes
* If user chooses to sign in
  * Match username and password in database
  * First sign in of the day will require user to complete a daily survey for recommendation and health state determination
* In basic survey activity
  * User will complete 21 questions for personal model and preference
  * Data will be recorded in database(survey score and preference)
* In dashboard activity
  * Display user's step count and happiness index(health state)
  * Daily survey will be available if user have not taken survey yet
  * Display user's health state based on daily survey results
* In survey activity
  * Daily survey is composed of 6 questions
  * Upon completion will trigger recommendation for user (video or music)
  * New data will be recorded in database(survey score)
* In recommendation activity
  * User will receive recommendation and asked to rate recommendation for Recommendation System improvement and collaborative filtering
  * New data will be recorded in database(recommendation rating)
