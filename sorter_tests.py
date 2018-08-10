import unittest
from sorter import Sorter
import re
import os
import tempfile
from random import randint
import main

# ToDo сделать тесты

class TestMakeRegexpForSplit(unittest.TestCase):

    def make_assert(self, separators, need_to_compile):
        sorter = Sorter(separators=separators, input_file_name='')
        self.assertEqual(
            re.compile(need_to_compile),
            sorter.regexp_for_split)

    def test_without_separators(self):
        self.make_assert('', "[ \t]")

    def test_single_separator(self):
        self.make_assert('@', '@')

    def test_many_separators(self):
        self.make_assert('@rt \t', "[@rt \t]")

    def test_with_single_bracket(self):
        self.make_assert('[', "\[")
        self.make_assert(']', '\]')

    def test_with_brackets(self):
        self.make_assert(']@rt[ \t', "[\]@rt\[ \t]")


class TestMakeAndDeleteTmpDir(unittest.TestCase):
    sorter = Sorter(separators='', input_file_name='')

    #ToDo сделать тесты с конкретной директорией

    def test_all(self):
        self.create_tmp_dir_test()
        self.delete_tmp_dir_test()

    def create_tmp_dir_test(self):
        self.sorter.make_tmp_dir(None)
        tmp_dir_name = re.split('[\\/]', self.sorter.path_tmp_dir)[
            len(re.split('[\\/]', self.sorter.path_tmp_dir)) - 1]
        self.assertTrue(tmp_dir_name in os.listdir(tempfile.gettempdir()))

    def delete_tmp_dir_test(self):
        self.sorter.delete_tmp_dir()
        tmp_dir_name = re.split('[\\/]', self.sorter.path_tmp_dir)[
            len(re.split('[\\/]', self.sorter.path_tmp_dir)) - 1]
        self.assertFalse(
            tmp_dir_name in os.listdir(tempfile.gettempdir()))


class TestMultisortingTest(unittest.TestCase):
    sorter = Sorter(input_file_name='', separators='_')
    sorter_reverse = Sorter(input_file_name='', separators='_',
                            is_reverse=True)

    def test_empty_test(self):
        self.assertEqual(
            '',
            self.sorter.multisorting_text('')
        )
        self.assertEqual(
            '',
            self.sorter_reverse.multisorting_text('')
        )

    def test_text_with_single_string(self):
        self.assertEqual(
            'a_b_c',
            self.sorter.multisorting_text('a_b_c')
        )
        self.assertEqual(
            'c_b_a',
            self.sorter_reverse.multisorting_text('c_b_a')
        )

    def test_text_with_any_strings(self):
        self.assertEqual(
            '1__hy_hiyb\n1_a_ij_j_jo\n2_a_yjtytj',
            self.sorter.multisorting_text(
                '1__hy_hiyb\n2_a_yjtytj\n1_a_ij_j_jo')
        )
        self.assertEqual(
            '2_a_yjtytj\n1_a_ij_j_jo\n1__hy_hiyb',
            self.sorter_reverse
                .multisorting_text('1_a_ij_j_jo\n2_a_yjtytj\n1__hy_hiyb')
        )

    def test_smth_goes_wrong(self):
        self.assertEqual(
            'explode\nexplode acceptable capital explode',
            self.sorter.multisorting_text(
                'explode\nexplode acceptable capital explode')
        )
        self.assertEqual(
            'explode\nexplode acceptable capital explode',
            self.sorter.multisorting_text(
                'explode acceptable capital explode\nexplode')
        )


class TestGetSomeSeparator(unittest.TestCase):
    def test_with_bracket(self):
        self.assertEqual(
            'a',
            Sorter.get_some_separator(re.compile('[abc]'))
        )

    def test_without_brackets(self):
        self.assertEqual(
            'a',
            Sorter.get_some_separator(re.compile('a'))
        )

    def test_bracket_in_brackets(self):
        self.assertEqual(
            '[',
            Sorter.get_some_separator(re.compile('[\[ab]'))
        )


