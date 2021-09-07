import re
import os
import sys
import numpy as np
import pandas as pd
# Command line should be in format: terms.txt tsvofscrape

terms = sys.argv[1]
data_frame = sys.argv[2]

with open(terms, "r") as reader:
    my_terms = reader.readlines()

# Pandas to open data frame of our listGEOData output
df = pd.read_csv(data_frame, sep = "\t")

# print(df[["Title", "Summary", "SampleTerms"]])
# print(df.columns)

# Get relevant data in a tuple c(title, summary, sampleterms)
# for n_row in range ( len(df)) :
#     tuple_search = (df.loc[ n_row, "Title" ].lower(), df.loc[ n_row, "Summary"].lower(), df.loc[n_row, 'SampleTerms'].lower())
#     print(search)

def yield_row(df): 
    # get a row of a df

    for n_row in range(len(df)):
        row = df.iloc[n_row]

        yield(row)



class searchable(object):



    def __init__(self, df_row, my_terms):
        self.GSE = df_row["Acc"]
        self.Title = df_row["Title"]
        self.Sum = df_row["Summary"]
        self.Sample = df_row["SampleTerms"]
        self.searchable = self.Title.lower() + self.Sum.lower() + self.Sample.lower()

        self.Terms = my_terms

        self.title_hits = []
        self.summary_hits = []
        self.sample_hits = []
        self.searchable_hits = []

    def get_Terms(self):
        return(self.Terms)
    def get_searchable_hits(self):
        return(self.searchable_hits)
    def get_GSE(self):
        return(self.GSE)
    def get_result(self):
        return(self.result)

    def terms_to_list(self):
        new_terms = []
        for term in self.Terms:
            new_terms.append(term)
        self.Terms = new_terms

    def remove_newline(self):
        new_list = []
        for term in self.Terms:
            new_list.append(term.strip())
        self.Terms = new_list
        
        # new_terms = []
        
        # for term in self.Terms:
        #     term.replace("\n", "")
        # self.Terms = new_terms

    def terms_to_lower(self):
        new_terms = []
        for term in self.Terms:
            term = term.lower()
            new_terms.append(term)
        self.Terms = new_terms
        


    def test_title(self):

        for term in self.Terms:
            term_test = re.findall(term, self.Title)
            if len(term_test) > 0:
                self.title_hits.append(term_test)

    def test_summary(self):

        for term in self.Terms:
            term_test = re.findall(term, self.Sum)
            if len(term_test) > 0:
                self.summary_hits.append(term_test)

    def test_sample(self):

        for term in self.Terms:
            term_test = re.findall(term, self.Sample)
            if len(term_test) > 0:
                self.sample_hits.append(term_test)

    def test_searchable(self):

        for term in self.Terms:
            term_test = re.findall(term, self.searchable)
            if len(term_test) > 0:
                self.searchable_hits.append(term_test)          

    def identify_result(self):
        if self.searchable_hits:
            self.result = True
        else:
            self.result = False

                
    def __str__(self):
        return "Test1"

def main(df, my_terms):
    
    df_output = pd.DataFrame(columns = ("Acc", "Results", "Terms"), index = range(len(df)))
    index_output = 0

    df_row_gen = yield_row(df)

    for row_gen in df_row_gen:

        my_searchable = searchable(row_gen, my_terms)

        my_searchable.terms_to_list()
        my_searchable.terms_to_lower()
        my_searchable.remove_newline()

        my_searchable.test_searchable()

        my_searchable.identify_result()

        # print(my_searchable.get_GSE(), my_searchable.get_result(), my_searchable.get_searchable_hits())

        df_output.loc[index_output, "Acc"] = my_searchable.get_GSE()
        df_output.loc[index_output, "Results"] = my_searchable.get_result()
        df_output.loc[index_output, "Terms"] = my_searchable.get_searchable_hits()
        index_output+=1

    df_merged = df_output.join(df.set_index('Acc'), on = 'Acc')

    # df_output_hits = df_output.loc [df_output["Results"] == True]

    # df_output_hits.to_csv('Results_Hits.tsv', sep = "\t", header = True, index = False)
    # df_output.to_csv('Results_All.tsv', sep = "\t", header = True, index = False)

    df_merged.to_csv('Term_Related_GSEs.tsv', sep = "\t", header = True, index = False)

         


        # print(my_searchable.get_GSE(), my_searchable.get_searchable_hits())

# main(df, my_terms)
        
test_frame = df.iloc[0:1000,:]
# print(test_frame["Title"])a
main(test_frame, my_terms)


