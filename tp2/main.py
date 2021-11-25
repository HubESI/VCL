import sys
from typing import Any, Callable

from menu import Menu, Choice
from utils import *

def choose_vm(prompt: str="Veuillez choisir une machine ", handler: Callable[..., Any]=None):
    def wrapper(choice: Choice):
        vms = ls_vms()
        vm = Menu(prompt, list(map(lambda vm: Choice(vm), vms))).run()
        return handler(vm)
    return wrapper

def wrap_start_vm(vm: Choice):
    if start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec sucès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_stop_vm(vm: Choice):
    if stop_vm(vm.value):
        print(f"Machine '{vm}' arrêtée avec sucès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_info(vm: Choice):
    print(f"Informations de la machine '{vm}':")
    print(get_vm_info(vm.value))

def wrap_ls_vms(choice: Choice):
    vms = ", ".join(ls_vms())
    print(f"Liste des machines virtuelles: {vms}")

def wrap_get_hyper_name(choice: Choice):
    print(f"Nom de la machine hyperviseur: {get_hyper_name()}")


MENU = Menu(
    "Programme de gestion des machines virtuelles ; veuillez entrer votre choix",
    [
        Choice("Nom de la machine hyperviseur", wrap_get_hyper_name),
        Choice("Lister les machines virtuelles", wrap_ls_vms),
        Choice("Démarrer une machine", choose_vm(handler=wrap_start_vm)),
        Choice("Arrêter une machine", choose_vm(handler=wrap_stop_vm)),
        Choice("État d'une machine", choose_vm(handler=wrap_get_vm_info)),
        Choice("Quitter", lambda choice : sys.exit())
    ]
)

while True:
    MENU.run()
    print("-"*100)
