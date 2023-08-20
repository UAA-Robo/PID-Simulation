class ControllerValue:
    def __init__(self, value: float, name: str, adjust_amount: float = None):
        self._value = value
        self._name = name
        self._adjust_amount = adjust_amount

    def increment_value(self) -> None:
        if not self._adjust_amount:
            return
        self._value += self._adjust_amount

    def decrement_value(self) -> None:
        if not self._adjust_amount:
            return
        self._value -= self._adjust_amount
    
    # Getters and Setters
    @property
    def value(self): return self._value
    @value.setter
    def value(self, value): self._value = float(value)

    @property
    def name(self): return self._name

    @property
    def adjust_amount(self): return self._adjust_amount
    @adjust_amount.setter
    def adjust_amount(self, value): self._adjust_amount = float(value)