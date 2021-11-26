from typing import Any, Callable

class Choice:
    def __init__(
        self,
        value: str,
        handler: Callable[..., Any]=lambda choice : choice,
        *args,
        **kwargs
    ) -> None:
        self.value = value
        self.handler = self._decorate_handler(handler, *args, **kwargs)
    
    def __str__(self) -> str:
        return self.value
    
    def _decorate_handler(self, handler: Callable[..., Any], *args, **kwargs):
        def wrapper() -> Any:
            return handler(self, *args, **kwargs)
        return wrapper

class Menu:
    def __init__(self, welcome: str, choices: list[Choice], prompt: str="Votre choix : ") -> None:
        self.welcome = welcome
        self.choices = choices
        self.prompt = prompt
    
    def __str__(self) -> str:
        return '\n'.join(
            [self.welcome]+[f"{i}) {choice}" for i, choice in enumerate(self.choices)]
        )
    
    def _get_choice(self) -> int:
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

    def run(self) -> Any:
        if len(self.choices) == 0:
            return None
        print(self)
        choice = self._get_choice()
        return self.choices[choice].handler()
