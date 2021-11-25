import libvirt

def connect(uri: str=None) -> libvirt.virConnect:
    try:
        return libvirt.openReadOnly(uri)
    except libvirt.libvirtError:
        return None

def close_conn(conn: libvirt.virConnect):
    conn.close()

def get_hyper_name() -> str:
    return 

def ls_vms() -> list[str]:
    return ["vm1", "vm2", "vm3"]

def start_vm(vm: str) -> bool:
    return True

def stop_vm(vm: str) -> bool:
    return False

def get_vm_info(vm: str) -> str:
    return "info of"
