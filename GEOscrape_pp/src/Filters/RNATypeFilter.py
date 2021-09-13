from filter import Filter

class RNAtypeFilter(Filter):

    def __init__(self, df) -> None:
        super().__init__(df)
    
    ### Filter by only using the outputs in Paul's listGEO -> Try out how many false negatives and we can try entrez api?
    def lnt