class TestStableSortingTest(unittest.TestCase):
    sorter = Sorter(separators='_', is_multisorting=False, column_for_sort=2,
                    input_file_name="")
    sorter_reverse = Sorter(separators='_', is_reverse=True,
                            is_multisorting=False, column_for_sort=2,
                            input_file_name="")

    def refresh_sorters(self):
        self.sorter.string_counter = 0
        self.sorter_reverse.string_counter = 0

    def test_empty_text(self):
        self.refresh_sorters()
        self.assertEqual(
            "",
            self.sorter.stable_sorting_text("")
        )
        self.assertEqual(
            "",
            self.sorter_reverse.stable_sorting_text("")
        )

    def test_text_with_single_string(self):
        self.refresh_sorters()
        self.assertEqual(
            "456_0_123_456_789",
            self.sorter.stable_sorting_text("123_456_789")
        )
        self.assertEqual(
            "456_0_123_456_789",
            self.sorter_reverse.stable_sorting_text("123_456_789")
        )

    def test_any_text(self):
        self.refresh_sorters()
        self.assertEqual(
            "aaa_1_bbb_aaa_ccc\naaa_2_ccc_aaa_bbb\nbbb_0_aaa_bbb_ccc",
            self.sorter.stable_sorting_text(
                "aaa_bbb_ccc\nbbb_aaa_ccc\nccc_aaa_bbb")
        )
        self.assertEqual(
            "bbb_0_aaa_bbb_ccc\naaa_2_ccc_aaa_bbb\naaa_1_bbb_aaa_ccc",
            self.sorter_reverse.stable_sorting_text(
                "aaa_bbb_ccc\nbbb_aaa_ccc\nccc_aaa_bbb")
        )


class TestSortText(unittest.TestCase):
    multisorter = Sorter(input_file_name="", is_reverse=False,
                         is_multisorting=True, separators="_")
    stable_sorter1 = Sorter(input_file_name="", is_reverse=False,
                            is_multisorting=False, separators="_",
                            column_for_sort=2)
    stable_sorter2 = Sorter(input_file_name="", is_reverse=False,
                            is_multisorting=False, separators="_",
                            column_for_sort=2)

    def refresh_sorter(self):
        self.stable_sorter1.string_counter = 0
        self.stable_sorter2.string_counter = 0

    def test_empty_string(self):
        self.refresh_sorter()
        self.assertEqual(
            self.multisorter.multisorting_text(""),
            self.multisorter.sort_text("")
        )
        self.assertEqual(
            self.stable_sorter1.stable_sorting_text(""),
            self.stable_sorter2.sort_text("")
        )

    def test_text_with_single_string(self):
        self.refresh_sorter()
        self.assertEqual(
            self.multisorter.multisorting_text("123_456_789"),
            self.multisorter.sort_text("123_456_789")
        )
        self.assertEqual(
            self.stable_sorter1.stable_sorting_text("123_456_789"),
            self.stable_sorter2.sort_text("123_456_789")
        )

    def test_text_with_any_string(self):
        self.refresh_sorter()
        self.assertEqual(
            self.multisorter.multisorting_text(
                "aaa_1_bbb_aaa_ccc\naaa_2_ccc_aaa_bbb\nbbb_0_aaa_bbb_ccc"),
            self.multisorter.sort_text(
                "aaa_1_bbb_aaa_ccc\naaa_2_ccc_aaa_bbb\nbbb_0_aaa_bbb_ccc")
        )
        self.assertEqual(
            self.stable_sorter1.stable_sorting_text(
                "aaa_1_bbb_aaa_ccc\naaa_2_ccc_aaa_bbb\nbbb_0_aaa_bbb_ccc"),
            self.stable_sorter2.sort_text(
                "aaa_1_bbb_aaa_ccc\naaa_2_ccc_aaa_bbb\nbbb_0_aaa_bbb_ccc")
        )


