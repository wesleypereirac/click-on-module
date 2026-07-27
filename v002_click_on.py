import subprocess
from time import sleep


class MouseMover:
    def __init__(
        self,
        move_val=20,
        offset=1,
        pointer_speed=0,
        verify_precision=False
    ):
        self.move_val = move_val
        self.offset = offset
        self.pointer_speed = pointer_speed
        self.verify_precision = verify_precision

    def move_mouse(self, x, y):

        # garante começar do canto
        subprocess.run([
            "ydotool",
            "mousemove",
            "-x",
            "-2000",
            "-y",
            "-2000"
        ])

        # eixo X
        self.__move_axis(x, "x")

        # eixo Y
        self.__move_axis(y, "y")

        self.mouse_click()

        if self.verify_precision:
            print(self.get_current_pos())

    def __move_axis(self, value, axis):

        iterations = value // self.move_val
        remainder = (value - self.offset) % self.move_val

        for _ in range(iterations):

            if axis == "x":
                subprocess.run([
                    "ydotool",
                    "mousemove",
                    "-x",
                    str(self.move_val),
                    "-y",
                    "0"
                ])
            else:
                subprocess.run([
                    "ydotool",
                    "mousemove",
                    "-x",
                    "0",
                    "-y",
                    str(self.move_val)
                ])

            sleep(self.pointer_speed)

        if remainder:

            if axis == "x":
                subprocess.run([
                    "ydotool",
                    "mousemove",
                    "-x",
                    str(remainder),
                    "-y",
                    "0"
                ])
            else:
                subprocess.run([
                    "ydotool",
                    "mousemove",
                    "-x",
                    "0",
                    "-y",
                    str(remainder)
                ])

    @staticmethod
    def mouse_click():
        subprocess.run(
            ["ydotool", "click", "0xC0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    @staticmethod
    def get_current_pos():

        proc = subprocess.Popen(
            ["slurp", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        sleep(1.5)

        MouseMover.mouse_click()

        sleep(1)

        stdout, _ = proc.communicate()

        coord = stdout.split()[0]

        x, y = map(int, coord.split(","))

        return {
            "x": x,
            "y": y
        }
