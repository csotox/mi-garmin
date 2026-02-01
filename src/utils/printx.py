
# Colores ANSI
COLOR_CYAN = "36"
COLOR_GREEN = "32"
COLOR_RED = "31"
RESET = "\033[0m"
# Oculto y muestro el cursor
CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"

class Console:

    def __init__(self, use_color: bool = True, enabled: bool = True):
        self.use_color = use_color
        self.enabled = enabled

    def _color(self, text: str, code: str) -> str:
        if not self.use_color:
            return text
        return f"\033[{code}m{text}{RESET}"


    def info(self, message: str):
        if self.enabled:
            print(self._color(f"[INFO] {message}", COLOR_CYAN))


    def success(self, message: str):
        if self.enabled:
            print(self._color(f"[OK] {message}", COLOR_GREEN))


    def error(self, message: str):
        if self.enabled:
            print(self._color(f"[ERROR] {message}", COLOR_RED))


class Progress:

    def __init__(self, total: int = 1, bar_length: int = 30):
        self.total = total if total > 0 else 1
        self.current = 0
        self.bar_length = bar_length
        self._finished = False


    def __enter__(self):
        print(CURSOR_HIDE, end="", flush=True)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:

        if exc_type is not None or self.current < self.total:
            self.finish(success=False)      # Por si ocurre un error
        else:
            self.finish(success=True)

        return False


    def update(self) -> None:
        self.current += 1

        progress = self.current / self.total
        filled = int(self.bar_length * progress)

        bar = f"{'█' * filled}{'-' * (self.bar_length - filled)}"

        print(f"\r[{bar}] {self.current}/{self.total}", end="", flush=True)


    def finish(self, success: bool = True) -> None:
        if self._finished:
            return

        color = COLOR_GREEN if success else COLOR_RED
        filled = int(self.bar_length * ( self.current / self.total ))
        bar = f"{'█' * filled}{'-' * (self.bar_length - filled)}"

        print(f"\r\033[{color}m[{bar}] {self.current}/{self.total}{RESET}", end="")
        print(CURSOR_SHOW, end="", flush=True)
        print()

        self._finished = True
