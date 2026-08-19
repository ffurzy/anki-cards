import random
import sys
import time

STOP_WORD = 'стоп'


def load_words(filename='words.txt'):
    """Читает файл со словами и возвращает словарь слово-перевод."""
    words = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # делим только по первой запятой
                parts = line.split(',', 1)
                if len(parts) != 2:
                    continue
                word = parts[0].strip()
                translation = parts[1].strip()
                words[word] = translation
    except FileNotFoundError:
        print('Не нашёл файл ' + filename)
        sys.exit(1)
    return words


def save_words(words, filename='words.txt'):
    """Записывает словарь обратно в файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(f'{word}, {words[word]}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}.')


def show_all_words(words):
    """Печатает все пары слово - перевод в одну строку."""
    pairs = []
    for word, translation in words.items():
        pairs.append(f'{word} - {translation}')
    print('; '.join(pairs))


def add_words(words):
    """Добавляет новые слова в словарь, пока не введут СТОП."""
    print(f'Чтобы закончить, введите {STOP_WORD.upper()}')
    while True:
        word = input('Введите слово: ').strip()
        if word.lower() == STOP_WORD:
            break
        translation = input('Введите перевод: ').strip()
        if translation.lower() == STOP_WORD:
            break
        words[word] = translation


def ask_and_check(word, correct):
    """Спрашивает перевод слова.

    Возвращает кортеж: (нужен ли выход, верно ли, время ответа).
    """
    print(f'Ваше слово: {word}')
    start = time.time()
    answer = input('Ваш перевод: ')
    finish = time.time()

    answer = answer.strip()
    if answer.lower() == STOP_WORD:
        return True, False, 0.0

    answer_time = finish - start
    is_correct = answer.lower() == correct.strip().lower()
    return False, is_correct, answer_time


def print_statistics(score, total_time):
    """Печатает счёт, общее и среднее время игры."""
    print(f'Ваш итоговый счёт: {score}')
    if score > 0:
        average = round(total_time / score, 2)
        print(f'Время игры: {total_time:.2f} секунд '
              f'(среднее время: {average} сек.)')
    else:
        # ни одного правильного ответа, среднее не посчитать
        print(f'Время игры: {total_time:.2f} секунд (среднее время: -)')


def start_game(words):
    """Обычная тренировка: переводим случайные слова до СТОП."""
    if not words:
        print('Словарь пустой, сначала добавьте слова.')
        return
    print(f'Чтобы закончить, введите {STOP_WORD.upper()}')

    score = 0
    total_time = 0.0
    all_words = list(words)

    while True:
        word = random.choice(all_words)
        need_exit, is_correct, answer_time = ask_and_check(
            word, words[word]
        )
        if need_exit:
            break
        total_time = total_time + answer_time
        if is_correct:
            score += 1
            print(f'Верно! Время на ответ: {answer_time:.2f} секунд')
        else:
            print(f'Неправильно, правильный ответ: {words[word]} '
                  f'(Время на ответ: {answer_time:.2f} секунд)')

    print('Спасибо за игру!')
    print_statistics(score, total_time)


def train_until_mistake(words):
    """Режим до первой ошибки."""
    if not words:
        print('Словарь пустой, сначала добавьте слова.')
        return
    print(f'\nРежим: игра до первой ошибки! '
          f'Чтобы выйти вручную, введите {STOP_WORD.upper()}\n')

    score = 0
    total_time = 0.0
    all_words = list(words)

    while True:
        word = random.choice(all_words)
        need_exit, is_correct, answer_time = ask_and_check(
            word, words[word]
        )
        if need_exit:
            print('Выход из режима по запросу пользователя.')
            break
        total_time += answer_time
        if not is_correct:
            print(f'Ошибка! Неверно. Правильный ответ: {words[word]}')
            break
        score += 1
        print(f'Верно! Всего очков: {score} '
              f'(ответ за {answer_time:.2f} секунд)')

    print_statistics(score, total_time)


def main():
    """Главное меню программы."""
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')

    while True:
        print('\nМеню:\n'
              '    1. Начать игру\n'
              '    2. Добавить слова\n'
              '    3. Тренировка до первой ошибки\n'
              '    4. Вывод всех слов\n'
              '    5. Выход\n')
        choice = input('Пункт меню: ').strip()

        if choice == '1':
            start_game(words)
        elif choice == '2':
            add_words(words)
        elif choice == '3':
            train_until_mistake(words)
        elif choice == '4':
            show_all_words(words)
        elif choice == '5':
            save_words(words)
            sys.exit()
        else:
            print('Неизвестный пункт меню')


main()