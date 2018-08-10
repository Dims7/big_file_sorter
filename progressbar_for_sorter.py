import progressbar


# ToDo оптимизировать код
class ProgressbarForSorter:
    current_value = None
    bar = None
    tmp_list = []

    list_with_merge_costs = []
    list_with_sort_costs = []

    counter = 0

    def get_max_value(self):
        return sum(self.list_with_merge_costs) + sum(self.list_with_sort_costs)

    def fill_tmp_list(self, strings_count, strings_in_tmp_file):
        while strings_count != 0:
            if strings_count > strings_in_tmp_file:
                self.tmp_list.append(strings_in_tmp_file)
                self.list_with_sort_costs.append(strings_in_tmp_file)
                strings_count -= strings_in_tmp_file
            else:
                self.tmp_list.append(strings_count)
                self.list_with_sort_costs.append(strings_count)
                strings_count = 0

    def fill_list_with_update_costs(self, merge_files_for_step):
        if len(self.tmp_list) == 1:
            self.list_with_merge_costs.append(0)

        while len(self.tmp_list) != 1:
            merge_count = min(merge_files_for_step, len(self.tmp_list))
            sum = 0
            for _ in range(merge_count):
                sum += self.tmp_list.pop(0)
            self.tmp_list.append(sum)
            self.list_with_merge_costs.append(sum)

    def __init__(self, filename, strings_in_one_step, merging_in_one_step):
        self.current_value = 0
        strings_count = self.get_strings_count(filename)
        self.fill_tmp_list(strings_count, strings_in_one_step)
        self.fill_list_with_update_costs(merging_in_one_step)
        max_value = self.get_max_value()
        self.bar = progressbar.ProgressBar(max_value=max_value)

    def update_for_compare(self):
        self.current_value += 1
        self.bar.update(self.current_value)

    def update_for_sorter(self):
        self.current_value += self.list_with_sort_costs.pop(0)
        self.bar.update(self.current_value)

    @staticmethod
    def get_strings_count(filename):
        with open(filename, 'r') as f:
            return len(f.readlines())
