#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

// Создание матрицы
const int N = 5;
int matrix[N][N] = {0}; 
int countSolutions = 0; // Счётчик расстановок

// Смещения
int dx[] = {3, -3, 0, 0, 2, -2, 2, -2};
int dy[] = {0, 0, 3, -3, 2, -2, -2, 2};

// Проверка корректности координат
bool isValid(int x, int y) {
    return (x >= 0 && x < N && y >= 0 && y < N && matrix[x][y] == 0);
}

// Вывод матрицы
void printMatrix() {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cout << setw(3) << matrix[i][j] << " ";
        }
        cout << endl;
    }
    cout << "________________________________" << endl;
}

// Рекурсия для нумерации позиций
void branchAndBound(int x, int y, int num) {
    if (num > N * N) { // Все позиции пронумерованы
        countSolutions++;
        cout << "Расстановка #" << countSolutions << ":" << endl;
        printMatrix(); // Вывод матрицы после нахождения расстановки
        return;
    }

    for (int i = 0; i < 8; ++i) {
        int nx = x + dx[i];
        int ny = y + dy[i];
        
        if (isValid(nx, ny)) { // Если переход возможен
            matrix[nx][ny] = num; // Устанавливаем номер
            branchAndBound(nx, ny, num + 1); // Рекурсивный вызов для следующего номера
            matrix[nx][ny] = 0; // Возврат к предыдущему состоянию
        }
    }
}

int main() {
    for (int x = 1; x < N; ++x) {
        for (int y = 0; y < x; ++y) {
            matrix[x][y] = 1;
            branchAndBound(x, y, 2);
            matrix[x][y] = 0; // Сброс позиции
        }
    }

    cout << "Общее количество возможных расстановок: " << countSolutions << endl;
    return 0;
}
