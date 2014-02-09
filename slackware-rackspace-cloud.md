Installing Slackware on Rackspace Cloud.
========================================

Using the boot.rackspace.com iPXE image to boot from allows for greater than usual configuration. There are a limited number of OS supported at the moment but that doesn't stop you installing Slackware.

Booting.
--------

Build a machine using the boot.rackspace.com image:

    root@tools:~# nova boot slack --image "9aa0d346-c06f-4652-bbb1-4342a7d2d017" --flavor "performance1-1"
    +------------------------+--------------------------------------+
    | Property               | Value                                |
    +------------------------+--------------------------------------+
    | status                 | BUILD                                |
    | updated                | 2014-02-09T14:29:12Z                 |
    | OS-EXT-STS:task_state  | scheduling                           |
    | key_name               | None                                 |
    | image                  | boot.rackspace.com                   |
    | hostId                 |                                      |
    | OS-EXT-STS:vm_state    | building                             |
    | flavor                 | 1 GB Performance                     |
    | id                     | 60689192-8f81-4083-bc81-153c343cb19f |
    | user_id                |                                      |
    | name                   | slack                                |
    | adminPass              |                                      |
    | tenant_id              |                                      |
    | created                | 2014-02-09T14:29:12Z                 |
    | OS-DCF:diskConfig      | MANUAL                               |
    | accessIPv4             |                                      |
    | accessIPv6             |                                      |
    | progress               | 0                                    |
    | OS-EXT-STS:power_state | 0                                    |
    | config_drive           |                                      |
    | metadata               | {}                                   |
    +------------------------+--------------------------------------+

Then connect to console through the web interface on the control panel.

