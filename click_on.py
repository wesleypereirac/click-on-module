import subprocess
import time
from time import sleep


def start_ydo():
    # Verifica se o daemon já existe
    if subprocess.run(
        ['pgrep', 'ydotoold'],
        capture_output=True
    ).returncode != 0:

        subprocess.Popen(
            ['ydotoold'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(1)


class MouseMover:
    """
    Uso:

    mouse = MouseMover()
    mouse.click_on(1297, 18)
    mouse.click_on(1187, 46)
    """
    debug = True

    def __init__(
        self,
        move_val=50,
        pointer_speed=0.008
    ):
        self.move_val = move_val
        self.pointer_speed = pointer_speed


    def click_on(self, x, y):
        start_ydo()
        # reset para origem
        subprocess.run([
            "ydotool",
            "mousemove",
            "-x",
            "-2000",
            "-y",
            "-2000"
        ])

        sleep(0.2)

        self.debug_pos()

        self.__move_axis(x, "x")
        self.__move_axis(y, "y")

        # # calibração do ambiente (ydotool + Wayland/KWin)
        # subprocess.run([
        #     "ydotool",
        #     "mousemove",
        #     "-x",
        #     "-14",
        #     "-y",
        #     "-1"
        # ])
        self.debug_pos()

        self.mouse_click()


    def __move_axis(self, target, axis):

        iterations = target // self.move_val

        remainder = target % self.move_val
        print(f'\n[DEBUG]\n iterations: {iterations}\n  remainder: {remainder}\n  target: {target}\n  move_val: {self.move_val}\n\n')


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
                str(dx),
                str(dy)
            ])

            sleep(0.1) #self.pointer_speed)


        # movimento restante
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
            print(f'[debug] no RESTO, movendo {dx},{dy}')



    @staticmethod
    def debug_pos():
        if not MouseMover.debug:
            return
        
        proc = subprocess.Popen(
            [
                "slurp",
                "-p"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        sleep(0.5)

        MouseMover.mouse_click()
        stdout, _ = proc.communicate()

        print(
            f"posição atual: {stdout.strip()}"
        )



    @staticmethod
    def mouse_click():

        subprocess.run(
            [
                "ydotool",
                "click",
                "0xC0"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )



def teste():

    mouse = MouseMover()

    print("[warning] remover teste!")
    x,y = 1229,62
    print("movendo para ",x,y)

    mouse.click_on(
        x,
        y
    )


# remover depois
teste()     