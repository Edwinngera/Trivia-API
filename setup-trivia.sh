# start postgres service
sudo service postgresql start

# setup and populate the testing database
pwd
su - postgres bash -c "psql < /home/edwin/trivia/Trivia-API/backend/setup-trivia.sql"
su - postgres bash -c "psql trivia < /home/edwin/trivia/Trivia-API/backend/trivia.psql"


# setup and populate the testing database
su - postgres bash -c "psql < /home/edwin/trivia/Trivia-API/backend/setup-test.sql"
su - postgres bash -c "psql trivia_test < /home/edwin/trivia/Trivia-API/backend/trivia.psql"
