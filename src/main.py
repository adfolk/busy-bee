# from io_ops import extract_comment_blocks
from languages import Lang, SrcLangType
from parsers import group_comment_blocks
# from languages import Lang, SrcLangType

current_dir = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/'
target_file = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/lmao.go'
snake_vic = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/character.py'

def main():
    #print(find_src_files(current_dir))

    #com_lst, todo_lst = parse_src_files(current_dir)
    snek = Lang(SrcLangType.PYTHON)
    com_blocks = group_comment_blocks(snake_vic, snek)
    # for block in com_blocks:
    #     print(block)
    #     print("\n\n---------\n\n")
    # print("\n\n--------------------\n\n")
    #print(todo_lst)
    print("finished")


main()