class TestSplitFileIntoSortedTmpFiles(unittest.TestCase):
    @staticmethod
    def create_file_for_check(text):
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        input_file = open("test.txt", "w")
        input_file.write(text)
        input_file.close()

    def test_empty_file(self):
        self.create_file_for_check("")
        sorter = Sorter(input_file_name="test.txt", separators="_")
        sorter.split_file_into_sorted_tmp_files()
        os.chdir(sorter.path_tmp_dir)
        tmp_file_0 = open("0.tmp", "r")
        self.assertEqual("", tmp_file_0.read())
        tmp_file_0.close()

    def test_file_with_single_string(self):
        self.create_file_for_check("1_2_345_a")
        multisorter = Sorter(input_file_name="test.txt", separators="_")
        stable_sorter = Sorter(input_file_name="test.txt", separators="_",
                               is_multisorting=False, column_for_sort=2)

        multisorter.split_file_into_sorted_tmp_files()
        os.chdir(multisorter.path_tmp_dir)
        tmp_file_0 = open("0.tmp", "r")
        self.assertEqual("1_2_345_a", tmp_file_0.read())
        tmp_file_0.close()

        stable_sorter.split_file_into_sorted_tmp_files()
        os.chdir(stable_sorter.path_tmp_dir)
        tmp_file_0 = open("0.tmp", "r")
        self.assertEqual("2_0_1_2_345_a", tmp_file_0.read())
        tmp_file_0.close()

    def test_file_with_3_string(self):
        self.create_file_for_check("aaa_ccc_bbb\nccc_bbb_aaa\nbbb_ccc_aaa")
        multisorter = Sorter(input_file_name="test.txt", separators="_",
                             strings_in_tmp_file=1)
        stable_sorter = Sorter(input_file_name="test.txt", separators="_",
                               is_multisorting=False, column_for_sort=2,
                               strings_in_tmp_file=1)

        multisorter.split_file_into_sorted_tmp_files()
        os.chdir(multisorter.path_tmp_dir)
        tmp_file_0 = open("0.tmp", "r")
        tmp_file_1 = open("1.tmp", "r")
        tmp_file_2 = open("2.tmp", "r")
        self.assertEqual("aaa_ccc_bbb", tmp_file_0.read())
        self.assertEqual("ccc_bbb_aaa", tmp_file_1.read())
        self.assertEqual("bbb_ccc_aaa", tmp_file_2.read())
        tmp_file_0.close()
        tmp_file_1.close()
        tmp_file_2.close()

        os.chdir(stable_sorter.path_tmp_dir)
        stable_sorter.split_file_into_sorted_tmp_files()
        tmp_file_0 = open("0.tmp", "r")
        tmp_file_1 = open("1.tmp", "r")
        tmp_file_2 = open("2.tmp", "r")
        self.assertEqual("ccc_0_aaa_ccc_bbb", tmp_file_0.read())
        self.assertEqual("bbb_1_ccc_bbb_aaa", tmp_file_1.read())
        self.assertEqual("ccc_2_bbb_ccc_aaa", tmp_file_2.read())
        tmp_file_0.close()
        tmp_file_1.close()
        tmp_file_2.close()
        self.assertEqual(
            len(stable_sorter.tmp_files_names),
            3
        )

    def test_with_4_strig_and_sorting(self):
        self.create_file_for_check(
            "ccc_bbb_aaa\naaa_ccc_bbb\nbbb_ccc_aaa\naaa_bbb_ccc")
        multisorter = Sorter(input_file_name="test.txt", separators="_",
                             strings_in_tmp_file=2)
        stable_sorter = Sorter(input_file_name="test.txt", separators="_",
                               is_multisorting=False, column_for_sort=2,
                               strings_in_tmp_file=2)

        multisorter.split_file_into_sorted_tmp_files()
        os.chdir(multisorter.path_tmp_dir)
        tmp_file_0 = open("0.tmp", "r")
        tmp_file_1 = open("1.tmp", "r")
        self.assertEqual("aaa_ccc_bbb\nccc_bbb_aaa", tmp_file_0.read())
        self.assertEqual("aaa_bbb_ccc\nbbb_ccc_aaa", tmp_file_1.read())
        tmp_file_0.close()
        tmp_file_1.close()

        os.chdir(stable_sorter.path_tmp_dir)
        stable_sorter.split_file_into_sorted_tmp_files()
        tmp_file_0 = open("0.tmp", "r")
        tmp_file_1 = open("1.tmp", "r")
        self.assertEqual("bbb_0_ccc_bbb_aaa\nccc_1_aaa_ccc_bbb",
                         tmp_file_0.read())
        self.assertEqual("bbb_3_aaa_bbb_ccc\nccc_2_bbb_ccc_aaa",
                         tmp_file_1.read())
        tmp_file_0.close()
        tmp_file_1.close()
        self.assertEqual(
            len(stable_sorter.tmp_files_names),
            2
        )


