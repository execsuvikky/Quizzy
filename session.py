import streamlit

state = streamlit.session_state

class SessionVariable:
    def __init__(self, key, default=None):
        self.key = key
        if default is not None:
            self.set_if_missing(default)

    def get(self):
        if self.key not in state:
            return None
        return state.get(self.key)
    
    def set(self, value):
        state[self.key] = value
    
    def get_or_set(self, default):
        value = self.get()
        if value is None:
            self.set(default)
            return default
        return value
    
    def update(self, lambda_):
        self.set(lambda_(self.get()))
    
    def set_if_missing(self, value):
        if self.get():
            return
        if callable(value):
            value = value()
        self.set(value)
