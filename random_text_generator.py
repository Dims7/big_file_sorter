import random


class RandomTextGenerator:
    words = []

    def __init__(self):
        with open('words.txt', 'r') as f:
            self.words = f.read().split("\n")

    def _get_random_word(self):
        return self.words[random.randint(0, len(self.words) - 1)]

    def generate_random_text(self, file_name, words_in_one_string,
                             strings_count, separator):
        with open(file_name, 'w') as f:
            for string_counter in range(strings_count):
                string = ''
                for word_counter in range(words_in_one_string):
                    string += self._get_random_word() + separator
                string = string[:-len(separator)] + '\n'
                f.write(string)
        print("Generating complete.")