![iPXE](http://img.cfil.es/1391957689.jpg 'iPXE')

Setup DNS server and configure the PXE to boot from remote bzImage and initrd with these options (Rackspace LON DNS is being used here)

    set dns 83.138.151.80
    kernel http://lon.mirror.rackspace.com/slackware/slackware-14.1/kernels/huge.s/bzImage load_ramdisk=1 prompt_ramdisk=0 rw nomodeset SLACK_KERNEL=huge.s
    initrd http://lon.mirror.rackspace.com/slackware/slackware-14.1/isolinux/initrd.img
    boot

![boot](http://img.cfil.es/1391961912.jpg 'boot')

Go through the usual configuration of Slackware, since the drive comes pre-partitioned I blew that away and created a swap partition as well for the base image. When it gets to choosing an install source then HTTP/FTP works with configuration like this:

![sources](http://img.cfil.es/1391959634.jpg 'sources')
![slackware](http://img.cfil.es/1391959660.jpg 'slackware')

The installer will probe for network drivers and should load up fine, then enter the static IP info for the machine. I also dropped to an alternate screen and added DNS server.

![DNS](http://img.cfil.es/1391959568.jpg 'DNS')

Then the install continues as normal, I normally skip the X packages such as X, XAP, KDE.
Once it finishes, skip creating a USB rescue drive and installing LILO, set a password up and then drop out to console.

We need to install GRUB here so chroot into /mnt and run the installer before rebooting.

![GRUB](http://img.cfil.es/1391964700.jpg 'GRUB')

At this point I lost the console, but a few seconds later I can ssh into the Slackware install.
Nest steps are to image it and continue the process in the boot.rackspace.com wiki to try and install Nova Agent. It tests for the OS and Slackware isn't included so I've skipped that for now.

    root@tools:~# ssh 123.123.123.123 -l root
    The authenticity of host '123.123.123.123 (123.123.123.123)' can't be established.
    ECDSA key fingerprint is 28:34:fa:9b:2e:cc:2b:6d:05:8c:f3:bc:9f:de:39:e4.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '123.123.123.123' (ECDSA) to the list of known hosts.
    root@123.123.123.123's password: 
    Linux 3.10.17-smp.
    root@slack:~# 
    root@slack:~# uptime 
    16:54:17 up 0 min,  1 user,  load average: 0.06, 0.01, 0.01
    root@slack:~# 
    root@slack:~# df
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/sda1       19097204 4012468  14091604  23% /
    tmpfs             508748       0    508748   0% /dev/shm
    root@slack:~# cat /proc/cpuinfo 
    processor	: 0
    vendor_id	: GenuineIntel
    cpu family	: 6
    model		: 45
    model name	: Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
    stepping	: 7
    microcode	: 0x710
    cpu MHz		: 2600.000
    cache size	: 20480 KB
    fdiv_bug	: no
    f00f_bug	: no
    coma_bug	: no
    fpu		: yes
    fpu_exception	: yes
    cpuid level	: 13
    wp		: yes
    flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat clflush mmx fxsr sse sse2 nx rdtscp lm constant_tsc pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes hypervisor lahf_lm
    bogomips	: 5187.87
    clflush size	: 64
    cache_alignment	: 64
    address sizes	: 46 bits physical, 48 bits virtual
    power management:
    root@slack:~# dmesg 
    [    0.000000] Initializing cgroup subsys cpuset
    [    0.000000] Initializing cgroup subsys cpu
    [    0.000000] Initializing cgroup subsys cpuacct
    [    0.000000] Linux version 3.10.17-smp (root@hive) (gcc version 4.8.2 (GCC) ) #2 SMP Wed Oct 23 17:13:14 CDT 2013
    [    0.000000] e820: BIOS-provided physical RAM map:
    [    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009a3ff] usable
    [    0.000000] BIOS-e820: [mem 0x00000000000e0000-0x00000000000fffff] reserved
    [    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000003fa75fff] usable
    [    0.000000] BIOS-e820: [mem 0x000000003fbde000-0x000000003fbfffff] usable
    [    0.000000] BIOS-e820: [mem 0x00000000fc000000-0x00000000ffffffff] reserved
    [    0.000000] NX (Execute Disable) protection: active
    [    0.000000] SMBIOS 2.4 present.
    [    0.000000] DMI: Xen HVM domU, BIOS 4.1.5 11/28/2013
    [    0.000000] Hypervisor detected: Microsoft HyperV
    [    0.000000] HyperV: features 0x70, hints 0x0
    [    0.000000] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
    [    0.000000] e820: remove [mem 0x000a0000-0x000fffff] usable
    [    0.000000] e820: last_pfn = 0x3fc00 max_arch_pfn = 0x1000000
    [    0.000000] MTRR default type: write-back
    [    0.000000] MTRR fixed ranges enabled:
    [    0.000000]   00000-9FFFF write-back
    [    0.000000]   A0000-BFFFF write-combining
    [    0.000000]   C0000-FFFFF write-back
    [    0.000000] MTRR variable ranges enabled:
    [    0.000000]   0 base 0000F0000000 mask 3FFFF8000000 uncachable
    [    0.000000]   1 base 0000F8000000 mask 3FFFFC000000 uncachable
    [    0.000000]   2 disabled
    [    0.000000]   3 disabled
    [    0.000000]   4 disabled
    [    0.000000]   5 disabled
    [    0.000000]   6 disabled
    [    0.000000]   7 disabled
    [    0.000000] x86 PAT enabled: cpu 0, old 0x7040600070406, new 0x7010600070106
    [    0.000000] found SMP MP-table at [mem 0x000fb710-0x000fb71f] mapped at [c00fb710]
    [    0.000000] initial memory mapped: [mem 0x00000000-0x023fffff]
    [    0.000000] Base memory trampoline at [c0096000] 96000 size 16384
    [    0.000000] init_memory_mapping: [mem 0x00000000-0x000fffff]
    [    0.000000]  [mem 0x00000000-0x000fffff] page 4k
    [    0.000000] init_memory_mapping: [mem 0x37600000-0x377fffff]
    [    0.000000]  [mem 0x37600000-0x377fffff] page 2M
    [    0.000000] init_memory_mapping: [mem 0x34000000-0x375fffff]
    [    0.000000]  [mem 0x34000000-0x375fffff] page 2M
    [    0.000000] init_memory_mapping: [mem 0x00100000-0x33ffffff]
    [    0.000000]  [mem 0x00100000-0x001fffff] page 4k
    [    0.000000]  [mem 0x00200000-0x33ffffff] page 2M
    [    0.000000] init_memory_mapping: [mem 0x37800000-0x379fdfff]
    [    0.000000]  [mem 0x37800000-0x379fdfff] page 4k
    [    0.000000] BRK [0x01fb2000, 0x01fb2fff] PGTABLE
    [    0.000000] BRK [0x01fb3000, 0x01fb4fff] PGTABLE
    [    0.000000] ACPI: RSDP 000ea020 00024 (v02    Xen)
    [    0.000000] ACPI: XSDT fc00ef80 00044 (v01    Xen      HVM 00000000 HVML 00000000)
    [    0.000000] ACPI: FACP fc00ed40 000F4 (v04    Xen      HVM 00000000 HVML 00000000)
    [    0.000000] ACPI: DSDT fc003040 0BC75 (v02    Xen      HVM 00000000 INTL 20090123)
    [    0.000000] ACPI: FACS fc003000 00040
    [    0.000000] ACPI: APIC fc00ee40 000D8 (v02    Xen      HVM 00000000 HVML 00000000)
    [    0.000000] ACPI: HPET fc00ef20 00038 (v01    Xen      HVM 00000000 HVML 00000000)
    [    0.000000] ACPI: WAET fc00ef58 00028 (v01    Xen      HVM 00000000 HVML 00000000)
    [    0.000000] ACPI: Local APIC address 0xfee00000
    [    0.000000] No NUMA configuration found
    [    0.000000] Faking a node at [mem 0x0000000000000000-0x000000003fbfffff]
    [    0.000000] Initmem setup node 0 [mem 0x00000000-0x3fbfffff]
    [    0.000000]   NODE_DATA [mem 0x379fd000-0x379fdfff]
    [    0.000000] 130MB HIGHMEM available.
    [    0.000000] 889MB LOWMEM available.
    [    0.000000] max_low_pfn = 379fe, highstart_pfn = 379fe
    [    0.000000] Low memory ends at vaddr f79fe000
    [    0.000000] High memory starts at vaddr f79fe000
    [    0.000000]   mapped low ram: 0 - 379fe000
    [    0.000000]   low ram: 0 - 379fe000
    [    0.000000] BRK [0x01fb5000, 0x01fb5fff] PGTABLE
    [    0.000000] Node: 0, start_pfn: 1, end_pfn: 9a
    [    0.000000]   Setting physnode_map array to node 0 for pfns:
    [    0.000000]   1 
    [    0.000000] Node: 0, start_pfn: 100, end_pfn: 3fa76
    [    0.000000]   Setting physnode_map array to node 0 for pfns:
    [    0.000000]   100 4100 8100 c100 10100 14100 18100 1c100 20100 24100 28100 2c100 30100 34100 38100 3c100 
    [    0.000000] Node: 0, start_pfn: 3fbde, end_pfn: 3fc00
    [    0.000000]   Setting physnode_map array to node 0 for pfns:
    [    0.000000]   3fbde 
    [    0.000000] Zone ranges:
    [    0.000000]   DMA      [mem 0x00001000-0x00ffffff]
    [    0.000000]   Normal   [mem 0x01000000-0x379fdfff]
    [    0.000000]   HighMem  [mem 0x379fe000-0x3fbfffff]
    [    0.000000] Movable zone start for each node
    [    0.000000] Early memory node ranges
    [    0.000000]   node   0: [mem 0x00001000-0x00099fff]
    [    0.000000]   node   0: [mem 0x00100000-0x3fa75fff]
    [    0.000000]   node   0: [mem 0x3fbde000-0x3fbfffff]
    [    0.000000] On node 0 totalpages: 260657
    [    0.000000] free_area_init_node: node 0, pgdat f79fd000, node_mem_map f7205020
    [    0.000000]   DMA zone: 32 pages used for memmap
    [    0.000000]   DMA zone: 0 pages reserved
    [    0.000000]   DMA zone: 3993 pages, LIFO batch:0
    [    0.000000]   Normal zone: 1748 pages used for memmap
    [    0.000000]   Normal zone: 223742 pages, LIFO batch:31
    [    0.000000]   HighMem zone: 261 pages used for memmap
    [    0.000000]   HighMem zone: 32922 pages, LIFO batch:7
    [    0.000000] Using APIC driver default
    [    0.000000] ACPI: PM-Timer IO Port: 0x1f48
    [    0.000000] ACPI: Local APIC address 0xfee00000
    [    0.000000] ACPI: LAPIC (acpi_id[0x00] lapic_id[0x00] enabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x01] lapic_id[0x02] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x02] lapic_id[0x04] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x03] lapic_id[0x06] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x04] lapic_id[0x08] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x05] lapic_id[0x0a] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x06] lapic_id[0x0c] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x07] lapic_id[0x0e] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x08] lapic_id[0x10] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x09] lapic_id[0x12] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x0a] lapic_id[0x14] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x0b] lapic_id[0x16] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x0c] lapic_id[0x18] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x0d] lapic_id[0x1a] disabled)
    [    0.000000] ACPI: LAPIC (acpi_id[0x0e] lapic_id[0x1c] disabled)
    [    0.000000] ACPI: IOAPIC (id[0x01] address[0xfec00000] gsi_base[0])
    [    0.000000] IOAPIC[0]: apic_id 1, version 17, address 0xfec00000, GSI 0-47
    [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
    [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 low level)
    [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 low level)
    [    0.000000] ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 low level)
    [    0.000000] ACPI: IRQ0 used by override.
    [    0.000000] ACPI: IRQ2 used by override.
    [    0.000000] ACPI: IRQ5 used by override.
    [    0.000000] ACPI: IRQ9 used by override.
    [    0.000000] ACPI: IRQ10 used by override.
    [    0.000000] ACPI: IRQ11 used by override.
    [    0.000000] Using ACPI (MADT) for SMP configuration information
    [    0.000000] ACPI: HPET id: 0x8086a201 base: 0xfed00000
    [    0.000000] smpboot: Allowing 15 CPUs, 14 hotplug CPUs
    [    0.000000] nr_irqs_gsi: 64
    [    0.000000] PM: Registered nosave memory: 000000000009a000 - 00000000000e0000
    [    0.000000] PM: Registered nosave memory: 00000000000e0000 - 0000000000100000
    [    0.000000] e820: [mem 0x3fc00000-0xfbffffff] available for PCI devices
    [    0.000000] setup_percpu: NR_CPUS:32 nr_cpumask_bits:32 nr_cpu_ids:15 nr_node_ids:1
    [    0.000000] PERCPU: Embedded 13 pages/cpu @f713b000 s32192 r0 d21056 u53248
    [    0.000000] pcpu-alloc: s32192 r0 d21056 u53248 alloc=13*4096
    [    0.000000] pcpu-alloc: [0] 00 [0] 01 [0] 02 [0] 03 [0] 04 [0] 05 [0] 06 [0] 07 
    [    0.000000] pcpu-alloc: [0] 08 [0] 09 [0] 10 [0] 11 [0] 12 [0] 13 [0] 14 
    [    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 258877
    [    0.000000] Policy zone: HighMem
    [    0.000000] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-huge-smp-3.10.17-smp root=/dev/sda1 ro
    [    0.000000] PID hash table entries: 4096 (order: 2, 16384 bytes)
    [    0.000000] Dentry cache hash table entries: 131072 (order: 7, 524288 bytes)
    [    0.000000] Inode-cache hash table entries: 65536 (order: 6, 262144 bytes)
    [    0.000000] Initializing CPU#0
    [    0.000000] Initializing HighMem for node 0 (000379fe:0003fc00)
    [    0.000000] Memory: 1016704k/1044480k available (10841k kernel code, 25924k reserved, 3474k data, 796k init, 131688k highmem)
    [    0.000000] virtual kernel memory layout:
    [    0.000000]     fixmap  : 0xffd36000 - 0xfffff000   (2852 kB)
    [    0.000000]     pkmap   : 0xffa00000 - 0xffc00000   (2048 kB)
    [    0.000000]     vmalloc : 0xf81fe000 - 0xff9fe000   ( 120 MB)
    [    0.000000]     lowmem  : 0xc0000000 - 0xf79fe000   ( 889 MB)
    [    0.000000]       .init : 0xc1dfc000 - 0xc1ec3000   ( 796 kB)
    [    0.000000]       .data : 0xc1a96766 - 0xc1dfb280   (3474 kB)
    [    0.000000]       .text : 0xc1000000 - 0xc1a96766   (10841 kB)
    [    0.000000] Checking if this processor honours the WP bit even in supervisor mode...Ok.
    [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=15, Nodes=1
    [    0.000000] Hierarchical RCU implementation.
    [    0.000000] 	RCU restricting CPUs from NR_CPUS=32 to nr_cpu_ids=15.
    [    0.000000] NR_IRQS:2304 nr_irqs:1208 16
    [    0.000000] CPU 0 irqstacks, hard=f6c0c000 soft=f6c0e000
    [    0.000000] Console: colour VGA+ 80x25
    [    0.000000] console [tty0] enabled
    [    0.000000] hpet clockevent registered
    [    0.000000] tsc: Fast TSC calibration using PIT
    [    0.000000] tsc: Detected 2593.939 MHz processor
    [    0.021004] Calibrating delay loop (skipped), value calculated using timer frequency.. 5187.87 BogoMIPS (lpj=2593939)
    [    0.022004] pid_max: default: 32768 minimum: 301
    [    0.023045] Security Framework initialized
    [    0.023765] Mount-cache hash table entries: 512
    [    0.024209] Initializing cgroup subsys devices
    [    0.025004] Initializing cgroup subsys freezer
    [    0.025615] Initializing cgroup subsys net_cls
    [    0.026003] Initializing cgroup subsys blkio
    [    0.027006] Initializing cgroup subsys perf_event
    [    0.028110] mce: CPU supports 0 MCE banks
    [    0.029035] Last level iTLB entries: 4KB 512, 2MB 0, 4MB 0
    [    0.029035] Last level dTLB entries: 4KB 512, 2MB 32, 4MB 32
    [    0.029035] tlb_flushall_shift: 5
    [    0.048652] ACPI: Core revision 20130328
    [    0.053114] ACPI: All ACPI Tables successfully acquired
    [    0.054747] ftrace: allocating 36203 entries in 71 pages
    [    0.098104] Overriding APIC driver with bigsmp
    [    0.099004] Enabling APIC mode:  Physflat.  Using 1 I/O APICs
    [    0.101000] Leaving ESR disabled.
    [    0.101269] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=0 pin2=0
    [    0.112916] smpboot: CPU0: Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz (fam: 06, model: 2d, stepping: 07)
    [    0.114601] TSC deadline timer enabled
    [    0.114623] Performance Events: unsupported p6 CPU model 45 no PMU driver, software events only.
    [    0.115188] Brought up 1 CPUs
    [    0.115818] smpboot: Total of 1 processors activated (5187.87 BogoMIPS)
    [    0.116366] devtmpfs: initialized
    [    0.117425] xor: measuring software checksum speed
    [    0.128005]    pIII_sse  :  2316.000 MB/sec
    [    0.138003]    prefetch64-sse:  2348.000 MB/sec
    [    0.138688] xor: using function: prefetch64-sse (2348.000 MB/sec)
    [    0.139009] atomic64 test passed for i586+ platform with CX8 and with SSE
    [    0.139803] regulator-dummy: no parameters
    [    0.140062] NET: Registered protocol family 16
    [    0.140873] ACPI: bus type PCI registered
    [    0.141006] acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
    [    0.141947] PCI : PCI BIOS area is rw and x. Use pci=nobios if you want it NX.
    [    0.142030] PCI: PCI BIOS revision 2.10 entry at 0xfb0a0, last bus=0
    [    0.142696] PCI: Using configuration type 1 for base access
    [    0.145529] bio: create slab <bio-0> at 0
    [    0.163004] raid6: mmxx1     3941 MB/s
    [    0.180007] raid6: mmxx2     4214 MB/s
    [    0.198018] raid6: sse1x1    3363 MB/s
    [    0.215010] raid6: sse1x2    4074 MB/s
    [    0.232009] raid6: sse2x1    6128 MB/s
    [    0.249003] raid6: sse2x2    7355 MB/s
    [    0.249726] raid6: using algorithm sse2x2 (7355 MB/s)
    [    0.250008] raid6: using ssse3x1 recovery algorithm
    [    0.250817] ACPI: Added _OSI(Module Device)
    [    0.251005] ACPI: Added _OSI(Processor Device)
    [    0.251731] ACPI: Added _OSI(3.0 _SCP Extensions)
    [    0.252004] ACPI: Added _OSI(Processor Aggregator Device)
    [    0.253850] ACPI: EC: Look up EC in DSDT
    [    0.256714] ACPI: Interpreter enabled
    [    0.257010] ACPI Exception: AE_NOT_FOUND, While evaluating Sleep State [\_S1_] (20130328/hwxface-568)
    [    0.258609] ACPI Exception: AE_NOT_FOUND, While evaluating Sleep State [\_S2_] (20130328/hwxface-568)
    [    0.260005] ACPI Exception: AE_NOT_FOUND, While evaluating Sleep State [\_S3_] (20130328/hwxface-568)
    [    0.261616] ACPI Exception: AE_NOT_FOUND, While evaluating Sleep State [\_S4_] (20130328/hwxface-568)
    [    0.263014] ACPI: (supports S0 S5)
    [    0.263677] ACPI: Using IOAPIC for interrupt routing
    [    0.264031] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
    [    0.285288] ACPI: No dock devices found.
    [    0.325033] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
    [    0.325865] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configuration space under this bridge.
    [    0.326846] acpiphp: Slot [0] registered
    [    0.327090] acpiphp: Slot [1] registered
    [    0.327906] acpiphp: Slot [2] registered
    [    0.328085] acpiphp: Slot [3] registered
    [    0.328832] acpiphp: Slot [4] registered
    [    0.329085] acpiphp: Slot [5] registered
    [    0.329845] acpiphp: Slot [6] registered
    [    0.330070] acpiphp: Slot [7] registered
    [    0.331110] acpiphp: Slot [8] registered
    [    0.332108] acpiphp: Slot [9] registered
    [    0.333109] acpiphp: Slot [10] registered
    [    0.334114] acpiphp: Slot [11] registered
    [    0.335068] acpiphp: Slot [12] registered
    [    0.335803] acpiphp: Slot [13] registered
    [    0.336121] acpiphp: Slot [14] registered
    [    0.337109] acpiphp: Slot [15] registered
    [    0.338000] acpiphp: Slot [16] registered
    [    0.338068] acpiphp: Slot [17] registered
    [    0.338815] acpiphp: Slot [18] registered
    [    0.339111] acpiphp: Slot [19] registered
    [    0.340111] acpiphp: Slot [20] registered
    [    0.341107] acpiphp: Slot [21] registered
    [    0.342013] acpiphp: Slot [22] registered
    [    0.342733] acpiphp: Slot [23] registered
    [    0.343067] acpiphp: Slot [24] registered
    [    0.343804] acpiphp: Slot [25] registered
    [    0.344067] acpiphp: Slot [26] registered
    [    0.344782] acpiphp: Slot [27] registered
    [    0.345067] acpiphp: Slot [28] registered
    [    0.345808] acpiphp: Slot [29] registered
    [    0.346068] acpiphp: Slot [30] registered
    [    0.346787] acpiphp: Slot [31] registered
    [    0.347061] PCI host bridge to bus 0000:00
    [    0.347728] pci_bus 0000:00: root bus resource [bus 00-ff]
    [    0.348005] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7]
    [    0.348796] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff]
    [    0.349004] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff]
    [    0.349820] pci_bus 0000:00: root bus resource [mem 0xf0000000-0xfbffffff]
    [    0.350089] pci 0000:00:00.0: [8086:1237] type 00 class 0x060000
    [    0.351413] pci 0000:00:01.0: [8086:7000] type 00 class 0x060100
    [    0.352770] pci 0000:00:01.1: [8086:7010] type 00 class 0x010180
    [    0.353693] pci 0000:00:01.1: reg 20: [io  0xc320-0xc32f]
    [    0.354754] pci 0000:00:01.2: [8086:7020] type 00 class 0x0c0300
    [    0.355583] pci 0000:00:01.2: reg 20: [io  0xc300-0xc31f]
    [    0.356602] pci 0000:00:01.3: [8086:7113] type 00 class 0x068000
    [    0.356626] * Found PM-Timer Bug on the chipset. Due to workarounds for a bug,
    [    0.356626] * this clock source is slow. Consider trying other clock sources
    [    0.357829] pci 0000:00:01.3: quirk: [io  0x1f40-0x1f7f] claimed by PIIX4 ACPI
    [    0.358524] pci 0000:00:02.0: [1013:00b8] type 00 class 0x030000
    [    0.358668] pci 0000:00:02.0: reg 10: [mem 0xf0000000-0xf1ffffff pref]
    [    0.358769] pci 0000:00:02.0: reg 14: [mem 0xf3000000-0xf3000fff]
    [    0.359436] pci 0000:00:03.0: [5853:0001] type 00 class 0x010000
    [    0.359578] pci 0000:00:03.0: reg 10: [io  0xc000-0xc0ff]
    [    0.359680] pci 0000:00:03.0: reg 14: [mem 0xf2000000-0xf2ffffff pref]
    [    0.360619] pci 0000:00:04.0: [10ec:8139] type 00 class 0x020000
    [    0.360775] pci 0000:00:04.0: reg 10: [io  0xc100-0xc1ff]
    [    0.360892] pci 0000:00:04.0: reg 14: [mem 0xf3001000-0xf30010ff]
    [    0.361820] pci 0000:00:05.0: [10ec:8139] type 00 class 0x020000
    [    0.361966] pci 0000:00:05.0: reg 10: [io  0xc200-0xc2ff]
    [    0.362069] pci 0000:00:05.0: reg 14: [mem 0xf3001100-0xf30011ff]
    [    0.362980] acpi PNP0A03:00: ACPI _OSC support notification failed, disabling PCIe ASPM
    [    0.363005] acpi PNP0A03:00: Unable to request _OSC control (_OSC support mask: 0x08)
    [    0.364056] ACPI: PCI Interrupt Link [LNKA] (IRQs *5 10 11)
    [    0.366173] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 *10 11)
    [    0.368942] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 10 *11)
    [    0.371177] ACPI: PCI Interrupt Link [LNKD] (IRQs *5 10 11)
    [    0.392411] ACPI: Enabled 2 GPEs in block 00 to 1F
    [    0.393009] acpi root: \_SB_.PCI0 notify handler is installed
    [    0.393075] Found 1 acpi root devices
    [    0.393153] vgaarb: device added: PCI:0000:00:02.0,decodes=io+mem,owns=io+mem,locks=none
    [    0.394005] vgaarb: loaded
    [    0.394574] vgaarb: bridge control possible 0000:00:02.0
    [    0.395081] SCSI subsystem initialized
    [    0.395679] ACPI: bus type ATA registered
    [    0.396041] libata version 3.00 loaded.
    [    0.396046] ACPI: bus type USB registered
    [    0.396681] usbcore: registered new interface driver usbfs
    [    0.397013] usbcore: registered new interface driver hub
    [    0.397668] usbcore: registered new device driver usb
    [    0.398075] PCI: Using ACPI for IRQ routing
    [    0.398690] PCI: pci_cache_line_size set to 64 bytes
    [    0.398925] e820: reserve RAM buffer [mem 0x0009a400-0x0009ffff]
    [    0.398928] e820: reserve RAM buffer [mem 0x3fa76000-0x3fffffff]
    [    0.398929] e820: reserve RAM buffer [mem 0x3fc00000-0x3fffffff]
    [    0.399039] HPET: 3 timers in total, 0 timers will be used for per-cpu timer
    [    0.399736] hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0
    [    0.401004] hpet0: 3 comparators, 64-bit 62.500000 MHz counter
    [    0.403026] Switching to clocksource hpet
    [    0.407840] pnp: PnP ACPI init
    [    0.408471] ACPI: bus type PNP registered
    [    0.409131] system 00:00: [mem 0x00000000-0x0009ffff] could not be reserved
    [    0.409819] system 00:00: Plug and Play ACPI device, IDs PNP0c02 (active)
    [    0.409851] system 00:01: [io  0x10c0-0x1141] has been reserved
    [    0.410533] system 00:01: [io  0xb044-0xb047] has been reserved
    [    0.411199] system 00:01: Plug and Play ACPI device, IDs PNP0c02 (active)
    [    0.411239] pnp 00:02: Plug and Play ACPI device, IDs PNP0103 (active)
    [    0.411272] system 00:03: [io  0x08a0-0x08a3] has been reserved
    [    0.411928] system 00:03: [io  0x0cc0-0x0ccf] has been reserved
    [    0.412602] system 00:03: [io  0x04d0-0x04d1] has been reserved
    [    0.413275] system 00:03: Plug and Play ACPI device, IDs PNP0c02 (active)
    [    0.413287] pnp 00:04: [dma 4]
    [    0.413303] pnp 00:04: Plug and Play ACPI device, IDs PNP0200 (active)
    [    0.413339] pnp 00:05: Plug and Play ACPI device, IDs PNP0b00 (active)
    [    0.413355] pnp 00:06: Plug and Play ACPI device, IDs PNP0800 (active)
    [    0.413390] pnp 00:07: Plug and Play ACPI device, IDs PNP0f13 (active)
    [    0.413427] pnp 00:08: Plug and Play ACPI device, IDs PNP0303 PNP030b (active)
    [    0.413451] pnp 00:09: [dma 2]
    [    0.413464] pnp 00:09: Plug and Play ACPI device, IDs PNP0700 (active)
    [    0.413504] pnp 00:0a: Plug and Play ACPI device, IDs PNP0501 (active)
    [    0.413550] pnp 00:0b: Plug and Play ACPI device, IDs PNP0400 (active)
    [    0.431335] pnp: PnP ACPI: found 12 devices
    [    0.432423] ACPI: bus type PNP unregistered
    [    0.469263] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7]
    [    0.469267] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff]
    [    0.469268] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000bffff]
    [    0.469270] pci_bus 0000:00: resource 7 [mem 0xf0000000-0xfbffffff]
    [    0.469304] NET: Registered protocol family 2
    [    0.470116] TCP established hash table entries: 8192 (order: 4, 65536 bytes)
    [    0.470822] TCP bind hash table entries: 8192 (order: 4, 65536 bytes)
    [    0.471528] TCP: Hash tables configured (established 8192 bind 8192)
    [    0.474604] TCP: reno registered
    [    0.475212] UDP hash table entries: 512 (order: 2, 16384 bytes)
    [    0.475875] UDP-Lite hash table entries: 512 (order: 2, 16384 bytes)
    [    0.476631] NET: Registered protocol family 1
    [    0.477343] RPC: Registered named UNIX socket transport module.
    [    0.478028] RPC: Registered udp transport module.
    [    0.478646] RPC: Registered tcp transport module.
    [    0.479292] RPC: Registered tcp NFSv4.1 backchannel transport module.
    [    0.479967] pci 0000:00:00.0: Limiting direct PCI/PCI transfers
    [    0.480659] pci 0000:00:01.0: PIIX3: Enabling Passive Release
    [    0.481371] pci 0000:00:01.0: Activating ISA DMA hang workarounds
    [    0.482625] pci 0000:00:02.0: Boot video device
    [    0.482682] PCI: CLS 0 bytes, default 64
    [    0.483162] audit: initializing netlink socket (disabled)
    [    0.483832] type=2000 audit(1391964819.483:1): initialized
    [    0.484672] bounce pool size: 64 pages
    [    0.486342] VFS: Disk quotas dquot_6.5.2
    [    0.487003] Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
    [    0.488201] NFS: Registering the id_resolver key type
    [    0.488855] Key type id_resolver registered
    [    0.489494] Key type id_legacy registered
    [    0.490150] Installing knfsd (copyright (C) 1996 okir@monad.swb.de).
    [    0.490878] NTFS driver 2.1.30 [Flags: R/W].
    [    0.491569] ROMFS MTD (C) 2007 Red Hat, Inc.
    [    0.492286] JFS: nTxBlock = 7943, nTxLock = 63544
    [    0.494006] SGI XFS with ACLs, security attributes, large block/inode numbers, no debug enabled
    [    0.495401] OCFS2 1.5.0
    [    0.496190] ocfs2: Registered cluster interface o2cb
    [    0.496954] OCFS2 DLMFS 1.5.0
    [    0.497711] OCFS2 User DLM kernel interface loaded
    [    0.498478] OCFS2 Node Manager 1.5.0
    [    0.499376] OCFS2 DLM 1.5.0
    [    0.500147] bio: create slab <bio-1> at 1
    [    0.501048] Btrfs loaded
    [    0.501744] msgmni has been set to 1728
    [    0.503263] async_tx: api initialized (async)
    [    0.504058] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 252)
    [    0.505181] io scheduler noop registered
    [    0.505917] io scheduler deadline registered
    [    0.506699] io scheduler cfq registered (default)
    [    0.507537] pci_hotplug: PCI Hot Plug PCI Core version: 0.5
    [    0.508408] intel_idle: does not run on family 6 model 45
    [    0.508423] GHES: HEST is not enabled!
    [    0.509177] isapnp: Scanning for PnP cards...
    [    0.872712] isapnp: No Plug & Play device found
    [    0.874175] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
    [    0.903623] 00:0a: ttyS0 at I/O 0x3f8 (irq = 4) is a 16550A
    [    0.906507] brd: module loaded
    [    0.907180] Compaq SMART2 Driver (v 2.6.0)
    [    0.907816] HP CISS Driver (v 3.6.26)
    [    0.909075] fnic: Cisco FCoE HBA Driver, ver 1.5.0.22
    [    0.909732] fnic: Successfully Initialized Trace Buffer
    [    0.910985] Adaptec aacraid driver 1.2-0[30200]-ms
    [    0.911900] aic94xx: Adaptec aic94xx SAS/SATA driver version 1.0.3 loaded
    [    0.912685] scsi: <fdomain> Detection failed (no card)
    [    0.913344] sym53c416.c: Version 1.0.0-ac
    [    0.913977] qlogicfas: no cards were found, please specify I/O address and IRQ using iobase= and irq= options
    [    0.914812] qla2xxx [0000:00:00.0]-0005: : QLogic Fibre Channel HBA Driver: 8.05.00.03-k.
    [    0.916343] Emulex LightPulse Fibre Channel SCSI driver 8.3.39
    [    0.916994] Copyright(c) 2004-2009 Emulex.  All rights reserved.
    [    0.917707] Brocade BFA FC/FCOE SCSI driver - version: 3.1.2.1
    [    0.920748] FDC 0 is a S82078B
    [    0.940091] Failed initialization of WD-7000 SCSI card!
    [    1.144344] DC390: clustering now enabled by default. If you get problems load
    [    1.145310]        with "disable_clustering=1" and report to maintainers
    [    1.145993] megaraid cmm: 2.20.2.7 (Release Date: Sun Jul 16 00:01:03 EST 2006)
    [    1.146983] megaraid: 2.20.5.1 (Release Date: Thu Nov 16 15:32:35 EST 2006)
    [    1.147695] megasas: 06.506.00.00-rc1 Sat. Feb. 9 17:00:00 PDT 2013
    [    1.148387] mpt2sas version 14.100.00.00 loaded
    [    1.149109] GDT-HA: Storage RAID Controller Driver. Version: 3.05
    [    1.149794] 3ware Storage Controller device driver for Linux v1.26.02.003.
    [    1.150508] 3ware 9000 Storage Controller device driver for Linux v2.26.02.014.
    [    1.151454] LSI 3ware SAS/SATA-RAID Controller device driver for Linux v3.26.02.000.
    [    1.152511] ipr: IBM Power RAID SCSI Device Driver version: 2.6.0 (November 16, 2012)
    [    1.154076] RocketRAID 3xxx/4xxx Controller driver v1.8
    [    1.155391] stex: Promise SuperTrak EX Driver version: 4.6.0000.4
    [    1.156535] st: Version 20101219, fixed bufsize 32768, s/g segs 256
    [    1.157764] ata_piix 0000:00:01.1: version 2.13
    [    1.157907] ata_piix 0000:00:01.1: setting latency timer to 64
    [    1.158386] scsi2 : ata_piix
    [    1.159589] scsi3 : ata_piix
    [    1.160659] ata1: PATA max MWDMA2 cmd 0x1f0 ctl 0x3f6 bmdma 0xc320 irq 14
    [    1.161877] ata2: PATA max MWDMA2 cmd 0x170 ctl 0x376 bmdma 0xc328 irq 15
    [    1.164592] I2O subsystem v1.325
    [    1.165430] i2o: max drivers = 8
    [    1.166201] I2O Configuration OSM v1.323
    [    1.166961] I2O Bus Adapter OSM v1.317
    [    1.167686] I2O Block Device OSM v1.325
    [    1.168523] I2O SCSI Peripheral OSM v1.316
    [    1.169256] I2O ProcFS OSM v1.316
    [    1.169986] Fusion MPT base driver 3.04.20
    [    1.170730] Copyright (c) 1999-2008 LSI Corporation
    [    1.171512] Fusion MPT SPI Host driver 3.04.20
    [    1.172273] Fusion MPT FC Host driver 3.04.20
    [    1.173071] Fusion MPT SAS Host driver 3.04.20
    [    1.173848] Fusion MPT misc device (ioctl) driver 3.04.20
    [    1.174693] mptctl: Registered with Fusion MPT base driver
    [    1.175481] mptctl: /dev/mptctl @ (major,minor=10,220)
    [    1.176238] Fusion MPT LAN driver 3.04.20
    [    1.177046] i8042: PNP: PS/2 Controller [PNP0303:PS2K,PNP0f13:PS2M] at 0x60,0x64 irq 1,12
    [    1.179829] serio: i8042 KBD port at 0x60,0x64 irq 1
    [    1.180608] serio: i8042 AUX port at 0x60,0x64 irq 12
    [    1.181459] mousedev: PS/2 mouse device common for all mice
    [    1.183622] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input0
    [    1.185122] rtc_cmos 00:05: RTC can wake from S4
    [    1.185983] rtc_cmos 00:05: rtc core: registered rtc_cmos as rtc0
    [    1.186830] rtc_cmos 00:05: alarms up to one day, 114 bytes nvram, hpet irqs
    [    1.187683] md: linear personality registered for level -1
    [    1.188469] md: raid0 personality registered for level 0
    [    1.189253] md: raid1 personality registered for level 1
    [    1.190062] md: raid10 personality registered for level 10
    [    1.190843] md: raid6 personality registered for level 6
    [    1.191638] md: raid5 personality registered for level 5
    [    1.192417] md: raid4 personality registered for level 4
    [    1.193214] md: multipath personality registered for level -4
    [    1.194058] device-mapper: uevent: version 1.0.3
    [    1.194891] device-mapper: ioctl: 4.24.0-ioctl (2013-01-15) initialised: dm-devel@redhat.com
    [    1.196059] Intel P-state driver initializing.
    [    1.196841] Intel pstate controlling: cpu 0
    [    1.197644] cpuidle: using governor ladder
    [    1.198386] cpuidle: using governor menu
    [    1.199165] input: Speakup as /devices/virtual/input/input1
    [    1.199986] initialized device: /dev/synth, node (MAJOR 10, MINOR 25)
    [    1.200851] speakup 3.1.6: initialized
    [    1.201619] synth name on entry is: (null)
    [    1.202605] TCP: cubic registered
    [    1.203555] Initializing XFRM netlink socket
    [    1.204197] NET: Registered protocol family 17
    [    1.204855] Key type dns_resolver registered
    [    1.205609] Using IPI No-Shortcut mode
    [    1.316445] ata1.00: ATA-7: QEMU HARDDISK, 0.10.2, max UDMA/100
    [    1.317276] ata1.00: 41943040 sectors, multi 16: LBA48 
    [    1.318100] ata1.01: ATAPI: QEMU DVD-ROM, 0.10.2, max UDMA/100
    [    1.320568] ata1.00: configured for MWDMA2
    [    1.322378] ata1.01: configured for MWDMA2
    [    1.323735] scsi 2:0:0:0: Direct-Access     ATA      QEMU HARDDISK    0.10 PQ: 0 ANSI: 5
    [    1.325732] scsi 2:0:1:0: CD-ROM            QEMU     QEMU DVD-ROM     0.10 PQ: 0 ANSI: 5
    [    1.327927] sr0: scsi3-mmc drive: 4x/4x xa/form2 tray
    [    1.328707] cdrom: Uniform CD-ROM driver Revision: 3.20
    [    1.329599] sd 2:0:0:0: [sda] 41943040 512-byte logical blocks: (21.4 GB/20.0 GiB)
    [    1.330825] sd 2:0:0:0: [sda] Write Protect is off
    [    1.331615] sd 2:0:0:0: [sda] Mode Sense: 00 3a 00 00
    [    1.331631] sd 2:0:0:0: [sda] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
    [    1.333445] sr 2:0:1:0: Attached scsi CD-ROM sr0
    [    1.336458]  sda: sda1 sda2
    [    1.337425] sd 2:0:0:0: [sda] Attached SCSI disk
    [    1.338233] registered taskstats version 1
    [    1.339409] md: Waiting for all devices to be available before autodetect
    [    1.340288] md: If you don't use raid, use raid=noautodetect
    [    1.341230] md: Autodetecting RAID arrays.
    [    1.341984] md: Scanned 0 and added 0 devices.
    [    1.342726] md: autorun ...
    [    1.343458] md: ... autorun DONE.
    [    1.345977] EXT3-fs (sda1): error: couldn't mount because of unsupported optional features (240)
    [    1.347673] EXT2-fs (sda1): error: couldn't mount because of unsupported optional features (240)
    [    1.358685] EXT4-fs (sda1): mounted filesystem with ordered data mode. Opts: (null)
    [    1.359830] VFS: Mounted root (ext4 filesystem) readonly on device 8:1.
    [    1.364031] devtmpfs: mounted
    [    1.364479] Freeing unused kernel memory: 796k freed
    [    1.365950] Write protecting the kernel text: 10844k
    [    1.366778] Write protecting the kernel read-only data: 2820k
    [    1.367601] NX-protecting the kernel data: 5540k
    [    1.484087] tsc: Refined TSC clocksource calibration: 2593.748 MHz
    [    1.485347] Switching to clocksource tsc
    [    1.560587] loop: module loaded
    [    1.608735] udevd[144]: starting version 182
    [    1.793319] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input2
    [    1.795546] ACPI: Power Button [PWRF]
    [    1.806689] input: Sleep Button as /devices/LNXSYSTM:00/LNXSLPBN:00/input/input3
    [    1.816076] ACPI: Sleep Button [SLPF]
    [    1.830883] parport_pc 00:0b: reported by Plug and Play ACPI
    [    1.832122] parport0: PC-style at 0x378, irq 7 [PCSPP,TRISTATE]
    [    1.844479] microcode: CPU0 sig=0x206d7, pf=0x1, revision=0x710
    [    1.851772] microcode: Microcode Update Driver: v2.00 <tigran@aivazian.fsnet.co.uk>, Peter Oruba
    [    1.877879] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
    [    1.882546] uhci_hcd: USB Universal Host Controller Interface driver
    [    1.896600] uhci_hcd 0000:00:01.2: setting latency timer to 64
    [    1.896794] uhci_hcd 0000:00:01.2: UHCI Host Controller
    [    1.898752] Linux agpgart interface v0.103
    [    1.907460] uhci_hcd 0000:00:01.2: new USB bus registered, assigned bus number 1
    [    1.914863] uhci_hcd 0000:00:01.2: irq 23, io base 0x0000c300
    [    1.921820] usb usb1: New USB device found, idVendor=1d6b, idProduct=0001
    [    1.922548] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
    [    1.923497] usb usb1: Product: UHCI Host Controller
    [    1.924166] usb usb1: Manufacturer: Linux 3.10.17-smp uhci_hcd
    [    1.924852] usb usb1: SerialNumber: 0000:00:01.2
    [    1.931364] 8139too: 8139too Fast Ethernet driver 0.9.28
    [    1.932546] hub 1-0:1.0: USB hub found
    [    1.937543] hub 1-0:1.0: 2 ports detected
    [    1.951061] piix4_smbus 0000:00:01.3: SMBus base address uninitialized - upgrade BIOS or use force_addr=0xaddr
    [    1.954249] 8139too 0000:00:04.0: This (id 10ec:8139 rev 20) is an enhanced 8139C+ chip, use 8139cp
    [    1.955889] 8139too 0000:00:05.0: This (id 10ec:8139 rev 20) is an enhanced 8139C+ chip, use 8139cp
    [    2.070182] ppdev: user-space parallel port driver
    [    2.249416] usb 1-2: new full-speed USB device number 2 using uhci_hcd
    [    2.372799] Adding 1436476k swap on /dev/sda2.  Priority:-1 extents:1 across:1436476k 
    [    2.889796] usb 1-2: New USB device found, idVendor=0627, idProduct=0001
    [    2.890761] usb 1-2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
    [    2.891473] usb 1-2: Product: QEMU USB Tablet
    [    2.892091] usb 1-2: Manufacturer: QEMU 0.10.2
    [    2.892711] usb 1-2: SerialNumber: 1
    [    3.044851] input: ImExPS/2 Generic Explorer Mouse as /devices/platform/i8042/serio1/input/input4
    [    3.081955] hidraw: raw HID events driver (C) Jiri Kosina
    [    3.161120] usbcore: registered new interface driver usbhid
    [    3.161121] usbhid: USB HID core driver
    [    3.167517] input: QEMU 0.10.2 QEMU USB Tablet as /devices/pci0000:00/0000:00:01.2/usb1/1-2/1-2:1.0/input/input5
    [    3.173831] hid-generic 0003:0627:0001.0001: input,hidraw0: USB HID v0.01 Pointer [QEMU 0.10.2 QEMU USB Tablet] on usb-0000:00:01.2-2/input0
    [    3.218091] EXT4-fs (sda1): re-mounted. Opts: (null)
    [    3.684534] lp0: using parport0 (interrupt-driven).
    [    3.685325] lp0: console ready
    [    3.699109] 8139cp: 8139cp: 10/100 PCI Ethernet driver v1.3 (Mar 22, 2004)
    [    3.711970] 8139cp 0000:00:04.0 eth0: RTL-8139C+ at 0xf8954000, bc:76:4e:08:7a:b0, IRQ 32
    [    3.727870] 8139cp 0000:00:05.0 eth1: RTL-8139C+ at 0xf8956100, bc:76:4e:08:a5:85, IRQ 36
    [   10.673925] 8139cp 0000:00:04.0 eth0: link up, 100Mbps, full-duplex, lpa 0x05E1
    [   15.021729] NET: Registered protocol family 10
    root@slack:~# 
