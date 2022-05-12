from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vaderAnalyzer = SentimentIntensityAnalyzer()

sentence1 = "Bitcoin is a powerfull coin. GREAT!"
sentence2 = "Crypto adoption in 2021: The prospects for 2021 look bright as major forces driving adoption in 2020 will remain powerful."

sentiment1 = vaderAnalyzer.polarity_scores(sentence1)
sentiment2 = vaderAnalyzer.polarity_scores(sentence2)

print("Sentence 1: ",sentiment1)
print("Sentence 2: ",sentiment2)