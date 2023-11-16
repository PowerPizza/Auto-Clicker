from pynput.mouse import Controller as ms_ctrl
import threading, time, random

class MouseControl:
    _can_stop = 0
    my_mouse = ms_ctrl()
    _t = time.perf_counter()
    debounce_ = 500

    def __init__(self, debounce_, func=None):
        """
        :param debounce_: how many milliseconds latter button click again. like 20 or 100
        :param func: function which called while clicking
        """
        self.debounce_ = debounce_
        self._func = func

    def start_clicking(self, btn, click_repeat=1):
        """
        :param btn: pynput_btn acceptable, it can be pynput_btn.left or pynput_btn.right
        :param click_repeat: how many click done at once. like 1, 2 or 3
        """

        if self._can_stop == 1:
            return

        self._can_stop = 1
        def _click_():
            while self._can_stop:
                self.my_mouse.click(btn, click_repeat)
                time.sleep(self.debounce_/1000)  # ms to sec conversion.
                if self._func: self._func()

        threading.Thread(target=_click_).start()
        # threading.Thread(target=self._change_current_debounce).start()

    def stop_clicking(self):
        self._can_stop = 0

    def is_running(self):
        return self._can_stop

if __name__ == '__main__':
    # Testing of MouseControl
    # from pynput.mouse import Button as pynput_btn
    # ms = MouseControl(500, func=lambda : print("clicking"))
    # time.sleep(10)
    # ms.start_clicking(pynput_btn.left, 1)
    # time.sleep(2)
    # ms.stop_clicking()
    # working properly


    # Testing of createButtonTypeInput() and createScaleTypeInput()
    """
    root = Tk()
    data_ = IntVar()
    createScaleTypeInput(root, "Age : ", data_, 5, 80, "horizontal")
    def printData():
        print(data_.get())
    createButtonTypeInput(root, "Print Data : ", "Print", printData)
    root.mainloop()
    # working properly.
    """
    pass