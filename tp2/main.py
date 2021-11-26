import sys
from typing import Any, Callable

from menu import Menu, Choice
from libvirt_utils import LibVirtUtils, virDomain

def choose_vm(
    vms_gen: Callable[..., list[virDomain]],
    handler: Callable[..., Any],
    welcome: str="Veuillez choisir une machine",
    error_msg: str="Impossible de lister les vms",
    novm_msg: str="Aucune vm trouvée",
    *args,
    **kwargs
):
    def wrapper(choice: Choice, conn: LibVirtUtils):
        vms = vms_gen(*args, **kwargs)
        if vms is None:
            print(error_msg)
            return
        if len(vms) == 0:
            print(novm_msg)
            return
        Menu(welcome, list(map(lambda vm: Choice(vm.name(), handler, conn), vms))).run()
    return wrapper

def wrap_start_vm(vm: Choice, conn: LibVirtUtils):
    if conn.start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec sucès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_shutdown_vm(vm: Choice, conn: LibVirtUtils):
    if conn.shutdown_vm(vm.value):
        print(f"Demande d'arrêt envoyée avec succès à '{vm}'")
    else:
        print(f"Impossible d'envoyer une demande d'arrêt à '{vm}'")

def wrap_destroy_vm(vm: Choice, conn: LibVirtUtils):
    if conn.destroy_vm(vm.value):
        print(f"Machine '{vm}' arrêtée avec sucès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_info(vm: Choice, conn: LibVirtUtils):
    print(f"Informations de la machine '{vm}':")
    print(conn.get_vm_info(vm.value))

def wrap_ls_vms(choice: Choice, conn: LibVirtUtils):
    vms = conn.ls_vms()
    if vms is None:
        print("Impossible de lister les machine virtuelle")
    else:
        vms_names = list(map(lambda vm: vm.name(), vms))
        print(f"Liste des machines virtuelles: {', '.join(vms_names) if len(vms_names) else 'nul'}")

def wrap_get_hyper_name(choice: Choice, conn: LibVirtUtils):
    print(f"Machine hyperviseur: {conn.get_hyper_name()}")

def exit_handler(choice: Choice, conn: LibVirtUtils):
    conn.close_conn()
    sys.exit()


try:
    conn = LibVirtUtils()
except Exception as e:
    print("Impossible de se connecter à l'hyperviseur")
    sys.exit(1)

MENU = Menu(
    "Programme de gestion des machines virtuelles ; veuillez entrer votre choix",
    [
        Choice("Afficher le nom de la machine hyperviseur", wrap_get_hyper_name, conn),
        Choice("Lister les machines virtuelles", wrap_ls_vms, conn),
        Choice(
            "Démarrer une machine virtuelle",
            choose_vm(
                conn.ls_inactive_vms,
                wrap_start_vm,
                "Veuillez choisir une machine inactive à activer",
                "Impossible de lister les machines virtuelles inactives",
                "Aucune machine virtuelle inactive trouvée"
            ),
            conn
        ),
        Choice(
            "Demander l'arrêt d'une machine virtuelle",
            choose_vm(
                conn.ls_active_vms,
                wrap_shutdown_vm,
                "Veuillez choisir une machine active à demander l'arrêt",
                "Impossible de lister les machines virtuelles actives",
                "Aucune machine virtuelle active trouvée"
            ),
            conn
        ),
        Choice(
            "Arrêter une machine virtuelle",
            choose_vm(
                conn.ls_active_vms,
                wrap_destroy_vm,
                "Veuillez choisir une machine active à arrêter",
                "Impossible de lister les machines virtuelles actives",
                "Aucune machine virtuelle active trouvée"
            ),
            conn
        ),
        Choice(
            "Afficher l'état d'une machine virtuelle",
            choose_vm(conn.ls_vms, wrap_get_vm_info),
            conn
        ),
        Choice("Quitter", exit_handler, conn)
    ]
)

while True:
    MENU.run()
    print("-"*100)
