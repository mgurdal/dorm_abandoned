# coding: utf-8

from datetime import datetime

from dorm.database.drivers.mysql import Mysql
from dorm.database import models
from config import MYSQL_DATABASES



if __name__ == "__main__":
    md = Mysql(MYSQL_DATABASES[0])
    e1 = Employees(emp_no=300025,
                   birth_date=datetime.now(),
                   first_name="mehmet",
                   last_name="gurdal",
                   gender="M",
                   hire_date=datetime.now()
                  )
    #e1.save()
    # emps = Employees.select().all()
    emp_10005 = Employees.select().where("emp_no").like("10005").first()
    first_5_emp_of_first_db = Employees.select()[:5, :1]
    print(emp_10005)
    print(*first_5_emp_of_first_db)
