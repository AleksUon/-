class FiniteAutomaton:
    def __init__(self):
        self.states = {1, 2, 3, 4, 5, 6, 7, 8}  # Набор состояний
        self.initial_state = 1  # Начальное состояние
        self.final_states = {5, 6, 7, 8}  # Конечные состояния

        # Функции перехода (текущее состояние, вводимый символ) -> следующее состояние
        self.transition_function = {
            (1, 'a'): 2,
            (2, 'a'): 3,
            (2, 'b'): 4,
            (3, 'a'): 5,
            (3, 'b'): 6,
            (3, 'a'): 7,
            (5, 'a'): 5,
            (5, 'b'): 6,
            (6, 'a'): 7,
            (6, 'b'): 8,
            (4, 'b'): 8,
            (4, 'a'): 7,
            (7, 'b'): 2,
            (8, 'a'): 2,
            (8, 'b'): 1
        }

    def process_input(self, input_string):
        current_state = self.initial_state

        for char in input_string:
            # Проверяем, есть ли переход для текущего состояния и символа
            if (current_state, char) in self.transition_function:
                current_state = self.transition_function[(current_state, char)]
            else:
                # Нет доступного перехода - завершаем обработку
                return False

        # Проверяем, достигли ли мы конечного состояния
        return current_state in self.final_states


if __name__ == "__main__":
    fa = FiniteAutomaton()
    input_string = input("Введите строку для анализа: ")

    if fa.process_input(input_string):
        print("Строка принята.")
    else:
        print("Строка не принята.")
