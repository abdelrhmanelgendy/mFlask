from pytube import  Search
s=Search('sebedy')
print(len(s.results))
print(s.completion_suggestions)