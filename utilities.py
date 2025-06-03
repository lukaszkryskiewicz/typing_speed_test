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

def compare_input(pattern, user_input, key, words_list):
    user_input_list = user_input.split(' ')
    current_word_index = len(user_input_list) - 1
    current_char_index = len(user_input_list[current_word_index]) - 1
    i = len(user_input_list[current_word_index])

    current_pattern_word = words_list[current_word_index]
    current_user_input_word = user_input_list[current_word_index]

    # counts length of all previous words in a words_list and adds current_word_index value for spaces
    base_offset = sum(len(words) for words in words_list[:current_word_index]) + current_word_index

    if key == 'BackSpace':
        start_del = f"1.0+{base_offset + current_char_index +1}c"
        end_del = f"1.0+{base_offset + current_char_index + 2}c"
        pattern.tag_remove("correct", start_del, end_del)
        pattern.tag_remove("wrong", start_del, end_del)
        pattern.tag_add('raw', start_del, end_del)

    if current_char_index < 0 or i > len(current_pattern_word):
        return

    for idx in range(i):
        correct = user_input_list[current_word_index][idx] == current_pattern_word[idx]
        tag = 'correct' if correct else 'wrong'
        char_offset = base_offset + idx

        #forced by tkinter to use such fstring
        start_i = f"1.0+{char_offset}c"
        end_i = f"1.0+{char_offset + 1}c"

        pattern.tag_remove("raw", start_i, end_i)
        pattern.tag_add(tag, start_i, end_i)
