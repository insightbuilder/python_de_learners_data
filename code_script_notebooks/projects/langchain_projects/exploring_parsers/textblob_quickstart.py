# Script looks at the ways TextBlob module can be used 
from textblob import Word
from textblob.wordnet import VERB, NOUN, ADJ, ADV
from textblob import TextBlob

wiki = TextBlob("Python is a high-level, general-purpose programming language.")
# print(wiki.tags)

# print(wiki.noun_phrases)

query = """*DLH DARPAN TOWER*\n2BHK FLAT SALE\n2.OPTINS\n2.CR TO 2.20.CR NEGOTIABLE \n\n*2BHK MITTAL COVE*\nNEW BUILDING\nPRICE 2.10.CR NEGOTIABLE \n\n*2BHK CAME SWEET 16*\nAZAD NAGAR\nASKING 1.90.CR NEGOTIABLE \n\n*2BHK PALASH TOWER*\n3.OPTINS\n2.25.CR TO 2.55.CR\n\n1BHK FLAT SALE\n*SANGAM APARTMENT*\nCARPET 500.SQFIT\nPRICE 1.40.CR\n\nVEER DESSAI ROAD ANDHERI WEST\n\n\n*2BHK RENTAL FLAT*\n*VAIDEHI APARTMENTS*\n*FURNISHED FLAT*\n*RENT 70.00* *NEGOTIABLE*\n*VEERA DESAI ROAD NEAR AZAD NAGAR METRO STATION ANDHERI WEST*\n\n2BHK RENTAL\nEXCLUSIVE FULLY FURNISHED\n*SHANTIVAN MHADA OSHIWARA*\nRENT 75.000\n \n3BHK RENTAL\n*MITTAL COVE*\nNEW BUILDING\nEMPTY FLAT\n3BHK 2BHATHROO\nRENT 75.000\n\n3bhk semi furnished flat \n*SHIV SHIVAM TOWER* \nonly working family client immediate possession \n*RENT 80K*\n\nANY INFORMATION\nCALL ME\nDHARMENDRA\n9987741783"""

query_blob = TextBlob(query)
print(query_blob.tags)

print(query_blob.words)
print(query_blob.word_counts)
for sent in query_blob.sentences:
    print(sent)

print(Word('Ridiculous').definitions)

print(query_blob.parse())
