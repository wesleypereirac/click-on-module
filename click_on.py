import subprocess
from time import sleep


class MouseMover:

    def __init__(self, move_val=20, offset=1, pointer_speed=0):
        self.move_val = move_val
        self.offset = offset
        self.pointer_speed = pointer_speed

    def move_mouse(self, x, y):

        # Reinicia no canto superior esquerdo
        subprocess.run([
            "ydotool",
            "mousemove",
            "-x",
            "-2000",
            "-y",
            "-2000"
        ])

        self.__move_axis(x, "x")
        self.__move_axis(y, "y")

        self.mouse_click()

    def __move_axis(self, target, axis):
        """
        Move um único eixo.
        """

        # Exemplo:
        # target=1297
        # move_val=20
        #
        # iterations = 64
        # remainder = 16

        iterations, remainder = divmod(
            target - self.offset,
            self.move_val
        )

        for _ in range(iterations):

            if axis == "x":
                dx = self.move_val
                dy = 0
            else:
                dx = 0
                dy = self.move_val

            subprocess.run([
                "ydotool",
                "mousemove",
                "-x",
                str(dx),
                "-y",
                str(dy)
            ])

            sleep(self.pointer_speed)

        if remainder:

            if axis == "x":
                dx = remainder
                dy = 0
            else:
                dx = 0
                dy = remainder

            subprocess.run([
                "ydotool",
                "mousemove",
                "-x",
                str(dx),
                "-y",
                str(dy)
            ])

    @staticmethod
    def mouse_click():
        subprocess.run(
            ["ydotool", "click", "0xC0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
