class PolygonSymbol(object):

    def __init__(
        self, 
        symbol, 
        name, 
        _type, 
        isOTC, 
        updated, 
        url):
        """Return a new Account object."""
        self.symbol = symbol
        self.name = name
        self._type = _type
        self.isOTC = isOTC
        self.updated = updated
        self.url = url


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

