# Задание 1

Эмпирическая оценка эффективности алгоритмов.

1. Разработать алгоритм Шелла со смещениями Д. Кнута вторым способом, реализовать код на языке С++. Сформировать таблицу 1.1 результатов эмпирической оценки сложности сортировки по формату табл. 1 для массива, заполненного случайными числами.
2. Определить ёмкостную сложность алгоритма Шелла со смещениями Д. Кнута вторым способом.
3. Разработать алгоритм простого слияния, реализовать код на языке С++. Сформировать таблицу 1.2 результатов эмпирической оценки сортировки по формату табл. 1 для массива, заполненного случайными числами.
4. Определить ёмкостную сложность алгоритма быстрой сортировки (Хоара).
5. Добавьте в отчёт данные по работе любого из алгоритмов простой сортировки в среднем случае, полученные в предыдущей практической работе (в отчёте – таблица 1.3).
6. Представить на общем сравнительном графике зависимости Тп(n)=Cф+Mф для трёх анализируемых алгоритмов. График должен быть подписан, на нём – обозначены оси.
7. На основе сравнения полученных данных определите наиболее эффективный из алгоритмов в среднем случае (отдельно для небольших массивов при n до 1000 и для больших массивов с n>1000).
8. Провести дополнительные прогоны программ ускоренной и быстрой сортировок на массивах, отсортированных а) строго в убывающем и б) строго возрастающем порядке значений элементов. Заполнить по этим данным соответствующие таблицы 1.4, 1.5 для каждого алгоритма по формату табл. 1.
9. Сделайте вывод о зависимости (или независимости) алгоритмов сортировок от исходной упорядоченности массива на основе результатов, представленных в таблицах.

# Задание 2

Асимптотический анализ сложности алгоритмов

Требования по выполнению задания

1. Из материалов предыдущей практической работы приведите в отчёте формулы Тт(n) функций роста алгоритма простой сортировки обменом в лучшем и худшем случае.
2. На основе определений соответствующих нотаций получите асимптотическую оценку вычислительной сложности простого алгоритма сортировки обменом:
- в О-нотации (оценка сверху) для анализа худшего случая;
- в Ω-нотации (оценка снизу) для анализа лучшего случая.
3. Получите (если это возможно) асимптотически точную оценку вычислительной сложности алгоритма в нотации θ.
4. Реализуйте графическое представление функции роста и полученных асимптотических оценок сверху и снизу.
5. Привести справочную информацию о вычислительной сложности алгоритмов шейкерной сортировки и быстрой сортировки (Хоара).
6. Общие результаты свести в табл. 2.
7. Сделать вывод о наиболее эффективном алгоритме из трёх.
