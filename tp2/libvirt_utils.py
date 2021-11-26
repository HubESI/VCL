import libvirt
from libvirt import virDomain

class LibVirtUtils:
    def __init__(self, uri: str=None) -> None:
        self.conn = libvirt.open(uri)
    
    def get_hyper_name(self) -> str:
        return self.conn.getHostname()
    
    def ls_vms(self) -> list[virDomain]:
        return self.conn.listAllDomains(0)
    
    def ls_active_vms(self) -> list[virDomain]:
        return self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
    
    def ls_inactive_vms(self) -> list[virDomain]:
        return self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE)
    
    def start_vm(self, vm: str) -> bool:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            return True if vm_obj.create()>=0 else False
        return False
    
    def shutdown_vm(self, vm: str) -> bool:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            return True if vm_obj.shutdown()>=0 else False
        return False
    
    def destroy_vm(self, vm: str) -> bool:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            return True if vm_obj.destroy()>=0 else False
        return False
    
    def get_vm_info(self, vm: str) -> str:
        return "info of"
    
    def close_conn(self):
        self.conn.close()
