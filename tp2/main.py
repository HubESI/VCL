import sys
import os

from menu import Menu, Choice
from libvirt_utils import LibVirtUtils

def choose_vm(
    vms_gen,
    handler,
    welcome="Veuillez choisir une machine",
    error_msg="Impossible de lister les vms",
    novm_msg="Aucune vm trouvée",
    *args,
    **kwargs
):
    def wrapper(choice, conn):
        vms = vms_gen(*args, **kwargs)
        if vms is None:
            print(error_msg)
            return
        if len(vms) == 0:
            print(novm_msg)
            return
        choices = list(map(lambda vm: Choice(vm.name(), handler, conn), vms))
        choices.append(Choice("Quitter"))
        Menu(welcome, choices).run()
    return wrapper

def wrap_start_vm(vm, conn):
    if conn.start_vm(vm.value):
        print(f"Machine '{vm}' démarrée avec succès")
    else:
        print(f"Échec du démarrage de la machine '{vm}'")

def wrap_shutdown_vm(vm, conn):
    if conn.shutdown_vm(vm.value):
        print(f"Demande d'arrêt envoyée avec succès à '{vm}'")
    else:
        print(f"Impossible d'envoyer une demande d'arrêt à '{vm}'")

def wrap_destroy_vm(vm, conn):
    if conn.destroy_vm(vm.value):
        print(f"Machine '{vm}' arrêtée avec succès")
    else:
        print(f"Échec d'arrêt de la machine '{vm}'")

def wrap_get_vm_hardware_info(vm, conn):
    info = conn.get_vm_hardware_info(vm.value)
    print(f"Configuration matérielle de la machine '{vm}':")
    print(f"Mémoire: {info['mem']} MiB")
    print(f"Mémoire: maximalle {info['maxmem']} MiB")
    print(f"Processeurs: {info['cpus']} vcpu")

def wrap_get_vm_network_info(vm, conn):
    net_info = conn.get_vm_network_info(vm.value)
    if len(net_info) == 0:
        print(f"Impossible d'afficher les informations réseau de la machine '{vm}'")
        return
    print(f"Informations réseau de la machine '{vm}' :")
    for source, source_value in net_info.items():
        print(f"From {source}")
        if len(source_value) == 0:
            print("\t N/A")
            continue
        for net, net_value in source_value.items():
            print(f"\tRéseau virtuel: {net}")
            print(f"\t\tInterface (MAC): {net_value['hwaddr']}")
            print("\t\tAdresses IP:")
            if len(net_value["addrs"]) == 0:
                print("\t\t\t N/A")
                continue
            for adr in net_value["addrs"]:
                print(f"\t\t\t{conn.get_ip_type(adr['type'])} {adr['addr']}/{adr['prefix']}")


def wrap_ls_vms(choice, conn):
    vms = conn.ls_vms()
    if vms is None:
        print("Impossible de lister les machine virtuelles")
    else:
        print(f"{'Name':<40}{'State':<40}")
        for vm in vms:
            print(f"{vm.name():<40}{conn.get_states(vm):<40}")

def wrap_get_hyper_name(choice, conn):
    print(f"Machine hyperviseur: {conn.get_hyper_name()}")

def clrsc_handler(choice):
    os.system("clear")

def exit_handler(choice, conn):
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
                conn.ls_running_vms,
                wrap_shutdown_vm,
                "Veuillez choisir une machine en cours d'exécution à demander l'arrêt",
                "Impossible de lister les machines virtuelles en cours d'exécution",
                "Aucune machine virtuelle en cours d'exécution trouvée"
            ),
            conn
        ),
        Choice(
            "Arrêter une machine virtuelle",
            choose_vm(
                conn.ls_running_vms,
                wrap_destroy_vm,
                "Veuillez choisir une machine en cours d'exécution à arrêter",
                "Impossible de lister les machines virtuelles en cours d'exécution",
                "Aucune machine virtuelle en cours d'exécution trouvée"
            ),
            conn
        ),
        Choice(
            "Afficher la configuration matérielle d'une machine virtuelle",
            choose_vm(conn.ls_vms, wrap_get_vm_hardware_info),
            conn
        ),
        Choice(
            "Afficher les informations réseau d'une machine virtuelle",
            choose_vm(
                conn.ls_running_vms,
                wrap_get_vm_network_info,
                "Veuillez choisir une machine en cours d'exécution",
                "Impossible de lister les machines virtuelles en cours d'exécution",
                "Aucune machine virtuelle en cours d'exécution trouvée"
            ),
            conn
        ),
        Choice("Clear", clrsc_handler),
        Choice("Quitter", exit_handler, conn)
    ]
)

while True:
    MENU.run()
    print("="*100)
