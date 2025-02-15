# Bungalow Take Home Project for Data Engineer Role (V2. 2021-11-02)

Welcome to the Bungalow Takehome Challenge for Data Engineering! This is a barebones repo to get you started.

## What to build
A common task for data engineers at Bungalow involves the integration of the of third-party data, modelling data, storing it and making it available for downstream teams such as analytics, data science and ultimately the entire organization.
For this challenge we'd like to give a brief snapshot of a common workload may entail. Of course, this might become a big task. Therefore, to save time for you, we did some of the heavy lifting, like the set up and some scaffolding of the environment.

For this test we will collect the [current weather data](https://openweathermap.org/current) from [OpenWeatherMap](https://openweathermap.org/). The free API will work for this assignment. You shouldn’t pay for the API.

Please install [Docker Desktop](https://www.docker.com/get-started) on your laptop. It will contain the environment that we would need for the next steps.

The Docker compose would have two software applications and simple setup required for them.

- Airflow: To run your additions to the boilerplate DAGs.

- Postgres: To maintain your tables. (You can swap it with any other database or your choice, i.e. SQLite, MySQL)


Below are the steps in the data flow diagram:

- fetcher.py script, that represents the fetcher DAG, would retrieve the data from the current weather API.

- The fetcher script would process and clean the data, then stores it the Postgres database considering relationships, integrity, performance, and extendability.

- The transformer.py script, that represents the Transformer DAG, would transform the data from the previous step to prepare some derived dataset tables. You will have the choice to implement the transformations both in Python or SQL.

- The Transformer writes the datasets back to Postgres.

- The downstream customer(s) would read both original and derived tables. They will execute historical queries to run analytics and science models.


This project is meant to be flexible as to showcase your decision making capabilities and your overall technical experience. 

**Note:** If you are uncomfortable with Docker, Postgres or Airflow, please feel free to remove or replace them. They are meant to save time for you. As long as you can achieve the outcome feel free to use any additional tooling, programming language (i.e. Java or Scala) and approach you see fit. We will ask follow up questions about your decision mechanism in the follow up conversation.

We are more interested in seeing your thought process and approach to solving the problem!

##  Deliverables
We will expect to see the following items in your Github pull request:

- Your Python code for data fetcher and transformer.

- The data model SQL and your design for its data modelling

- Readme file with your notes

## Evaluation
We will use this project as our basis for our evaluation of your overall fit for a data engineering role from a technical viewpoint.

To do this, we will review your code with an eye for the following:

- Readability, scalability and usability

- Data processing and relational modelling

- Python and SQL know-how

## Time expectations
We know you are busy and likely have other commitments in your life, so we don't want to take too much of your time. We don't expect you to spend more than 2 hours working on this project. That being said, if you choose to put more or less time into it for whatever reason, that is your choice.

Feel free to indicate in your notes below if you worked on this for a different amount of time and we will keep that in mind while evaluating the project. You can also provide us with additional context if you would like to.

Additionally, we have left a spot below for you to note. If you have ideas for pieces that you would have done differently or additional things you would have implemented if you had more time, you can indicate those in your notes below as well, and we will use those as part of the evaluation.

## Public forks
We encourage you to try this project without looking at the solutions others may have posted. This will give the most honest representation of your abilities and skills. However, we also recognize that day-to-day programming often involves looking at solutions others have provided and iterating on them. Being able to pick out the best parts and truly understand them well enough to make good choices about what to copy and what to pass on by is a skill in and of itself. As such, if you do end up referencing someone else's work and building upon it, we ask that you note that as a comment. Provide a link to the source so we can see the original work and any modifications that you chose to make.

## Challenge instructions
Fork this repository and clone to your local environment

- Prepare your environment with Python and any other tools you may need. Docker can do it for you.
  - To run the docker-compose, you need to run the following commands:
      ```shell
      # Initializing the folders and the non-root user for Airflow
      mkdir -p  ./logs ./plugins
      echo -e "AIRFLOW_UID=$(id -u)" > .env
      # Initializing airflow database
      docker-compose up airflow-init
      # Running the docker-compose
      docker-compose up 
      # You can see the Airflow UI in http://localhost:8080 with username/password: airflow
      ```
  - If you run to any problems with the environment, please refer to [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).
- Fill in the TODO in the repository. There are currently 6 TODOS, but you can go beyond and above.
  - Any problems with the DAGs? They are taken from [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html). Please take a look at the rest of tutorial if needed.
  - You can check Postgres operator from [here](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html)
  - To keep it simple, let's use the Airflow database for the storage of your dataset
- Write down the notes, in the Readme.md file.
- Complete the challenge and push back to the repo
  - If you have any questions in any step, please reach out to your recruiter. A member of engineering team will be involved to support you, as if you were working for Bungalow.
- **Note:** If you are using Apple hardware with M1 processor, there is a common challenge with Docker. You can read more about it [here](https://javascript.plainenglish.io/which-docker-images-can-you-use-on-the-mac-m1-daba6bbc2dc5).

## Your notes (Readme.md) 

1. `fetcher dag` inserts data into the `raw_current_weather` table in a very raw format: the entire json returned. An `id` field was created to identify unique rows and a `ingestion_timestamp` field to keep track of when this data was inserted into the table.
2. `tranformer dag` get all ids that are missing transformation from `raw_current_weather` and inserts them into `current_weather` and `current_weather_conditions` tables. All json fields are unested and tranformed into columns. A field called `etl_timestamp_utc` is added to the new tables to track when the tranformation ocurred. 
3. `current_weather_conditions` represents the weather list return from the API, as it is a list the best way to represent it was a separate table from `current_weather`.

### Time spent

Around 1:40.
I took some time to install Docker and configure WSL2 (I need to do this on an old Windows laptop I have that was not prepared for development :) )


### Assumptions

* Assumed that we only want to collect data from one city.
* For this challanged I assumed that there was no problem in using the existing airflow database to my tables, in a real world scenario that would not be wise.
* I assumed that the list attribute would be better unested in another table to facilitate joins, so the SQLs used to explore it could be more "standard". Depending on the situation, the main users of this data would be familiar enough with json operators/functins and that would not be needed (and dependending on the access pattern even beneficial to avoid a join).
* Each transformer dag execution should try to transform all missing data, making the executions to not be idempontent.

### Next steps

* On the table current_weather_conditions I would try to create a column with the index and keep it there. 
* Create a bigger/diverse dataset to validate my SQLs, it may have hidden bugs that will appear in a more diverse dataset.
* Create a table with the summarized view of the weather in a location groupbed by day.
* Add a foreign key in `current_weather_conditions` table to guarantee referencial integrity.
* Validate the performance of the left join used to determine which data still need to be tranformed. Maybe some flag column in the raw table could help to avoid the join by allowing a direct filter by it.

### Instructions to the evaluator
Provide any end user documentation you think is necessary and useful here