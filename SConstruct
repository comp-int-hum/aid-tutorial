import os
import steamroller

env = Environment(
    ENV=os.environ,
    tools=["default", steamroller.generate],
)

env.AddBuilder(
    "DivideDocuments",
    "scripts/divide_documents.py",
    "--primary_source ${SOURCE} --subdocuments ${TARGET} --words_per_subdocument ${WORDS_PER_SUBDOCUMENT}"
)

env.AddBuilder(
    "ExtractRepresentations",
    "scripts/extract_representations.py",
    "--subdocuments ${SOURCES} --representations ${TARGET} ${'--lowercase' if LOWERCASE else ''} --method ${METHOD}"
)

env.AddBuilder(
    "ClusterRepresentations",
    "scripts/cluster_representations.py",
    "--representations ${SOURCE} --clustering ${TARGET} --cluster_count ${CLUSTER_COUNT}"
)

env.AddBuilder(
    "CollateResults",
    "scripts/collate_results.py",
    "--clusterings ${SOURCES} --figure ${TARGET}"
)

all_subdocuments = []
for document in Glob("data/*"):
    subdocuments = env.DivideDocuments(
        "work/${SOURCE.name}.json",
        document,
        WORDS_PER_SUBDOCUMENT=2000
    )
    all_subdocuments.append(subdocuments)

representations = env.ExtractRepresentations(
    "work/representations.json",
    all_subdocuments,
    NUM_WORDS_TO_KEEP=100,
    METHOD="stopwords"
)

clustering = env.ClusterRepresentations(
    "work/clustering.json",
    representations,
    CLUSTER_COUNT=20
)

results = env.CollateResults(
    "work/results.png",
    clustering    
)
