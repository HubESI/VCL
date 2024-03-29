import libvirt
from libvirt import libvirtError

POSSIBLE_STATES = {
    libvirt.VIR_DOMAIN_NOSTATE: "NOSTATE",
    libvirt.VIR_DOMAIN_RUNNING: "RUNNING",
    libvirt.VIR_DOMAIN_BLOCKED: "BLOCKED",
    libvirt.VIR_DOMAIN_PAUSED: "PAUSED",
    libvirt.VIR_DOMAIN_SHUTDOWN: "SHUTDOWN",
    libvirt.VIR_DOMAIN_SHUTOFF: "SHUTOFF",
    libvirt.VIR_DOMAIN_CRASHED: "CRASHED",
    libvirt.VIR_DOMAIN_PMSUSPENDED: "PMSUSPENDED"
}

class LibVirtUtils:
    def __init__(self, uri=None):
        self.conn = libvirt.open(uri)
    
    def get_hyper_name(self):
        return self.conn.getHostname()
    
    def ls_vms(self):
        return self.conn.listAllDomains(0)
    
    def ls_running_vms(self):
        return self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_RUNNING)
    
    def ls_inactive_vms(self):
        return self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE)
    
    def start_vm(self, vm):
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj is None:
            return False
        try:
            return True if vm_obj.create() >= 0 else False
        except libvirtError:
            return False
    
    def shutdown_vm(self, vm):
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj is None:
            return False
        try:
            return True if vm_obj.shutdown() >= 0 else False
        except libvirtError:
            return False
    
    def destroy_vm(self, vm):
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj is None:
            return False
        try:
            return True if vm_obj.destroy() >= 0 else False
        except libvirtError:
            return False
    
    def get_vm_hardware_info(self, vm):
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            info = vm_obj.info()
            return {
                "maxmem": info[1] / 1024,
                "mem": info[2] / 1024,
                "cpus": info[3]
            }
    
    def get_vm_network_info(self, vm):
        vm_obj = self.conn.lookupByName(vm)
        if vm_obj:
            net_info = {}
            try:
                net_info["ARP"] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP,
                    0
                )
                net_info["LEASE"] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE,
                    0
                )
                net_info["AGENT"] = vm_obj.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT,
                    0
                )
            except libvirtError:
                pass
            return net_info
    
    @staticmethod
    def get_ip_type(type):
        if type == libvirt.VIR_IP_ADDR_TYPE_IPV4:
            return "ipv4"
        elif type == libvirt.VIR_IP_ADDR_TYPE_IPV6:
            return "ipv6"
    
    @staticmethod
    def get_states(vm):
        return POSSIBLE_STATES.get(vm.state()[0], "UNKNOWN")
    
    def close_conn(self):
        self.conn.close()
