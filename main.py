from lottery import tk, Menu
from constant import _init


def start():
    try:
        _init()
        root = tk.Tk()
        #example = Window(root)
        menu = Menu(root)
        root.mainloop()
    except KeyboardInterrupt:
        pass


start()
