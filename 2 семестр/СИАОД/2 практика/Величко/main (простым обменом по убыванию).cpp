#include <iostream>
#include <random>
#include <chrono>
#include <algorithm>

using namespace std;

void swap(int& a, int& b){  // обмен значениями
    int temp = a;
    a = b;
    b = temp;
}

void ExchangeSort(int A[], int n, long long& operation) {  // сортировка обменом
    for (int i = 0; i < n - 1; ++i) {
        operation++;
        
        for (int j = 0; j < n - i - 1; ++j) {
            operation++;
            
            if (A[j] > A[j + 1]) {
                swap(A[j], A[j + 1]);
                operation++;
            }
           operation++;
           
        }
        operation++;
        
    }
    operation++;
    
}

int main() {
    int num;
    cout << "Enter the array size: ";
    cin >> num;
    int* array = new int[num];//Динамическое выделение памяти
    long long oper = 0;
    
    mt19937 gen(random_device{}());//генератор случайных чисел
    uniform_int_distribution<int> dist(0, 9); //для заданного диапазона
    
    cout << "Generated array:" << endl;
    for (int i = 0; i < num; i++) {
        array[i] = dist(gen);
        cout << array[i] << " ";
    }
    
    cout << endl;
    cout << "Sorted array: " << endl;
    sort(array, array + num, greater<int>());//сортировка по убыванию
    
    for (int i = 0; i < num; ++i) {
        cout << array[i] << " ";
    }
    cout << endl;
    
    auto start = chrono::high_resolution_clock::now();//засекание времени
    
    ExchangeSort(array, num, oper);//сортировка обменом
    
    auto end = chrono::high_resolution_clock::now();//окончание засекания времени
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
    
    cout << "Sorted array: " << endl;
    for (int i = 0; i < num; ++i) {
        cout << array[i] << " ";
    }
    
    cout << endl;
    cout << "Number of comparison and assignment operations performed: " << oper << endl;
    cout << "Sorting took " << duration << " nanoseconds" << endl;
    delete[] array;  // Освобождение памяти
    return 0;
}
