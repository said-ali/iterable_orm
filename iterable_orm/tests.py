import unittest

try:
    from query import QuerySet
except ImportError:
    # For travis-ci
    from .query import QuerySet

ACCOUNTS_DICT = [
    {
        "id": 0,
        "active": True,
        "age": 22,
        "name": "Angeline Holloway",
        "gender": "male",
        "company": "MEMORA",
        "email": "angelineholloway@memora.com",
        "address": "988 Kiely Place, London, Palau, 4460",
        "registered": "2014-09-21T04:35:42 -01:00",
        "friends": {
            "id": 0,
            "name": "Rivas Snow",
            "gender": "male"
        }
    },
    {
        "id": 1,
        "active": True,
        "age": 30,
        "name": "Claire Burris",
        "gender": "female",
        "company": "EXOVENT",
        "email": "claireburris@exovent.com",
        "address": "863 Senator Street, Troy, Puerto Rico, 4092",
        "registered": "2015-11-15T09:38:43 -00:00",
        "friends": {
            "id": 1,
            "name": "Marta Walton",
            "gender": "female"
        }
    },
    {
        "id": 2,
        "active": True,
        "age": 22,
        "name": "Jeannette Clarke",
        "gender": "female",
        "company": "FITCORE",
        "email": "jeannetteclarke@fitcore.com",
        "address": "248 Village Road, Brecon, Hawaii, 5992",
        "registered": "2015-05-02T05:44:45 -01:00",
        "friends": {
            "id": 2,
            "name": "Schultz Nielsen",
            "gender": "male"
        }
    },
    {
        "id": 3,
        "active": False,
        "age": 35,
        "name": "Zimmerman Mosley",
        "gender": "female",
        "company": "GAZAK",
        "email": "zimmermanmosley@gazak.com",
        "address": "114 Elliott Place, Watchtower, Kansas, 888",
        "registered": "2015-01-24T04:58:59 -00:00",
        "friends": {
            "id": 3,
            "name": "Figueroa Melton",
            "gender": "male"
        }
    },
    {
        "id": 4,
        "active": False,
        "age": 22,
        "name": "Montgomery Bolton",
        "gender": "male",
        "company": "KOFFEE",
        "email": "montgomerybolton@koffee.com",
        "address": "167 Dennett Place, Trail, Idaho, 5066",
        "registered": "2015-03-09T03:03:53 -00:00",
        "friends": {
            "id": 4,
            "name": "Jacklyn Stein",
            "gender": "female"
        }
    },
    {
        "id": 5,
        "active": True,
        "age": 24,
        "name": "Petty Lang",
        "gender": "male",
        "company": "GOLISTIC",
        "email": "pettylang@golistic.com",
        "address": "921 Montgomery Street, Manchester, Oregon, 4267",
        "registered": "2014-05-01T09:13:11 -01:00",
        "friends": {
            "id": 5,
            "name": "Aurelia Tyson",
            "gender": "female"
        }
    },
    {
        "id": 6,
        "active": True,
        "age": 32,
        "name": "Ward Waller",
        "gender": "male",
        "company": "ELITA",
        "email": "wardwaller@elita.com",
        "address": "849 Stuart Street, Grandview, South Dakota, 2509",
        "registered": "2015-12-08T06:01:21 -00:00",
        "friends": {
            "id": 6,
            "name": "Wong Dunn",
            "gender": "male"
        }
    },
    {
        "id": 7,
        "active": False,
        "age": 20,
        "name": "Crawford Wilkins",
        "gender": "male",
        "company": "VICON",
        "email": "crawfordwilkins@vicon.com",
        "address": "814 Lawrence Avenue, Finzel, California, 7246",
        "registered": "2016-04-06T06:47:57 -01:00",
        "friends": {
            "id": 7,
            "name": "Lindsay Joseph",
            "gender": "female"
        }
    }
]


class AccountObject(object):
    """ Converts dicts to object"""
    def __init__(self, data):
        for (key, value) in data.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [(AccountObject(x) if isinstance(x, dict) else x) for x in value])
            else:
                setattr(self, key, (AccountObject(value) if isinstance(value, dict) else value))

ACCOUNT_OBJECTS = [AccountObject(account) for account in ACCOUNTS_DICT]


