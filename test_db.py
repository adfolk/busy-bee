from database import *
from orm import *

@with_test_db((ProjectRepo, SourceCodeFile, CodeTag))
def query_all(path: str):
    create_proj_tables(path)
    for tag in CodeTag.select():
        print(f"type: {tag.tag_name}\nmessage: {tag.message}")

def main():
    tppath = "/Users/austinfolkestad/workspace/github.com/adfolk/experiments/git-monkey/"
    query_all(tppath)

if __name__ == "__main__":
    main()
