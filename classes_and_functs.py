from pynput.mouse import Controller as ms_ctrl
import threading, time, random

class MouseControl:
    _can_stop = 0
    my_mouse = ms_ctrl()
    _t = time.perf_counter()

    def __init__(self, debounce_min, debounce_max, debounce_segment, change_after, func=None):
        """
        :param debounce_min: how many milliseconds latter button click again. like 20 or 100
        :param debounce_max: how many milliseconds latter button click again. like 20 or 100
        debounce_min and debounce_max work together if these both are same so constant cps will be granted
        but if they are given in a range like min 10 and max 20 so debounce randomly get chosen between the
        range of min and max. it helps to bypass anti-cheat.
        :param debounce_segment: how many numbers it will take between debounce_min to debounce_max.
        :param change_after: after how many seconds cps will change
        :param func: function which called while clicking
        """
        self._debounce_min = debounce_min
        self._debounce_max = debounce_max
        self._debounce_segment = debounce_segment
        self._change_after = change_after
        step_ = len(range(debounce_min, debounce_max + 1)) // debounce_segment
        self._segment_list_ms = list(range(debounce_min, debounce_max + 1, step_ + 1))
        self._current_debounce = random.choice(self._segment_list_ms) / 1000
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
                time.sleep(self._current_debounce)
                if int(time.perf_counter()) % self._change_after == 0:
                    self._current_debounce = random.choice(self._segment_list_ms) / 1000
                if self._func: self._func()

        threading.Thread(target=_click_).start()
        # threading.Thread(target=self._change_current_debounce).start()

    def stop_clicking(self):
        self._can_stop = 0

    def is_running(self):
        return self._can_stop

if __name__ == '__main__':
    # Testing of MouseControl
    """
    from pynput.mouse import Button as pynput_btn
    ms = MouseControl()
    time.sleep(10)
    ms.start_clicking(pynput_btn.left, 0.03, func=lambda : print("clicking.."))
    time.sleep(2)
    ms.stop_clicking()
    """
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