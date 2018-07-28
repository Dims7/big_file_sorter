# -*- coding: UTF-8 -*-

from sorter import Sorter
import argparse
import strings


# ToDo прогрессбар
# ToDo readme
# ToDo тесты main.py

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', nargs='?', required=True,
                        help=strings.HELP_FILENAME)
    parser.add_argument('-s', '--separators', help=strings.HELP_SEPARATORS,
                        default="")
    parser.add_argument('-r', '--reverse', action='store_const', const=True,
                        default=False, help=strings.HELP_REVERSE)
    parser.add_argument('-c', '--column', type=int, help=strings.HELP_COLUMN,
                        default=0)
    parser.add_argument('-m', '--maxstrings', help=strings.HELP_MAX_STRINGS,
                        type=int, default=4000)
    parser.add_argument('-t', '--tmppath', help=strings.HELP_TMP_PATH, default=None)
    return parser


def run():
    parser = create_parser()
    namespace = parser.parse_args()

    sorter = Sorter(input_file_name=namespace.filename,
                    separators=namespace.separators,
                    is_reverse=namespace.reverse,
                    is_multisorting=namespace.column == 0,
                    column_for_sort=namespace.column,
                    path_tmp_dir=namespace.tmppath)
    sorter.sort()


if __name__ == '__main__':
    run()
