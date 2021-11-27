from typing import Any
import libvirt
from libvirt import libvirtError, virDomain

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
        if vm_obj is None:
            return False
        return True if vm_obj.create()>=0 else False
        
    
    def shutdown_vm(self, vm: str) -> bool:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj is None:
            return False
        return True if vm_obj.shutdown()>=0 else False
    
    def destroy_vm(self, vm: str) -> bool:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj is None:
            return False
        return True if vm_obj.destroy()>=0 else False
    
    def get_vm_hardware_info(self, vm: str) -> dict[str, Any]:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            info = vm_obj.info()
            return {
                "maxmem": info[1] / 1024,
                "mem": info[2] / 1024,
                "cpus": info[3]
            }
    
    def get_vm_network_info(self, vm: str) -> dict[str, Any]:
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            net_info = {}
            try:
                net_info['ARP'] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP,
                    0
                )
                net_info['LEASE'] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE,
                    0
                )
                net_info['AGENT'] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT,
                    0
                )
            except libvirtError:
                pass
            return net_info
    
    @staticmethod
    def get_ip_type(type: int) -> str:
        if type == libvirt.VIR_IP_ADDR_TYPE_IPV4:
            return "ipv4"
        elif type == libvirt.VIR_IP_ADDR_TYPE_IPV6:
            return "ipv6"
    
    def close_conn(self):
        self.conn.close()
