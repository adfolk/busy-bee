from orm import create_db_with_project_files

test_repo_path = "/home/adfolk/workspace/github.com/adfolk/experiments/monke/"

def main():
    create_db_with_project_files(test_repo_path)

if __name__ == "__main__":
    main()
