## Architecture

## Workflow
1) user defines the databases via panel or config file
    1) Simple and fluid design
    2) Easy to set up
    3) Can work with known visualization and CI tools
2) dorm creates drivers based on conf
    1) Tests connection strength
    2) Gathers meta data from databases
3) drivers discovers databases based on conf
    1) Discovers the tables, columns and relations
    2) Detects manytomany relations 
    3) Generates model code from database information
4) drivers generates models and inserts itself to the models as conf
    1) Driver analyzes the models and generates model instances
    2) With a tinydb or reducer solution models can easly be found
    3) 
5) models 

## Create Models
```python
from datetime import datetime
from database.drivers import Sqlite
from database import models

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()
```

## Make Queries
```python
# Create the database file (also opens the transaction)
with Sqlite("poll.db") as db:
        try:
            db.create_table(Question)
            db.create_table(Choice)
        except Exception:
            pass
        
        # insert some data
        question = Question(question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice_1 = Choice(question=question.id, choice_text="red", votes=0)
        choice_2 = Choice(question=question.id, choice_text="blue", votes=0)
        choice_1.save()
        choice_2.save()

# read from database
with Sqlite("poll.db") as db:
    first_question = Question.select().where(id=1).first()
    red_choices = Choice.select().where(choice_text="red").all()

    # Get first 5 results from all databases
    first_5_choices = Choice.select()[:5]

    # Get first 5 results from first 5 databases
    first_5_choices_dbs = Choice.select()[:5, :5]

    # Get results as pandas.DataFrame
    all_choices_as_df = Choice.select().as_df()
```
## Multiple Database Connection & Parallel Processing
```python
with ExitStack() as stack:
    [stack.enter_context(Sqlite(db['address'])) for db in DATABASES]
    # get dask distributed dataframe
    ddf = Choice.select().as_distributed_df()
    result = ddf.votes.value_counts().compute()
    most_common_10_votes = result.sort_values()[-10:]
    print(most_common_10_votes)
```

## RESTful Service

```python
from datetime import datetime
from database import models
from services.restful import rest, app

# accessible with host:port/question or host:port/question/id
@rest()
class Question(models.Model):
    id = models.PrimaryKey()
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

# restrict http methods
@rest(without=["post", "delete", "patch"])
class Choice(models.Model):
    id = models.PrimaryKey()
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

if __name__ == "__main__":
    app.run()
```


## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (Mozilla Public License 2.0).
