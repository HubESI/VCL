import sys
from typing import Any, Callable

from menu import Menu, Choice
from utils import LibVirtApi

def choose_vm(prompt: str="Veuillez choisir une machine ", handler: Callable[..., Any]=None):
    def wrapper(choice: Choice, conn: LibVirtApi):
        vms = conn.ls_vms()
        vm = Menu(prompt, list(map(lambda vm: Choice(vm), vms))).run()
        return handler(vm)
    return wrapper

def wrap_start_vm(vm: Choice, conn: LibVirtApi):
    if conn.start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec sucès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_stop_vm(vm: Choice, conn: LibVirtApi,):
    if conn.stop_vm(vm.value):
        print(f"Machine '{vm}' arrêtée avec sucès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_info(vm: Choice, conn: LibVirtApi):
    print(f"Informations de la machine '{vm}':")
    print(conn.get_vm_info(vm.value))

def wrap_ls_vms(choice: Choice, conn: LibVirtApi):
    vms = conn.ls_vms()
    vms_names = list(map(lambda vm: vm.name(), vms))
    print(f"Machines virtuelles: {', '.join(vms_names) if len(vms_names) else 'nul'}")

def wrap_get_hyper_name(choice: Choice, conn: LibVirtApi):
    print(f"Machine hyperviseur: {conn.get_hyper_name()}")

def exit_handler(choice: Choice, conn: LibVirtApi):
    conn.close_conn()
    sys.exit()


try:
    conn = LibVirtApi()
except Exception as e:
    print("Impossible de se connecter à l'hyperviseur")
    sys.exit(1)

MENU = Menu(
    "Programme de gestion des machines virtuelles ; veuillez entrer votre choix",
    [
        Choice("Nom de la machine hyperviseur", wrap_get_hyper_name, conn),
        Choice("Lister les machines virtuelles", wrap_ls_vms, conn),
        Choice("Démarrer une machine", choose_vm(handler=wrap_start_vm), conn),
        Choice("Arrêter une machine", choose_vm(handler=wrap_stop_vm), conn),
        Choice("État d'une machine", choose_vm(handler=wrap_get_vm_info), conn),
        Choice("Quitter", exit_handler, conn)
    ]
)

while True:
    MENU.run()
    print("-"*100)
