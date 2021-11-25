import sys
from typing import Any, Callable

from menu import Menu, Choice
import utils

def choose_vm(prompt: str="Veuillez choisir une machine ", handler: Callable[..., Any]=None):
    def wrapper(choice: Choice):
        vms = utils.ls_vms()
        vm = Menu(prompt, list(map(lambda vm: Choice(vm), vms))).run()
        return handler(vm)
    return wrapper

def wrap_start_vm(vm: Choice):
    if utils.start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec sucès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_stop_vm(vm: Choice):
    if utils.stop_vm(vm.value):
        print(f"Machine '{vm}' arrêtée avec sucès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_info(vm: Choice):
    print(f"Informations de la machine '{vm}':")
    print(utils.get_vm_info(vm.value))

def wrap_ls_vms(choice: Choice):
    vms = ", ".join(utils.ls_vms())
    print(f"Liste des machines virtuelles: {vms}")

def wrap_get_hyper_name(choice: Choice):
    print(f"Nom de la machine hyperviseur: {utils.get_hyper_name()}")

def exit_handler(choice: Choice):
    utils.close_conn(conn)
    sys.exit()


MENU = Menu(
    "Programme de gestion des machines virtuelles ; veuillez entrer votre choix",
    [
        Choice("Nom de la machine hyperviseur", wrap_get_hyper_name),
        Choice("Lister les machines virtuelles", wrap_ls_vms),
        Choice("Démarrer une machine", choose_vm(handler=wrap_start_vm)),
        Choice("Arrêter une machine", choose_vm(handler=wrap_stop_vm)),
        Choice("État d'une machine", choose_vm(handler=wrap_get_vm_info)),
        Choice("Quitter", exit_handler)
    ]
)

conn = utils.connect()
if not conn:
    print("Impossible de se connecter à l'hyperviseur")
    sys.exit(1)

while True:
    MENU.run()
    print("-"*100)
