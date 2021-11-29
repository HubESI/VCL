class Choice:
    def __init__(self, value, handler=lambda choice : choice, *args, **kwargs):
        self.value = value
        self.handler = self._decorate_handler(handler, *args, **kwargs)
    
    def __str__(self):
        return self.value
    
    def _decorate_handler(self, handler, *args, **kwargs):
        def wrapper():
            return handler(self, *args, **kwargs)
        return wrapper

class Menu:
    def __init__(self, welcome, choices, prompt="Votre choix : "):
        self.welcome = welcome
        self.choices = choices
        self.prompt = prompt
    
    def __str__(self):
        return '\n'.join(
            [self.welcome]+[f"{i}) {choice}" for i, choice in enumerate(self.choices)]
        )
    
    def _get_choice(self):
        while(True):
            try:
                choice = int(input(self.prompt))
                assert choice >= 0
                assert choice < len(self.choices)
                return choice
            except ValueError as e:
                print("Veuillez entrer le numéro de votre choix")
            except AssertionError as e:
                print(f"Votre choix doit être entre 0 (inclus) et {len(self.choices)} (exclusif)")
    
    def run(self):
        if len(self.choices) == 0:
            return None
        print(self)
        choice = self._get_choice()
        return self.choices[choice].handler()
