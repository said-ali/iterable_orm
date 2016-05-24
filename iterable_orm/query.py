try:
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse
except ImportError:
    from itertools import filterfalse
    from functools import reduce

from operator import attrgetter, itemgetter


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


def lookups(filter):
    return {
        'gt': lambda obj_value, value: obj_value > value,
        'gte': lambda obj_value, value: obj_value >= value,
        'lt': lambda obj_value, value: obj_value < value,
        'lte': lambda obj_value, value: obj_value <= value,
        'startswith': lambda obj_value, value: obj_value.startswith(value),
        'istartswith': lambda obj_value, value: obj_value.lower().startswith(value),
        'endswith': lambda obj_value, value: obj_value.endswith(value),
        'contains': lambda obj_value, value: value in obj_value,
        'icontains': lambda obj_value, value: value.lower() in obj_value.lower(),
        'not_equal_to': lambda obj_value, value: obj_value != value,
        'value_in': lambda obj_value, value: obj_value in value,
        'value_not_in': lambda obj_value, value: obj_value not in value,
        'value_range': lambda obj_value, range_values: obj_value >= range_values[0] and obj_value <= range_values[1],
        'date_range': lambda obj_value, range_values: obj_value.isoformat() >= range_values[0].isoformat() and obj_value.isoformat() <= range_values[1].isoformat(),
    }.get(filter, None)


class QuerySet(object):

    def __init__(self, queryset):
        try:
            self._queryset = list(queryset)
        except TypeError:
            raise ValueError('Queryset must be a list of objects or Dictionary')

    def __iter__(self):
        for query in self._queryset:
            yield query

    def __getitem__(self, index):
        return self._queryset[index]

    def __len__(self):
        return len(self._queryset)

    def _copy(self, queryset):
        """TODO chain function calls togther until consumption """
        return self.__class__(queryset)

    def first(self):
        if self._queryset:
            return self._queryset[0]
        return None

    def last(self):
        if self._queryset:
            return self._queryset[-1]
        return None

    def exists(self):
        return bool(self)

    def count(self):
        return len(self)

    def all(self):
        return self._copy(self._queryset)

    def order_by(self, key):
        reverse = False
        if '-' in key:
            reverse = True
            key = key.replace('-', '')
        try:
            return self._copy(sorted(self._queryset, key=attrgetter(key.replace('__', '.')), reverse=reverse))
        except AttributeError:
            return self._copy(sorted(self._queryset, key=itemgetter(key.replace('__', '.')), reverse=reverse))

    def _filter_or_exclude(self, **kwargs):
        """ Used for filter and exlcude returns a function to be used by itertool"""
        def _filter(obj):
            for key, value in kwargs.items():
                field_lookup = lookups(key.split('__')[-1])
                lookup_key = key.replace('__', '.').split(".")

                # It looks like a function has been passed
                if hasattr(value, '__call__'):
                    if not value(reduce(getattr, lookup_key, obj)):
                        return False
                    continue

                if field_lookup:
                    # Since there's field_lookup remove last element which is a look up value such as gt, startswith ect
                    lookup_key.pop()
                    try:
                        lookup_match = field_lookup(reduce(getattr, lookup_key, obj), value)
                    except AttributeError:

                        try:
                            lookup_match = field_lookup(reduce(lambda d, k: d[k], lookup_key, obj), value)
                        except (KeyError, TypeError):
                            raise ValueError('Object {obj} does not have attribute or key: {lookup_key}'.format(
                                obj=obj, lookup_key=lookup_key[0]))

                    if not lookup_match:
                        return False
                    continue

                try:
                    field_match = reduce(getattr, lookup_key, obj) == value
                except AttributeError:
                    try:
                        field_match = reduce(lambda d, k: d[k], lookup_key, obj) == value
                    except (KeyError, TypeError):
                        raise ValueError('Object {obj} does not have attribute or key :{lookup_key}'.format(
                            obj=obj, lookup_key=key))

                if not field_match:
                    return False
            return True
        return _filter

    def filter(self, **kwargs):
        return self._copy(filter(self._filter_or_exclude(**kwargs), self._queryset))

    def exclude(self, **kwargs):
        return self._copy(filterfalse(self._filter_or_exclude(**kwargs), self._queryset))

    def get(self, **kwargs):
        clone = self.filter(**kwargs)
        num = len(clone)
        if num == 1:
            return clone[0]
        if not num:
            raise ObjectDoesNotExist("Matching query does not exist.")

        if len(clone) > 1:
            raise MultipleObjectsReturned("get() returned more than one -- it returned {num}!".format(num=num))
