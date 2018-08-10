import re
import os
import tempfile
from progressbar_for_sorter import ProgressbarForSorter


class Sorter:
    regexp_for_split = None
    input_file_name = None
    path_input_file = None
    path_tmp_dir = None
    is_reverse = None
    some_regexp = None
    tmp_files_names = None

    bar = None

    def __init__(self,
                 input_file_name,
                 separators,
                 is_reverse=False,
                 is_multisorting=True,
                 column_for_sort=0,
                 strings_in_tmp_file=4000,
                 path_tmp_dir=None):
        self.regexp_for_split = self.make_regexp_for_split(separators)
        self.path_input_file = os.getcwd()
        self.input_file_name = input_file_name
        self.path_tmp_dir = self.make_tmp_dir(path_tmp_dir)
        self.is_reverse = is_reverse
        self.is_multisorting = is_multisorting
        self.column_for_sort = column_for_sort - 1
        self.some_separator = self.get_some_separator(self.regexp_for_split)
        self.string_counter = 0
        self.strings_in_tmp_file = strings_in_tmp_file
        self.tmp_files_names = []
        self.tmp_file_counter = 0
        self.merging_in_one_step = 10
        self.bar = ProgressbarForSorter(input_file_name, strings_in_tmp_file,
                                        self.merging_in_one_step)

    def sort(self):
        self.split_file_into_sorted_tmp_files()
        self.merging_all_tmp_files()
        result_file_name = self.tmp_files_names[0]
        if not self.is_multisorting:
            self.prepare_stable_sorting_file_to_replace(result_file_name)
        os.chdir(self.path_input_file)
        self.replace_input_file_with_result_file(result_file_name)
        self.delete_tmp_dir()

    @staticmethod
    def get_some_separator(regexp_for_split):
        if regexp_for_split.pattern[0] != '[':
            return regexp_for_split.pattern[0]
        if regexp_for_split.pattern[1] != '\\':
            return regexp_for_split.pattern[1]
        return regexp_for_split.pattern[2]

    @staticmethod
    def make_regexp_for_split(separators):
        """Преобразует строку из сепараторов в регвыр для сплита по колонкам"""
        if len(separators) == 1:
            if separators == '[':
                return re.compile("\[")
            if separators == ']':
                return re.compile("\]")
            return re.compile(separators)

        if len(separators) == 0:
            separators = " \t"

        result = "["
        for char in separators:
            if char == "[" or char == "]":
                result += "\\"
            result += char
        result += ']'
        return re.compile(result)

    @staticmethod
    def make_tmp_dir(temp_dir):
        """Создаёт временную директорию и возвращает путь к ней"""
        if temp_dir is None:
            return tempfile.mkdtemp()
        else:
            try:
                os.stat(temp_dir)
            except IOError:
                os.mkdir(temp_dir)
            return os.getcwd() + '/' + temp_dir

    def split_file_into_sorted_tmp_files(self):
        """Отправляет во временую директорию отсортированные фрагменты
        исходного файла"""
        current_dir = os.getcwd()
        os.chdir(self.path_input_file)
        input_file = open(self.input_file_name, 'r')
        os.chdir(self.path_tmp_dir)

        current_lines = 0
        tmp_text = ""
        for chunk in iter(lambda: input_file.readline(), ''):
            if current_lines != 0:
                tmp_text += "\n"
            current_lines += 1
            chunk = chunk.replace("\n", "")
            tmp_text += chunk

            if current_lines == self.strings_in_tmp_file:
                current_lines = 0
                tmp_file = open(str(self.tmp_file_counter) + ".tmp", 'w')
                self.tmp_files_names.append(tmp_file.name)
                tmp_text = self.sort_text(tmp_text)
                tmp_file.write(tmp_text)
                tmp_file.close()
                tmp_text = ""
                self.tmp_file_counter += 1

        if tmp_text != "" or self.tmp_file_counter == 0:
            tmp_file = open(str(self.tmp_file_counter) + ".tmp", 'w')
            self.tmp_files_names.append(tmp_file.name)
            self.tmp_file_counter += 1
            tmp_text = self.sort_text(tmp_text)
            tmp_file.write(tmp_text)
            tmp_file.close()
        input_file.close()
        os.chdir(current_dir)

    def sort_text(self, input_text):
        """Сортирует текст одним из методов:
        мультисортировка или стабильная сортирока"""
        self.bar.update_for_sorter()
        if self.is_multisorting:
            return self.multisorting_text(input_text)
        return self.stable_sorting_text(input_text)

    def multisorting_text(self, input_text):
        """Сортирует текст методом мультисортировки"""
        if input_text == '':
            return ''
        strings = input_text.split('\n')
        splitted_strings = []
        for i in range(len(strings)):
            splitted_strings.append([
                re.split(self.regexp_for_split, strings[i].lower()),
                strings[i]])
        splitted_strings.sort(reverse=self.is_reverse)
        result = ""
        for splitted_string in splitted_strings:
            result += splitted_string[1] + "\n"
        return result[:-1]

    def stable_sorting_text(self, input_text):
        """Сортирует текст методом стабильной сортировки"""
        if input_text == "":
            return ""
        strings = input_text.split('\n')
        splitted_strings = []
        for i in range(len(strings)):
            tmp_arr = []
            splittered = re.split(self.regexp_for_split, strings[i].lower())
            column_for_current_sort = self.column_for_sort
            if column_for_current_sort > len(splittered) - 1:
                tmp_arr.append('')
            else:
                tmp_arr.append(splittered[self.column_for_sort])
            tmp_arr.append(self.string_counter)
            tmp_arr.append(strings[i])
            splitted_strings.append(tmp_arr)
            self.string_counter += 1
        splitted_strings.sort(reverse=self.is_reverse)

        for splitted_string in splitted_strings:
            splitted_string[1] = str(splitted_string[1])

        for i in range(len(splitted_strings)):
            splitted_strings[i] = self.some_separator.join(splitted_strings[i])
        return "\n".join(splitted_strings)

    def compare_for_multisorting(self, strings):
        """Получает на вход массив строк и возвращает id наименьшей
        (если не реверсивно)"""
        tmp_arr = []
        counter = 0
        for string in strings:
            tmp_arr.append(
                [re.split(self.regexp_for_split, string.lower()), counter])
            counter += 1
        tmp_arr.sort(reverse=self.is_reverse)

        return tmp_arr[0][1]

    def compare_for_stable_sorting(self, strings):
        """Получает на вход массив строк и возвращает id наименьшей
        (если не реверсивно)"""
        tmp_arr = []
        counter = 0
        for string in strings:
            tmp_arr.append(
                [re.split(self.regexp_for_split, string.lower()), counter])
            tmp_arr[len(tmp_arr) - 1][0][1] = int(
                tmp_arr[len(tmp_arr) - 1][0][1])
            counter += 1
        tmp_arr.sort(reverse=self.is_reverse)
        return tmp_arr[0][1]

    def compare_strings(self, strings):
        """Получает на вход массив строк и возвращает id наименьшей
        (если не включена реверсивная сортировка)"""
        self.bar.update_for_compare()
        if self.is_multisorting:
            return self.compare_for_multisorting(strings)
        return self.compare_for_stable_sorting(strings)

    def merging_all_tmp_files(self):
        """Объединяет все временные файлы в результирующий"""
        while len(self.tmp_files_names) != 1:
            count_of_merging = min(self.merging_in_one_step,
                                   len(self.tmp_files_names))
            self.merging_any_tmp_files(count_of_merging)

    def merging_any_tmp_files(self, count_of_files):
        """Объединяет определённое число временных файлов в один"""

        os.chdir(self.path_tmp_dir)
        result_file = open(str(self.tmp_file_counter) + ".tmp", 'w')
        self.tmp_files_names.append(result_file.name)
        self.tmp_file_counter += 1

        range_of_files = []
        for i in range(count_of_files):
            range_of_files.append(i)

        files = []
        for i in range_of_files:
            files.append(open(self.tmp_files_names[i], 'r'))

        strings_from_files = []
        for i in range(count_of_files):
            current_string = files[i].readline()
            if current_string == "":
                range_of_files.remove(i)
            else:
                current_string = current_string.replace("\n", "")
                strings_from_files.append(current_string)

        is_firts_string = True
        while len(strings_from_files) != 0:
            if not is_firts_string:
                result_file.write("\n")
            else:
                is_firts_string = False
            id_to_add = self.compare_strings(strings_from_files)
            result_file.write(strings_from_files[id_to_add])
            new_string = files[range_of_files[id_to_add]].readline()
            if new_string != "":
                new_string = new_string.replace("\n", "")
                strings_from_files[id_to_add] = new_string
            else:
                strings_from_files.remove(strings_from_files[id_to_add])
                range_of_files.remove(range_of_files[id_to_add])

        for file in files:
            name = file.name
            file.close()
            os.remove(name)
            self.tmp_files_names.remove(name)

        result_file.close()


    def replace_input_file_with_result_file(self, result_file_name):
        """Перезаписывает исходный файл результирующим"""
        os.chdir(self.path_tmp_dir)
        result_file = open(result_file_name, 'r')
        os.chdir(self.path_input_file)
        input_file = open(self.input_file_name, 'w')
        for chunk in iter(lambda: result_file.readline(), ''):
            input_file.write(chunk)
        input_file.close()
        result_file.close()

    def prepare_stable_sorting_file_to_replace(self, file_name):
        """Превращает строки файла, отсортированного методом стабильной
        сортировки в строки исходного файла"""
        file_to_remake = open(file_name, 'r')
        tmp_file_name = tempfile.mktemp()
        tmp_file = open(tmp_file_name, 'w')
        is_first_line = True
        for chunk in iter(lambda: file_to_remake.readline(), ''):
            if not is_first_line:
                tmp_file.write("\n")
            is_first_line = False
            chunk = chunk.replace("\n", "")
            chunk = chunk.split(self.some_separator, 2)
            tmp_file.write(chunk[2])
        tmp_file.close()
        file_to_remake.close()

        tmp_file = open(tmp_file_name, 'r')
        file_to_remake = open(file_name, 'w')

        for chunk in iter(lambda: tmp_file.readline(), ''):
            file_to_remake.write(chunk)
        tmp_file.close()
        file_to_remake.close()

    def delete_tmp_dir(self):
        """Удаляет временную директорию"""
        while len(self.tmp_files_names) > 0:
            path = os.path.join(self.path_tmp_dir, self.tmp_files_names.pop())
            os.remove(path)
        os.rmdir(self.path_tmp_dir)