from io_ops import find_src_files, parse_src_files
from parsers import extract_todo
from languages import Lang, SrcLangType

current_dir = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/'
target_file = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/lmao.go'
snake_vic = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/character.py'
def main():
    #print(find_src_files(current_dir))
    #com_lst, todo_lst = extract_todo(target_file, Lang(SrcLangType.GOLANG))

    #com_lst, todo_lst = extract_todo(snake_vic, Lang(SrcLangType.PYTHON))
    com_lst, todo_lst = parse_src_files(current_dir)
    print(com_lst)
    print("\n\n--------------------\n\n")
    print(todo_lst)


main()
