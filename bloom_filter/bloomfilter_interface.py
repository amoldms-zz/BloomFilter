import abc


class BloomFilterInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add') and
                callable(subclass.add) and
                hasattr(subclass, 'bulk_add') and
                callable(subclass.bulk_add) and
                hasattr(subclass, 'contain') and
                callable(subclass.contain) or
                NotImplemented)

    @abc.abstractmethod
    def add(self, item: object):
        """Add item to bloom filter"""
        raise NotImplementedError

    @abc.abstractmethod
    def bulk_add(self, items: list):
        """Bulk add items to bloom filter"""
        raise NotImplementedError

    @abc.abstractmethod
    def contain(self, items: object):
        """Check if item exists in bloom filter"""
        raise NotImplementedError
