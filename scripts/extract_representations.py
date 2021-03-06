import argparse
import json
from nltk.corpus import stopwords

parser = argparse.ArgumentParser()
parser.add_argument("--subdocuments", dest="subdocuments", nargs="+")
parser.add_argument("--representations", dest="representations")
parser.add_argument("--lowercase", dest="lowercase", default=False, action="store_true")
parser.add_argument("--minimum_count", dest="minimum_count", default=1)
parser.add_argument("--num_words_to_keep", dest="num_words_to_keep", type=int, default=200)
parser.add_argument("--method", dest="method", choices=["stopwords", "frequency"], default="stopwords")
args = parser.parse_args()

def frequency_based_list(fnames, lowercase, number_of_words):
    document_frequencies = {}
    author_frequencies = {}
    title_frequencies = {}
    total_document_count = 0
    unique_authors = set()
    unique_titles = set()
    for fname in fnames:
        with open(fname, "rt") as ifd:
            text = json.loads(ifd.read())
            author = text["author"]
            title = text["title"]
            unique_authors.add(author)
            unique_titles.add(title)
            total_document_count += len(text["subdocuments"])
            for subdocument in text["subdocuments"]:
                subdocument = [w.lower() for w in subdocument] if lowercase else subdocument
                for word in set(subdocument):
                    document_frequencies[word] = document_frequencies.get(word, 0) + 1
                    author_frequencies[word] = author_frequencies.get(word, set())
                    author_frequencies[word].add(author)
                    title_frequencies[word] = title_frequencies.get(word, set())
                    title_frequencies[word].add(title)
    scored_words = []
    for word, document_count in document_frequencies.items():
        scored_words.append((document_count / total_document_count, word))
    top_words = sorted(scored_words, reverse=True)[0:number_of_words]
    return [w for _, w in top_words]

word_list = stopwords.words("english") if args.method == "stopwords" else frequency_based_list(args.subdocuments, args.lowercase, args.num_words_to_keep)

items = []
for fname in args.subdocuments:
    with open(fname, "rt") as ifd:
        text = json.loads(ifd.read())
        author = text["author"]
        title = text["title"]
        for subdocument in text["subdocuments"]:
            item = {
                "author" : author,
                "title" : title,
                "representation" : {},
            }
            for word in subdocument:
                word = word.lower() if args.lowercase else word
                
                item["representation"][word] = item["representation"].get(word, 0) + 1
            item["representation"] = {k : v / len(subdocument) for k, v in item["representation"].items() if v >= args.minimum_count and k in word_list}
            items.append(item)
            
with open(args.representations, "wt") as ofd:
    ofd.write(json.dumps(items, indent=4))
