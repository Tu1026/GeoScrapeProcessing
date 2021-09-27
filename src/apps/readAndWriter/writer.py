import pandas as pd
from datetime import datetime
import os
class Writer:
    

    @staticmethod
    def writeToCsv(resultsFrame, sep, outPutDir):
        print(f"Outputing the file in your selected location at {outPutDir}")
        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if sep == "\t":
            format="tsv"
        else:
            format="csv"
        resultsFrame.to_csv(os.path.join(outPutDir,f"Processed_GeoSrape_{currTime}.{format}"), sep = sep, index=False)