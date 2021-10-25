from requests.models import Response
import xmltodict
import requests


class GeoService:
    domain = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?"
    defaultQueryOptions = "&targ=self&form=xml&view=quick"

    def __init__(self, acc) -> None:
        self.__buildQuery(acc)
        self.__getXMLToDict()

    def getOverAllDesign(self):
        try:
            return self.xmlDict['MINiML']['Series']['Overall-Design']
        except:
            print("No overall desgin field, proceed with default output")

    def __buildQuery(self, acc):
        self.query = (self.domain + f"acc={acc}" +
                      self.defaultQueryOptions)

    def __getXMLToDict(self):
        # XML gets converted to dict can access atrib though name
        try:
            reponse = requests.get(self.query)
            self.xmlDict = xmltodict.parse(reponse.text)
        except:
            print("Something went wrong can not get GEO records, "
                  "proceed with default data")
            self.xmlDict = None