class TestQueries(unittest.TestCase):

    def setUp(self):
        self.queryset = QuerySet(ACCOUNT_OBJECTS)
        self.maxDiff = None

    def test_filters_lamda(self):
        self.assertEqual(self.queryset.filter(company=lambda x: x == 'VICON' or x == 'ELITA').count(), 2)
        self.assertEqual(self.queryset.filter(age=lambda x: x >= 20 and x <= 30).count(), 6)
        self.assertEqual(self.queryset.filter(age=lambda x: x >= 20 and x <= 30).exclude(gender='male').count(), 2)
        self.assertEqual(self.queryset.filter(age=lambda x: x >= 20 and x <= 30).exclude(gender='female').count(), 4)

    def test_filters(self):
        self.assertEqual(self.queryset.filter(name='Crawford Wilkins')[0].id, ACCOUNT_OBJECTS[7].id)
        self.assertEqual(self.queryset.filter(address__icontains='London')[0].id, ACCOUNT_OBJECTS[0].id)
        self.assertEqual(self.queryset.filter(email='crawfordwilkins@vicon.com').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).count(), 5)
        self.assertEqual(self.queryset.filter(active=False).count(), 3)
        self.assertEqual(self.queryset.filter(gender='male').count(), 5)
        self.assertEqual(self.queryset.filter(gender='female').count(), 3)
        self.assertEqual(self.queryset.filter(address__contains='london').count(), 0)
        self.assertEqual(self.queryset.filter(address__icontains='London').count(), 1)
        self.assertEqual(self.queryset.filter(age__gte=30).count(), 3)
        self.assertEqual(self.queryset.filter(age__gt=30).count(), 2)
        self.assertEqual(self.queryset.filter(age__lte=22).count(), 4)
        self.assertEqual(self.queryset.filter(age__lt=30).count(), 5)
        self.assertEqual(self.queryset.filter(age__lte=30).count(), 6)
        self.assertEqual(self.queryset.filter(name__startswith='Angeline').count(), 1)
        self.assertEqual(self.queryset.filter(name__startswith='c').count(), 0)
        self.assertEqual(self.queryset.filter(name__istartswith='c').count(), 2)
        self.assertEqual(self.queryset.filter(name__istartswith='c').count(), 2)
        self.assertEqual(self.queryset.filter(name__endswith='s').count(), 2)

    def test_filters_combine(self):
        self.assertEqual(self.queryset.filter(active=True, age__lte=22, gender='female', company='FITCORE').count(), 1)
        self.assertEqual(self.queryset.filter(active=True, age__lte=22, gender='female').count(), 1)
        self.assertEqual(self.queryset.filter(active=True, age=22, gender='female').count(), 1)
        self.assertEqual(self.queryset.filter(active=True, age=22, gender='male').count(), 1)
        self.assertEqual(self.queryset.filter(active=True, age=22, gender='male', name='Angeline Holloway').count(), 1)
        self.assertEqual(self.queryset.filter(active=True, id=5).count(), 1)
        self.assertEqual(self.queryset.filter(active=True, age=22).count(), 2)
        self.assertEqual(self.queryset.filter(active=True, id=5).first().id, ACCOUNT_OBJECTS[5].id)

    def test_filters_combine_chained(self):
        self.assertEqual(self.queryset.filter(active=True).filter(age__lte=22).filter(gender='female').filter(company='FITCORE').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(age__lte=22).filter(gender='female').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(age=22).filter(gender='female').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(age=22).filter(gender='male').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(age=22).filter(gender='male').filter(name='Angeline Holloway').count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(id=5).count(), 1)
        self.assertEqual(self.queryset.filter(active=True).filter(age=22).count(), 2)
        self.assertEqual(self.queryset.filter(active=True).filter(id=5).first().id, ACCOUNT_OBJECTS[5].id)

    def test_exclude(self):
        self.assertEqual(self.queryset.exclude(email='crawfordwilkins@vicon.com').count(), 7)
        self.assertEqual(self.queryset.exclude(gender='male').count(), 3)
        self.assertEqual(self.queryset.exclude(active=True).count(), 3)
        self.assertEqual(self.queryset.exclude(active=False).count(), 5)
        self.assertEqual(self.queryset.exclude(address__contains='london').count(), 8)
        self.assertEqual(self.queryset.exclude(address__icontains='London').count(), 7)
        self.assertEqual(self.queryset.exclude(age__gte=30).count(), 5)
        self.assertEqual(self.queryset.exclude(age__gt=30).count(), 6)
        self.assertEqual(self.queryset.exclude(age__lte=22).count(), 4)
        self.assertEqual(self.queryset.exclude(age__lt=30).count(), 3)
        self.assertEqual(self.queryset.exclude(age__lte=30).count(), 2)
        self.assertEqual(self.queryset.exclude(name__startswith='Angeline').count(), 7)
        self.assertEqual(self.queryset.exclude(name__startswith='c').count(), 8)
        self.assertEqual(self.queryset.exclude(name__istartswith='c').count(), 6)
        self.assertEqual(self.queryset.exclude(name__istartswith='c').count(), 6)
        self.assertEqual(self.queryset.exclude(name__endswith='s').count(), 6)

    def test_exclude_combine(self):
        self.assertEqual(self.queryset.exclude(active=True, age__lte=22, gender='female').count(), 7)
        self.assertEqual(self.queryset.exclude(active=True, age=22, gender='female').count(), 7)
        self.assertEqual(self.queryset.exclude(active=True, id=5).count(), 7)
        self.assertEqual(self.queryset.exclude(active=True, age=22).count(), 6)

    def test_exclude_combine_chained(self):
        self.assertEqual(self.queryset.exclude(active=True).exclude(age__lte=22).exclude(gender='male').count(), 1)
        self.assertEqual(self.queryset.exclude(active=True).exclude(age=22).exclude(gender='female').count(), 1)
        self.assertEqual(self.queryset.exclude(active=True).exclude(id=5).count(), 3)
        self.assertEqual(self.queryset.exclude(active=True).exclude(age=22).count(), 2)

    def test_filter_combined_with_exclude(self):
        self.assertEqual(self.queryset.filter(active=True).exclude(gender='male').count(), 2)
        self.assertEqual(self.queryset.filter(active=True, gender='male').exclude(age__lte=22).count(), 2)

    def test_get(self):
        self.assertEqual(self.queryset.get(name='Angeline Holloway'), ACCOUNT_OBJECTS[0])
        self.assertEqual(self.queryset.get(id=0), ACCOUNT_OBJECTS[0])

    def test_related_lookups(self):
        self.assertEqual(self.queryset.filter(friends__gender='male').count(), 4)
        self.assertEqual(self.queryset.filter(friends__gender='female').count(), 4)
        self.assertEqual(self.queryset.filter(friends__gender='male').exclude(active=False).count(), 3)
        self.assertEqual(self.queryset.filter(friends__gender='male').exclude(active=True).count(), 1)

    def test_ordering(self):
        self.assertEqual(list(self.queryset.order_by('id')), ACCOUNT_OBJECTS)
        self.assertEqual(list(self.queryset.order_by('-id')), list(reversed(ACCOUNT_OBJECTS)))
        self.assertEqual(list(self.queryset.order_by('gender')), sorted(ACCOUNT_OBJECTS, key=lambda x: x.gender))
        self.assertEqual(list(self.queryset.order_by('-gender')), sorted(ACCOUNT_OBJECTS, key=lambda x: x.gender, reverse=True))

    def test_orderings(self):
        self.assertEqual(list(self.queryset.order_by('friends__gender')), sorted(
            ACCOUNT_OBJECTS, key=lambda x: x.friends.gender))
        self.assertEqual(list(self.queryset.order_by('-friends__gender')),
                         sorted(ACCOUNT_OBJECTS, key=lambda x: x.friends.gender, reverse=True))

        self.assertEqual(list(self.queryset.order_by('friends__name')), sorted(
            ACCOUNT_OBJECTS, key=lambda x: x.friends.name))
        self.assertEqual(list(self.queryset.order_by('-friends__name')),
                         sorted(ACCOUNT_OBJECTS, key=lambda x: x.friends.name, reverse=True))

    def test_exists(self):
        self.assertTrue(self.queryset.filter(email='wardwaller@elita.com').exists())
        self.assertFalse(self.queryset.filter(email='said.ali@msn.com').exists())
        self.assertTrue(self.queryset.filter(friends__name='Lindsay Joseph').exists())
        self.assertFalse(self.queryset.filter(friends__name='Said Ali').exists())

    def test_first(self):
        self.assertTrue(self.queryset.filter(email='wardwaller@elita.com').first())
        self.assertFalse(self.queryset.filter(email='said.ali@msn.com').first())
        self.assertEqual(self.queryset.filter(email='wardwaller@elita.com').first(), self.queryset.filter(email='wardwaller@elita.com')[0])

    def test_value_range(self):
        queryset = self.queryset.filter(registered__value_range=('2015-09-21', '2016-12-08')).exclude(name='Crawford Wilkins')
        self.assertEqual(queryset.count(), 2)
        queryset = queryset.filter(registered__value_range=('2015-09-21', '2016-12-08')).exclude(name='Crawford Wilkins')

        queryset = self.queryset.filter(registered__value_range=('2015-11-15', '2015-11-16'))
        self.assertEqual(queryset[0].id, ACCOUNT_OBJECTS[1].id)

if __name__ == '__main__':
    unittest.main()