class TestCompareForMultisorting(unittest.TestCase):
    sorter = Sorter(input_file_name="", separators="_")

    def make_test(self, result, strings):
        self.assertEqual(
            result,
            self.sorter.compare_for_multisorting(strings)
        )

    def test_single_string(self):
        self.make_test(0, [""])
        self.make_test(0, ["a"])

    def test_string_with_empty_string(self):
        self.make_test(1, ["a", "", "b"])
        self.make_test(0, ["", "b"])
        self.make_test(2, ["4", "tr", "", ""])

    def test_some_strings(self):
        self.make_test(0, ["a", "b", "c"])
        self.make_test(2, ["a_b_c", "a_b", "a"])
        self.make_test(1, ["ab", "aa", "ad"])
        self.make_test(0, ["a_bz", "aaaa"])
        self.make_test(0, ["a_BZ", "aAAA"])

    def test_with_reverse(self):
        self.sorter.is_reverse = True
        self.make_test(0, [""])
        self.make_test(0, ["a"])
        self.make_test(2, ["a", "", "b"])
        self.make_test(1, ["", "b"])
        self.make_test(1, ["4", "tr", "", ""])
        self.make_test(2, ["a", "b", "c"])
        self.make_test(0, ["a_b_c", "a_b", "a"])
        self.make_test(2, ["ab", "aa", "ad"])
        self.make_test(1, ["a_bz", "aaaa"])
        self.make_test(1, ["a_bz", "A_zz"])
        self.sorter.is_reverse = False


class TestCompareForStableSorting(unittest.TestCase):
    sorter = Sorter(input_file_name="", separators="_", is_multisorting=False,
                    column_for_sort=2)

    def make_test(self, result, strings):
        self.assertEqual(
            result,
            self.sorter.compare_for_stable_sorting(strings)
        )

    def test_single_string(self):
        self.make_test(0, ["a_324_a_a"])
        self.make_test(0, ["_0_"])

    def test_with_empty_strings(self):
        self.make_test(0, ["_4_", "aa_45_br_45"])
        self.make_test(1, ["aa_35_eg", "_7_"])

    def test_any_strings(self):
        self.make_test(0, ["a_4_b_a", "b_3_a_b"])
        self.make_test(1, ["b_4_a_b", "b_3_c_b"])
        self.make_test(2, ["a_4_b_a", "b_3_a_b", "a_0_b_a"])
        self.make_test(0, ["a_4_bc", "a_12_fx"])
        self.make_test(1, ["a_10_b", "a_2_b"])
        self.make_test(1, ["A_10_b", "a_2_b"])
        self.make_test(1, ["a_10_b", "A_2_b"])

    def test_all_with_reverse(self):
        self.sorter.is_reverse = True
        self.make_test(0, ["a_324_a_a"])
        self.make_test(0, ["_0_"])
        self.make_test(1, ["_4_", "aa_45_br_45"])
        self.make_test(0, ["aa_35_eg", "_7_"])
        self.make_test(1, ["a_4_b_a", "b_3_a_b"])
        self.make_test(0, ["b_4_a_b", "b_3_c_b"])
        self.make_test(1, ["a_4_b_a", "b_3_a_b", "a_0_b_a"])
        self.make_test(1, ["a_4_bc", "a_12_fx"])
        self.sorter.is_reverse = False


