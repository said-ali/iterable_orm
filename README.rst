Iterable_orm
============

.. image:: https://img.shields.io/pypi/v/iterable_orm.svg
    :target: https://pypi.python.org/pypi/iterable_orm
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/Said007/iterable_orm.svg?branch=master
   :target: https://travis-ci.org/Said007/iterable_orm
   :alt: Latest Travis CI build status


Iterable_orm allows you to filter, exclude and sort data using similer API provided by Django ORM. The data needs to be a list of objects or dictionary. Python 2 & 3 is supported.

Iterable_orm gives you the following API

filter - Returns a new list of objects or dictionaries that match the given lookup parameters

exclude - Returns a new list of objects or dictionaries that do not match the given lookup parameters

get - Returns a single object or dictionary if there's two matches returns an exception 

order_by - Returns a list ordered objects or dictionaries

first - Returns the first object or dictionary of filtered or exlcude data

last - Returns the first object or dictionary of filtered or exlcude data

count - Returns a lenth of filtered or exlcude or dictionaries

*Please note that Iterable_orm does not support Q like objects offered by Django ORM, but offers a way around by passing anonymous function to filter or exclude function e.g manager.filter(age=lambda x: x >= 20 and x <= 30)*


Basic Usage
-----------

Pass a list of objects or dictionary to Queryset

.. code:: python

    from iterable_orm import QuerySet
    Accounts = [ A list of account objects that have attrubtes such as name, email, age, gender ect ]
    manager = Queryset(Accounts)


Filtering and Excluding
-----------------------

You can filter and exclude data by value or lookups, such as gt, gte, lt, lte, startswith, istartswith, endswith, contains, icontains, value_in, value_not_in, value_range, date_range(expects a datetime object) or anonymous function.

iterable_orm also allows you to filter related objects using the standard double-underscore notation to separate related fields, e.g manager.filter(parent__name='John'), this filters by parent.child == 'John'.

All filtering and exlcuding are lazy so you can construct as many filtering as you like and its only evaluated on iterating, calling count, first, last and order_by. 

Below are code examples of filtering and excluding, 

.. code:: python

    from iterable_orm import QuerySet
    Accounts = [A list of account objects that have attrubtes such as name, email, age, gender ect ]
    manager = Queryset(Accounts)

    # Filter accounts with age greater than 25 and exclude if gender is male
    data = manager.filter(age__gt=20).exclude(gender='male')
    
    # Filter using lamda  
    data = manager.filter(age=lambda x: x >= 20 and x <= 30).exclude(gender='male')

    # Filter accounts with the name starting with letter 's' and gender is female
    data = manager.filter(name__istartswith='s').exclude(gender='female')
    
   # Filter accounts who have registred from 2014 till 2016 of current date and who are a female
    data = manager.filter(registered__date_range=(datetime.today().replace(year=2014), datetime.today().replace(year=2016))).exclude(gender='female')

   # Filter accounts who have registred from 01-01-2015 till 2016 and who are a female if date is string object
    data = manager.filter(registered__date_range=('01-01-2015', '01-01-2016')).exclude(gender='female')


Filtering
---------

You can filter data by value or lookups, such as gt, gte ect.

Below are code examples of filtering, 

.. code:: python

    from iterable_orm import QuerySet
    Accounts = [A list of account objects that have attrubtes such as name, email, age, gender ect ]
    manager = Queryset(Accounts)

    # Filter accounts with age greater that 25 
    data = manager.filter(age__gt=20)

    # Filter accounts with age less that 25 and who are a male
    data = manager.filter(age__lt=20, gender='male')

    # Get number of accounts with age 20 and who are a female
    data = manager.filter(age__gt=20, gender='female').count()
    
    # Filter accounts with name starting with letter 's'
    data = manager.filter(name__istartswith='s')
    
   # Filter accounts who have registred from 01-01-2015 till 2016
    data = manager.filter(registered__date_range=('01-01-2015', '01-01-2016')) 
    
   # Filter accounts who have friends who are a male
    data = manager.filter(friends__gender='male')
    
   # Filter accounts with date range
    data = manager.filter(registered__value_range=('2015-11-15', '2015-11-16')

   # chain filter e.g
    data = manager.filter(name__istartswith='s').filter(gender='male')


Excluding
---------

You can Exclude data by value or lookups such as gt, gte ect.
Below are code examples of exlcude function:

.. code:: python

    from iterable_orm import QuerySet
    Accounts = [A list of account objects that have attrubtes such as name, email, age, gender ect ]
    manager = Queryset(Accounts)

    # Exclude accounts with age greater that 25
    data = manager.exclude(age__gt=20)

    # Exclude accounts with age less then 25 and who are a male
    data = manager.exclude(age__lt=20, gender='male')

    # Exclude accounts with name starting with letter 's'
    data = manager.filter(name__istartswith='s')
    
   # Exclude accounts who have registred from 01-01-2015 till 2016
    data = manager.exclude(registered__date_range=('01-01-2015', '01-01-2016'))
    
   # Exclude accounts who have friends who are a male
    data = manager.filter(friends__gender='male')

   # Chain exclude e.g.
    data = manager.exclude(name__istartswith='s').exclude(gender='male')


Ordering
--------

You can order data by any value of object or dictionary :

.. code:: python

    from iterable_orm import QuerySet
    Accounts = [A list of account objects that have attrubtes such as name, email, age, gender ect ]
    manager = Queryset(Accounts)

    # Order by name 
    data = manager.order_by('name)

    # Order name by descending
    data = manager.order_by('-name)
    
    # Ordering by related lookup of friends name
    data = manager.order_by('friends__name')
    
    # Ordering by related lookup of friends name descending
    data = manager.order_by('-friends__name')


Unit Test
---------

Unit test inlcudes full example usage of the API

To tun unit test run:

.. code:: python

    python test.py


Installation
============

Install the latest release with:

::

    pip install iterable_orm


Compatibility
-------------

Python 2.7, 3.0 to 3.5


