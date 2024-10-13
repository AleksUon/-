#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>

using namespace std;

void InsertionSort(vector<int>& values, long& operations) {
    for (size_t i = 1; i < values.size(); ++i) {
        int x = values[i];
        size_t j = i;
        
        while (j > 0 && values[j - 1] > x) {
            values[j] = values[j - 1];
            --j;
            operations += 3; // увеличиваем операции на 3 (сравниение при входе в цикл,присваивание и декремент)
        }
        values[j] = x;
        operations += 5; // увеличиваем операции на 5 (сравниение при входе в цикл, присваивание 3 раза, сравнение при выходе из цикла)
    
    }
    ++operations; // увеличиваем операции на 1 (сравнение при выходе из цикла)
    
}

int main() {
    long operations = 0;
    int n,a;
    cout << "Введите n: ";
    cin >> n;
    vector<int> A(n);
    cout << "Введите 1 (для случайной генерации чисел) или 2 (для ручного ввода) : ";
    cin >> a;
    
    if (a == 1) {
        mt19937 gen(random_device{}()); //mt19937 gen-генератор случайных чисел. random_device{}- класс, формирует случайную последовательность с помощью внешнего устройства.
        uniform_int_distribution<int> dist(1, 10); //инструмент, позволяющий генерировать случайное целое число в заданном диапазоне
        
        cout << "Массив:" << endl;
        for (int i = 0; i < n; i++) { // i принимает значения от 0 до n включительно. 
            A[i] = dist(gen);
            cout << A[i] << " ";
        } cout << endl;
        
    } else if (a == 2) {// i принимает значения от 0 до n включительно. 
        cout << "Введите элементы массива:" << endl;
        for (int i = 0; i < n; i++) {
            cin >> A[i];
        }cout << endl;
        
    } else {
        cout << "Error";
        
        return 0;
    }
    
    sort(A.begin(), A.end(), greater<int>());
    
    auto start = chrono::high_resolution_clock::now();// Замер времени начала сортировки
    
    InsertionSort(A, operations); //вызов функции сортировки массива
    
    auto end = chrono::high_resolution_clock::now();// Замер времени окончания сортировки
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();//подсчёт затраченного превени сортировки
    
    cout << "Сортированный массив:\n";//вывод массива
    for (int i = 0; i < n; ++i) {
        cout << A[i] << " ";
    } 
    
    cout << endl;
    cout << "Было совершено операций сравнения и присваивания: " << operations << endl;
    cout << "Сортировка заняла " << duration << " микросекунд" << endl;// Вывод времени сортировки (в миллисекундах)
    
    return 0;
}
