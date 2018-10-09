class EarningsDate(object):
    
    def __init__(
        self, 
        ticker, 
        companyshortname, 
        startdatetime, 
        startdatetimetype,
        epsestimate,
        epsactual,
        epssurprisepct,
        gmtOffsetMilliSeconds):
        """Return a new PennyAlgo object."""
        self.ticker = ticker
        self.companyshortname = companyshortname
        self.startdatetime = startdatetime
        self.startdatetimetype = startdatetimetype
        self.epsestimate = epsestimate
        self.epsactual = epsactual
        self.epssurprisepct = epssurprisepct
        self.gmtOffsetMilliSeconds = gmtOffsetMilliSeconds


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

