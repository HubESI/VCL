import sys
from typing import Any, Callable

from menu import Menu, Choice
from utils import LibVirtApi, virDomain

def choose_vm(
    vms_gen: Callable[..., list[virDomain]],
    handler: Callable[..., Any],
    welcome: str="Veuillez choisir une machine ",
    error_msg: str="Impossible de lister les vms",
    no_vm_msg: str="Aucune vm trouvée",
    *args,
    **kwargs
):
    def wrapper(choice: Choice, conn: LibVirtApi):
        vms = vms_gen(*args, **kwargs)
        if not vms:
            print(error_msg)
            return
        if len(vms) == 0:
            print(no_vm_msg)
            return
        Menu(welcome, list(map(lambda vm: Choice(vm.name(), handler, conn), vms))).run()
    return wrapper

def wrap_start_vm(vm: Choice, conn: LibVirtApi):
    if conn.start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec sucès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_shutdown_vm(vm: Choice, conn: LibVirtApi):
    if conn.shutdown_vm(vm.value):
        print(f"Demande d'arrêt envoyée avec succès à '{vm}'")
    else:
        print(f"Impossible d'envoyer une demande d'arrêt à '{vm}'")

def wrap_destroy_vm(vm: Choice, conn: LibVirtApi):
    a = conn.destroy_vm(vm.value)
    print('lkj', a)
    if a:
        print(f"Machine '{vm}' arrêtée avec sucès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_info(vm: Choice, conn: LibVirtApi):
    print(f"Informations de la machine '{vm}':")
    print(conn.get_vm_info(vm.value))

def wrap_ls_vms(choice: Choice, conn: LibVirtApi):
    vms = conn.ls_vms()
    if vms:
        vms_names = list(map(lambda vm: vm.name(), vms))
        print(f"Machines virtuelles: {', '.join(vms_names) if len(vms_names) else 'nul'}")
    else:
        print("Impossible de lister les vms")

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
        Choice("Démarrer une machine", choose_vm(conn.ls_inactive_vms, wrap_start_vm), conn),
        Choice("Demander l'arrêt d'une machine", choose_vm(conn.ls_active_vms, wrap_shutdown_vm), conn),
        Choice("Arrêter une machine", choose_vm(conn.ls_active_vms, wrap_destroy_vm), conn),
        Choice("État d'une machine", choose_vm(conn.ls_vms, wrap_get_vm_info), conn),
        Choice("Quitter", exit_handler, conn)
    ]
)

while True:
    MENU.run()
    print("-"*100)
