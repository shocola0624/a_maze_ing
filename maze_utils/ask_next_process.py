from typing import List
from .generate_maze import MazeGenerator
from config_utils.keys import ConfigData


BLACK = "\x1b[40m"
GREEN = "\x1b[42m"
BLUE = "\x1b[44m"
MAGENTA = "\x1b[45m"
CYAN = "\x1b[46m"
GRAY = "\x1b[47m"
RED = "\x1b[101m"
LIME = "\x1b[102m"
WHITE = "\x1b[107m"


def ask_next_process(
    expanded_maze: List[List[int]],
    config_data: ConfigData,
    config_path: str,
    scheme_index: int = 0,
    show_path: bool = False
) -> None:
    """
    Prompt for the next action and update the maze display/settings.

    Reads user input and may re-render the maze or call `main()` to
    regenerate; returns when the user quits/enters an invalid choice.

    Args:
        expanded_maze: Expanded maze grid.
        config_data: config_data: Config data obtained from the specific file.
        config_path: Path to the config file used to regenerate the maze.
        scheme_index: Current index for cycling predefined color schemes.
        show_path: Whether to render the shortest path.
    """
    print_maze = MazeGenerator.print_maze
    # 0 floor, 1 wall, 2 inside 42, 3 outside 42, 4 entry, 5 exit, 6 path
    color_schemes = [
        [BLACK, WHITE, GRAY, WHITE, MAGENTA, RED, CYAN],
        [BLACK, WHITE, LIME, GREEN, MAGENTA, RED, CYAN],
        [BLACK, WHITE, WHITE, LIME, MAGENTA, RED, RED],
        [WHITE, BLACK, LIME, BLACK, MAGENTA, RED, CYAN]
    ]
    color_scheme = color_schemes[scheme_index % len(color_schemes)]

    print("=== A-Maze-ing ===")
    print("1: Re-generate a new maze")
    print("2: Show/Hide path from entry to exit")
    print("3: Rotate maze colors")
    print("4: Set color scheme")
    print("Other: Quit")
    try:
        choice = int(input("Choice? (1-4): ").strip())
    except (Exception, KeyboardInterrupt):
        return

    if choice == 1:
        from a_maze_ing import main
        main(config_path)
    if choice == 2:
        show_path = not show_path
        print_maze(expanded_maze, config_data, color_scheme, show_path)
        ask_next_process(
            expanded_maze, config_data, config_path, scheme_index, show_path
        )
    if choice == 3:
        scheme_index += 1
        color_scheme = color_schemes[scheme_index % len(color_schemes)]
        print_maze(expanded_maze, config_data, color_scheme, show_path)
        ask_next_process(
            expanded_maze, config_data, config_path, scheme_index, show_path
        )
    if choice == 4:
        def ask_color_scheme(component: str) -> str:
            """Prompt for a color name for one maze component.

            Args:
                component: Name of the maze component to color.

            Returns:
                The ANSI color string mapped from the user's input.
                Re-prompts until a supported color is entered.
            """
            input_color = input(f"Color you chose for the {component}: ")
            try:
                return colors[input_color]
            except KeyError:
                return ask_color_scheme(component)
        colors = {
            "BLACK": BLACK,
            "GREEN": GREEN,
            "BLUE": BLUE,
            "MAGENTA": MAGENTA,
            "CYAN": CYAN,
            "GRAY": GRAY,
            "RED": RED,
            "LIME": LIME,
            "WHITE": WHITE
        }
        print("Supported colors:")
        for c in colors.keys():
            print(c, end=" ")
        print()

        color_scheme = []
        components = ("floor", "wall", "inside of 42", "outside of 42",
                      "entry", "exit", "shortest path")
        for c in components:
            color_scheme.append(ask_color_scheme(c))
        print_maze(expanded_maze, config_data, color_scheme, show_path)
        ask_next_process(
            expanded_maze, config_data, config_path, scheme_index, show_path
        )
