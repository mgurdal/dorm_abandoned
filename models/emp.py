from dorm.database import models

class Choice(models.Model):
    question = models.Integer()
    choice_text = models.Char(max_length=200)
    id = models.Integer()
    votes = models.Integer()

class Employees(models.Model):
    emp_no = models.Integer()
    birth_date = models.Date()
    first_name = models.Varchar(max_length=14)
    last_name = models.Varchar(max_length=16)
    gender = models.Text()
    hire_date = models.Date()
    
class Departments(models.Model):
    dept_no = models.Char(max_length=4)
    dept_name = models.Varchar(max_length=40)

class Dept_Emp(models.Model):
    emp_no = models.Integer()
    dept_no = models.Char(max_length=4)
    from_date = models.Date()
    to_date = models.Date()
    dept_emp_ibfk_1 = models.ForeignKey(Employees)
    dept_emp_ibfk_2 = models.ForeignKey(Departments)

class Dept_Manager(models.Model):
    emp_no = models.Integer()
    dept_no = models.Char(max_length=4)
    from_date = models.Date()
    to_date = models.Date()
    dept_manager_ibfk_1 = models.ForeignKey(Employees)
    dept_manager_ibfk_2 = models.ForeignKey(Departments)

class Question(models.Model):
    id = models.Integer()
    pub_date = models.Timestamp()
    question_text = models.Char(max_length=200)

class Salaries(models.Model):
    emp_no = models.Integer()
    salary = models.Integer()
    from_date = models.Date()
    to_date = models.Date()
    salaries_ibfk_1 = models.ForeignKey(Employees)

class Titles(models.Model):
    emp_no = models.Integer()
    title = models.Varchar(max_length=50)
    from_date = models.Date()
    to_date = models.Date()
    titles_ibfk_1 = models.ForeignKey(Employees)
