# Sudoku
This is my implementation of a [Sudoku](https://en.wikipedia.org/wiki/Sudoku) interface.  
It is capable of  creating and solving sudokus with basic sudoku logic.  
The current logic is:
- [Last possible number](https://sudoku.com/sudoku-rules/last-possible-number/)
- [Last remaining cell](https://sudoku.com/sudoku-rules/last-remaining-cell/)

## ToDo
- Implement more sudoku logic
    - [Naked pairs](https://sudoku.com/sudoku-rules/obvious-pairs/)
    - [Hidden pairs](https://sudoku.com/sudoku-rules/hidden-pairs/)
    - [X-wing](https://sudoku.com/sudoku-rules/h-wing/)
    - [Y-wing](https://sudoku.com/sudoku-rules/y-wing/)
    - [Swordfish](https://sudoku.com/sudoku-rules/swordfish/)
- Restructure to be more readable
- Separate into multiple files
- Add support for more sudoku sizes
- Add support for multiple Boards with shared borders or subcells
- Add support for forced solutions
- Possibly rewrite the solving algorithm