class TestCompareStrings(unittest.TestCase):
    multisorter = Sorter(input_file_name="", separators="_")
    stable_sorter = Sorter(input_file_name="", separators="_",
                           is_multisorting=False, column_for_sort=2)

    def make_test_multisorting(self, strings):
        self.assertEqual(
            self.multisorter.compare_for_multisorting(strings),
            self.multisorter.compare_strings(strings)
        )

    def make_test_stable_sorting(self, strings):
        self.assertEqual(
            self.stable_sorter.compare_for_stable_sorting(strings),
            self.stable_sorter.compare_strings(strings)
        )

    def test_multisorting(self):
        self.make_test_multisorting([""])
        self.make_test_multisorting(["a"])
        self.make_test_multisorting(["a", "", "b"])
        self.make_test_multisorting(["", "b"])
        self.make_test_multisorting(["4", "tr", "", ""])
        self.make_test_multisorting(["a", "b", "c"])
        self.make_test_multisorting(["a_b_c", "a_b", "a"])
        self.make_test_multisorting(["ab", "aa", "ad"])
        self.make_test_multisorting(["a_bz", "aaaa"])

        self.multisorter.is_reverse = True
        self.make_test_multisorting([""])
        self.make_test_multisorting(["a"])
        self.make_test_multisorting(["a", "", "b"])
        self.make_test_multisorting(["", "b"])
        self.make_test_multisorting(["4", "tr", "", ""])
        self.make_test_multisorting(["a", "b", "c"])
        self.make_test_multisorting(["a_b_c", "a_b", "a"])
        self.make_test_multisorting(["ab", "aa", "ad"])
        self.make_test_multisorting(["a_bz", "aaaa"])

    def test_stable_sorting(self):
        self.make_test_stable_sorting(["a_324_a_a"])
        self.make_test_stable_sorting(["_0_"])
        self.make_test_stable_sorting(["_4_", "aa_45_br_45"])
        self.make_test_stable_sorting(["aa_35_eg", "_7_"])
        self.make_test_stable_sorting(["a_4_b_a", "b_3_a_b"])
        self.make_test_stable_sorting(["b_4_a_b", "b_3_c_b"])
        self.make_test_stable_sorting(["a_4_b_a", "b_3_a_b", "a_0_b_a"])
        self.make_test_stable_sorting(["a_4_bc", "a_12_fx"])

        self.stable_sorter.is_reverse = True
        self.make_test_stable_sorting(["a_324_a_a"])
        self.make_test_stable_sorting(["_0_"])
        self.make_test_stable_sorting(["_4_", "aa_45_br_45"])
        self.make_test_stable_sorting(["aa_35_eg", "_7_"])
        self.make_test_stable_sorting(["a_4_b_a", "b_3_a_b"])
        self.make_test_stable_sorting(["b_4_a_b", "b_3_c_b"])
        self.make_test_stable_sorting(["a_4_b_a", "b_3_a_b", "a_0_b_a"])
        self.make_test_stable_sorting(["a_4_bc", "a_12_fx"])


