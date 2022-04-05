import sys
import backtracking
import maze
import minSpanningTree
import solver


def print_info():
    print()
    print('Опции:')
    print('1. Для генерации лабиринта введите generate')
    print('2. Для загрузки сгенерированного лабиринта в файл введите download')
    print('3. Для чтения лабиринта из файла введите read')
    print('4. Для решения сгенерированного/загруженного лабиринта введите solve')
    print('5. Для выхода введите quit')
    print()


if __name__ == '__main__':
    print('Здравствуйте! Для начала генерации лабиринта, введите его желаемую высоту и ширину.')
    height = int(input('Bведите высоту: '))
    width = int(input('Введите ширину: '))
    print()

    if sys.argv[1] == 'backtracking':
        generator = backtracking.BacktrackingGenerator(height, width)
    elif sys.argv[1] == 'minimal_spanning_tree':
        generator = minSpanningTree.MinSpanningTreeGenerator(height, width)

    my_solver = solver.MazeSolver()

    print_info()

    query = input('Введите запрос: ')

    my_maze = maze.Maze(height, width)

    while query != 'quit':
        if query == 'generate':
            my_maze = generator.generate()
            my_maze.draw()
        if query == 'download':
            filename = 'generated_maze.txt'
            with open(filename, 'w') as file:
                my_maze.draw(file)
            print('\nВыполнено!')

        if query == 'read':
            filename = input('Введите имя файла для чтения: ')
            my_maze.read_maze_from_file(filename)
            my_maze.draw()
            print('\nВыполнено!')

        if query == 'solve':
            my_solver.solve(my_maze).draw()

        query = input('\nВведите запрос: ')

    print('\nДо свидания!')
