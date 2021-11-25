import libvirt

class LibVirtApi:
    def __init__(self, uri: str=None) -> None:
        self.conn = libvirt.openReadOnly(uri)

    def get_hyper_name(self) -> str:
        return self.conn.getHostname()

    def ls_vms(self) -> list[str]:
        return ["vm1", "vm2", "vm3"]

    def start_vm(self, vm: str) -> bool:
        return True

    def stop_vm(self, vm: str) -> bool:
        return False

    def get_vm_info(self, vm: str) -> str:
        return "info of"