class TestMergingAnyFiles(unittest.TestCase):
    @staticmethod
    def prepare_to_check(sorter, texts):
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        sorter.path_tmp_dir = tmp_dir
        counter = 0
        for text in texts:
            input_file = open(str(counter) + ".tmp", "w")
            counter += 1
            sorter.tmp_file_counter += 1
            sorter.tmp_files_names.append(input_file.name)
            input_file.write(text)
            input_file.close()

    def make_test(self, texts, count_of_merging, result, reverse=False,
                  multisorting=True):
        sorter = Sorter(input_file_name="", separators="_", is_reverse=reverse,
                        is_multisorting=multisorting, column_for_sort=2)
        self.prepare_to_check(sorter, texts)
        tmp_files_counter = sorter.tmp_file_counter
        sorter.merging_any_tmp_files(count_of_merging)
        self.assertTrue(sorter.tmp_file_counter - 1 == tmp_files_counter)

        self.assertTrue(
            len(sorter.tmp_files_names) == len(texts) - count_of_merging + 1)
        self.assertTrue(str(len(texts)) + ".tmp" in sorter.tmp_files_names)
        result_file = open(str(len(texts)) + ".tmp", 'r')
        self.assertEqual(
            result,
            result_file.read()
        )
        result_file.close()

    def test_empty_files(self):
        self.make_test(["", ""], 2, "")
        self.make_test(["", "", ""], 3, "")

    def test_two_file_with_single_strings(self):
        self.make_test(["cba", "abc"], 2, "abc\ncba")
        self.make_test(["abc", "cba"], 2, "abc\ncba")
        self.make_test(["A_z", "aa_z"], 2, "A_z\naa_z")

    def test_three_files_with_single_strings(self):
        self.make_test(["c", "a", "b"], 3, "a\nb\nc")
        self.make_test(["C", "A", "b"], 3, "A\nb\nC")

    def test_files_more_then_count_of_merging(self):
        self.make_test(["c", "a", "b"], 2, "a\nc")
        self.make_test(["c", "Z", "a", "b"], 2, "c\nZ")

    def test_files_with_two_strings(self):
        self.make_test(["a\nb", "c\nd"], 2, "a\nb\nc\nd")
        self.make_test(["a\nd", "b\nc"], 2, "a\nb\nc\nd")

    def test_different_count_strings_in_files(self):
        self.make_test(["a\nz", "b\nc\nd\ne", "u"], 3, "a\nb\nc\nd\ne\nu\nz")
        self.make_test(["a\nz", "b\nc\nD\ne", "U"], 3, "a\nb\nc\nD\ne\nU\nz")

    def test_reverse(self):
        self.make_test(["z\na", "e\nd\nc\nb", "u"], 3, "z\nu\ne\nd\nc\nb\na",
                       reverse=True)
        self.make_test(["z\na", "e\nD\nc\nb", "U"], 3, "z\nU\ne\nD\nc\nb\na",
                       reverse=True)

    def test_any_texts_with_stable_sorting(self):
        self.make_test(["_0_", "_1_"], 2, "_0_\n_1_", multisorting=False)
        self.make_test(["_10_", "_0_", "_2_"], 3, "_0_\n_2_\n_10_",
                       multisorting=False)
        self.make_test(["a_1_cba", "a_0_abc"], 2, "a_0_abc\na_1_cba",
                       multisorting=False)


class TestPrepareStableSortingFileToReplace(unittest.TestCase):

    def make_test(self, text, result):
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        tmp_file = open("4.tmp", "w")
        tmp_file.write(text)
        tmp_file.close()
        sorter = Sorter(input_file_name="", separators="_",
                        is_multisorting=False, column_for_sort=2)
        sorter.path_tmp_dir = tmp_dir
        sorter.prepare_stable_sorting_file_to_replace("4.tmp")
        tmp_file = open("4.tmp", "r")
        self.assertEqual(
            result,
            tmp_file.read()
        )
        tmp_file.close()

    def test_empty_file(self):
        self.make_test("_0_", "")

    def test_single_string_file(self):
        self.make_test("aa_5_bb_aa_c", "bb_aa_c")

    def test_any_files_with_any_strings(self):
        self.make_test("a_0_a\nb_1_b\nc_2_c", "a\nb\nc")
        self.make_test("1_1_1\n2_2_2\n3_3_3", "1\n2\n3")


