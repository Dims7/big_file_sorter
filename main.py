from sys import argv
from sorter import Sorter

#ToDo сделать нормальные аргументы
#ToDo удаление без rmtree
#ToDo прогрессбар
#ToDo возможность указания временной директории
#ToDo readme
#ToDo тесты main.py

if __name__ == '__main__':
    if len(argv) == 2 and (argv[1] == "-h" or argv[1] == "--help"):
        print("""
Big file sorter
The program sorts a large file without loading it into memory completely

Arguments:
-f --filename       name of file to sort
-s --separators     String with separators for words in string/ 
                    Input like ' a|'. (Default tab and space)
-r --reverse        Reverse Sorting
-c --column         Column for sorting. Using this argument disables 
                    multisorting and enables stable sorting
-m --maxstrings     Max strings in tmp file""")
    else:
        if not '-f' in argv and not '--filename' in argv:
            raise Exception("Can`t find filename in arguments")

        file_name = ''
        if '-f' in argv:
            file_name = argv[argv.index("-f") + 1]
        else:
            file_name = argv[argv.index("--filename") + 1]

        separators = ''
        if '-s' in argv:
            separators = argv[argv.index("-s") + 1]
        if '--separators' in argv:
            separators = argv[argv.index("--separators") + 1]

        is_reverse = '-r' in argv or '--reverse' in argv
        is_multisorting = not '-c' in argv and not '--column' in argv

        column_for_sort = 0
        if '-c' in argv:
            column_for_sort = int(argv[argv.index("-c") + 1])
        if '--column' in argv:
            column_for_sort = int(argv[argv.index("--column") + 1])

        strings_in_tmp_file = 4000
        if '-m' in argv:
            column_for_sort = int(argv[argv.index("-m") + 1])
        if '--maxstrings' in argv:
            separators = int(argv[argv.index("--maxstrings") + 1])

        sorter = Sorter(input_file_name=file_name, separators=separators,
                        is_reverse=is_reverse, is_multisorting=is_multisorting,
                        column_for_sort=column_for_sort)

        sorter.sort()
