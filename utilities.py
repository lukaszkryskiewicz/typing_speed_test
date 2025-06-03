import requests


def generate_words():
    url ='https://random-word-api.herokuapp.com/word'
    params = {
        'length': 7,
        'number': 25,
    }

    try:
        response = requests.get(url, params)
    except:
        print('No data returned')
        return

    return response.json()

def compare_input(pattern, user_input, key, words_list, previous_char, update_cpm):
    user_input_list = user_input.split(' ')
    current_word_index = len(user_input_list) - 1
    current_char_index = len(user_input_list[current_word_index]) - 1
    i = len(user_input_list[current_word_index])
    current_pattern_word = words_list[current_word_index]
    current_user_input_word = user_input_list[current_word_index]

    # counts length of all previous words in a words_list and adds current_word_index value for spaces
    base_offset = sum(len(words) for words in words_list[:current_word_index]) + current_word_index

    # changes formatting to default in case deleting letter or space
    if key == 'BackSpace':
        start_del = f"1.0+{base_offset + current_char_index +1}c"
        end_del = f"1.0+{base_offset + current_char_index + 2}c"
        pattern.tag_remove("correct_letter", start_del, end_del)
        pattern.tag_remove("wrong_letter", start_del, end_del)
        pattern.tag_add('raw', start_del, end_del)
        if previous_char == ' ':
            pattern.tag_remove("correct_word", f"1.0+{base_offset}c", f"1.0+{base_offset + len(current_pattern_word)}c")
            pattern.tag_remove("wrong_word", f"1.0+{base_offset}c", f"1.0+{base_offset + len(current_pattern_word)}c")

            if user_input_list[current_word_index] == words_list[current_word_index]:
                update_cpm(- len(words_list[current_word_index]))

    # highlights correct and incorrect words
    if key == 'space':
        correct_word = user_input_list[current_word_index-1] == words_list[current_word_index-1]
        tag = 'correct_word' if correct_word else 'wrong_word'
        word_offset = sum(len(words) for words in words_list[:current_word_index-1]) + (current_word_index - 1)

        start_index_word = f'1.0+{word_offset}c'
        end_index_word = f'1.0+{word_offset + len(words_list[current_word_index-1])}c'

        pattern.tag_remove("correct_letter", start_index_word, end_index_word)
        pattern.tag_remove("wrong_letter", start_index_word, end_index_word)
        pattern.tag_add(tag, start_index_word, end_index_word)

        if correct_word:
            update_cpm(len(words_list[current_word_index-1]))

    if current_char_index < 0 or i > len(current_pattern_word):
        return

    # highlights correct and incorrect letters
    for idx in range(i):
        correct = current_user_input_word[idx] == current_pattern_word[idx]
        tag = 'correct_letter' if correct else 'wrong_letter'
        char_offset = base_offset + idx

        #forced by tkinter to use such fstring
        start_index = f"1.0+{char_offset}c"
        end_index = f"1.0+{char_offset + 1}c"

        pattern.tag_remove("raw", start_index, end_index)
        pattern.tag_add(tag, start_index, end_index)

