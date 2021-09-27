import pandas as pd
from datetime import datetime
import os
class Writer:
    

    @staticmethod
    def writeToCsv(resultsFrame, sep, outPutDir):
        print(f"Outputing the file in your selected location at {outPutDir}")
        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        resultsFrame.to_csv(os.path.join(outPutDir,f"Processed_GeoSrape_{currTime}"), sep = sep, index=False)