class TestReplaceInputFileWithResultFile(unittest.TestCase):
    def make_test(self, text):
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        tmp_file = open("4.tmp", "w")
        tmp_file.write(text)
        tmp_file.close()
        sorter = Sorter(input_file_name="wow.txt", separators="_",
                        is_multisorting=False, column_for_sort=2)
        sorter.path_tmp_dir = tmp_dir
        sorter.replace_input_file_with_result_file("4.tmp")
        sorter.path_input_file = tmp_dir

        main_file = open("wow.txt", 'r')
        self.assertEqual(
            text,
            main_file.read()
        )
        main_file.close()

    def test_any_files(self):
        self.make_test("")
        self.make_test("123")
        self.make_test("1\n2\n3")
        self.make_test("abc\ncba")


class TestMergingAllTmpFiles(unittest.TestCase):
    def do_tests(self, texts, result):
        sorter = Sorter(input_file_name="", separators="_")
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        sorter.path_tmp_dir = tmp_dir
        counter = 0
        for text in texts:
            input_file = open(str(counter) + ".tmp", "w")
            counter += 1
            sorter.tmp_file_counter += 1
            sorter.tmp_files_names.append(input_file.name)
            input_file.write(text)
            input_file.close()

        sorter.merging_all_tmp_files()
        result_file = open(sorter.tmp_files_names[0], 'r')
        self.assertEqual(
            result,
            result_file.read()
        )
        result_file.close()

    def test_single_file(self):
        self.do_tests(['a'], 'a')
        self.do_tests(['a\nb'], 'a\nb')

    def test_two_files(self):
        self.do_tests(['a', 'b'], 'a\nb')
        self.do_tests(['a\nb', 'c\nd'], 'a\nb\nc\nd')
        self.do_tests(['a\nc', 'b\nd'], 'a\nb\nc\nd')

    def test_three_files(self):
        self.do_tests(['a', 'b', 'c'], 'a\nb\nc')
        self.do_tests(['a\na', 'b\nb', 'c\nc'], 'a\na\nb\nb\nc\nc')

    def test_many_files(self):
        self.do_tests(['a', 'b', 'c', 'd', 'e'], 'a\nb\nc\nd\ne')


class TestSort(unittest.TestCase):
    random_words = ["tendency", "reverse", "game", "particle", "quest",
                    "braid",
                    "girlfriend", "deter", "jury", "church", "foster",
                    "mourning", "advance", "adviser", "spider", "couple",
                    "high", "explode", "appear", "charity", "nomination",
                    "notorious", "possible", "houseplant", "staircase",
                    "acceptable", "restrict", "conscious", "tin", "marine",
                    "glide", "capital", "margin", "cabinet", "plead", "floor",
                    "owner", "fail", "velvet", ]

    def create_random_file(self, file_name, strings_count,
                           max_words_in_string):
        file = open(file_name, 'w')
        for i in range(strings_count):
            string = ""
            for j in range(randint(1, max_words_in_string)):
                string += self.random_words[
                              randint(0, len(self.random_words) - 1)] + " "
            string = string[:-1] + "\n"
            file.write(string)
        file.close()

    def do_test(self):
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)
        self.create_random_file("test.txt", 5000, 30)
        sorter = Sorter(input_file_name="test.txt", separators=" ")
        sorter.strings_in_tmp_file = 50
        sorter.sort()
        result_file = open("test.txt", 'r')
        previous_string = result_file.readline().replace("\n", "")
        current_string = result_file.readline().replace("\n", "")
        while current_string != "":
            self.assertEqual(0, sorter.compare_strings(
                [previous_string, current_string]))
            previous_string = current_string
            current_string = result_file.readline().replace("\n", "")
        result_file.close()

    def test_all_sorter(self):
        for i in range(100):
            self.do_test()

if __name__ == '__main__':
    unittest.main()
