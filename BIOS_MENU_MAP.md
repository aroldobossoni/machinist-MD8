# BIOS Menu Tree - Machinist MD8 (X99 MD8)

**BIOS Version:** M94X8 3.00 x64  
**Build Date:** 10/12/2024 10:35:51  
**Vendor:** American Megatrends  

---

## Árvore Completa da BIOS

```
Aptio Setup Utility
│
├── Main
│   
│   BIOS Information
│     • Manufacturer: MACHINIST
│     • Model: X99 MD8
│     • BIOS Vendor: American Megatrends
│     • Core Version: 5.11
│     • Compliancy: UEFI 2.4; PI 1.3
│     • Project Version: M94X8 3.00 x64
│     • Build Date and Time: 10/12/2024 10:35:51
│     • Access Level: Administrator
│   
│   Memory Information
│     • Total Memory: (detected MB)
│   
│   - System Language: [English]
│   - System Date: [MM/DD/YYYY]
│   - System Time: [HH:MM:SS]
│
├── Advanced
│   │
│   ├── ACPI Settings >
│   │   - Enable ACPI Auto Configuration: [Disabled]
│   │   - Enable Hibernation: [Enabled]
│   │   - Lock Legacy Resources: [Disabled]
│   │
│   ├── NCT5532D Super IO Configuration >
│   │   │
│   │   │ Super IO Chip: NCT5532D
│   │   │
│   │   └── Serial Port 1 Configuration >
│   │       - Serial Port: [Enabled]
│   │       - Device Settings: IO=3F8h; IRQ=4;
│   │       - Change Settings: [Auto]
│   │
│   ├── Hardware Monitor >
│   │   │
│   │   Pc Health Status
│   │       │
│   │       - Smart Fan Function: [Enabled]
│   │       │
│   │       ├── Smart Fan Mode Configuration >
│   │       │   - Cpu Fan Mode: [SmartFan TM IV Mode]
│   │       │   - CPU Fan Full Speed Temp: 70
│   │       │   - CPU Fan Start Temp Value: 35
│   │       │   - CPU Fan Start PWM Value: 120
│   │       │   │
│   │       │   └── Smart Fan IV mode
│   │       │       • T1:35 Duty:100/255
│   │       │       • T2:45 Duty:160/255
│   │       │       • T3:55 Duty:200/255
│   │       │       • T4:65 Duty:230/255
│   │       │       • Critical:70 Duty:100%
│   │       │
│   │       Sensors (readings)
│   │         • CPU Temperature: (current value)
│   │         • CPU Fan1 Speed: (current RPM)
│   │         • CPU Fan2 Speed: (current RPM)
│   │         • VDIMM: (current voltage)
│   │         • +12V: (current voltage)
│   │         • VCC3V: (current voltage)
│   │         • VSB3V: (current voltage)
│   │         • VBAT: (current voltage)
│   │         • VTT: (current voltage)
│   │         • AVCC: (current voltage)
│   │
│   ├── RTC Wakeup Configuration >
│   │   - Wakeup By RTC: [Disabled]
│   │
│   ├── iSCSI Configuration >
│   │   │
│   │   │ iSCSI Initiator Name: (IQN)
│   │   │
│   │   ├── Add an Attempt >
│   │   ├── Delete Attempts >
│   │   └── Change Attempt Order >
│   │
│   ├── Realtek PCIe GBE Family Controller 1 >
│   │   │
│   │   Driver Information
│   │     • Driver Name: Realtek UEFI UNDI Driver
│   │     • Driver Version: X.XXX
│   │     • Driver Released Date: (Date)
│   │   
│   │   Device Information
│   │     • Device Name: Realtek PCIe GBE Family
│   │     • PCI Slot: XX:XX:XX
│   │     • MAC Address: XX:XX:XX:XX:XX:XX
│   │
│   ├── Realtek PCIe GBE Family Controller 2 >
│   │   │
│   │   Driver Information
│   │     • Driver Name: Realtek UEFI UNDI Driver
│   │     • Driver Version: X.XXX
│   │     • Driver Released Date: (Date)
│   │   
│   │   Device Information
│   │     • Device Name: Realtek PCIe GBE Family
│   │     • PCI Slot: XX:XX:XX
│   │     • MAC Address: XX:XX:XX:XX:XX:XX
│   │
│   ├── PCI Subsystem Settings >
│   │   │
│   │   │ PCI Bus Driver Version: (version)
│   │   │
│   │   PCI Devices Common Settings
│   │     - PCI Latency Timer: [32 PCI Bus Clocks]
│   │     - PCI-X Latency Timer: [64 PCI Bus Clocks]
│   │     - VGA Palette Snoop: [Disabled]
│   │     - PERR# Generation: [Disabled]
│   │     - SERR# Generation: [Disabled]
│   │     - Above 4G Decoding: [Disabled]
│   │     - Re-Size BAR Support: [Disabled]
│   │     - SR-IOV Support: [Disabled]
│   │     - BME DMA Mitigation: [Disabled]
│   │   
│   │   ├── PCI Express Settings >
│   │   │   │
│   │   │   PCI Express Device Register Settings
│   │   │     - Relaxed Ordering: [Disabled]
│   │   │     - Extended Tag: [Disabled]
│   │   │     - No Snoop: [Enabled]
│   │   │     - Maximum Payload: [Auto]
│   │   │   
│   │   │   PCI Express Link Register Settings
│   │   │     - Extended Synch: [Disabled]
│   │   │     - Link Training Retry: [5]
│   │   │     - Link Training Timeout (uS): [1000]
│   │   │     - Restore PCIE Registers: [Disabled]
│   │   │
│   │   └── PCI Express GEN 2 Settings >
│   │       │
│   │       PCI Express GEN2 Device Register Settings
│   │         - Completion Timeout: [Default]
│   │         - ARI Forwarding: [Disabled]
│   │         - AtomicOp Requester Enable: [Disabled]
│   │         - AtomicOp Egress Blocking: [Disabled]
│   │         - IDO Request Enable: [Disabled]
│   │         - IDO Completion Enable: [Disabled]
│   │         - LTR Mechanism Enable: [Disabled]
│   │         - End-End TLP Prefix Blocking: [Disabled]
│   │       
│   │       PCI Express GEN2 Link Register Settings
│   │         - Clock Power Management: [Disabled]
│   │         - Compliance SOS: [Disabled]
│   │         - Hardware Autonomous Width: [Enabled]
│   │         - Hardware Autonomous Speed: [Enabled]
│   │
│   ├── Network Stack Configuration >
│   │   - Network Stack: [Disabled]
│   │
│   ├── CSM Configuration >
│   │   - CSM Support: [Enabled]
│   │   - Boot option filter: [UEFI and Legacy]
│   │   - Option ROM execution: [Do not launch]
│   │   - Network: [Legacy]
│   │   - Storage: [Legacy]
│   │   - Video: [Legacy]
│   │
│   ├── NVMe Configuration >
│   │   │
│   │   NVMe controller and Drive information
│   │     (displays connected NVMe devices)
│   │
│   └── USB Configuration >
│       │
│       USB Information
│         • USB Module Version: 11
│         • USB Controllers: 2 EHCIs, 1 XHCI
│         • USB Devices: (detected devices)
│       
│       - Legacy USB Support: [Enabled]
│       - XHCI Hand-off: [Enabled]
│       - EHCI Hand-off: [Disabled]
│       - USB Mass Storage Driver Support: [Enabled]
│       │
│       USB hardware delays and time-outs
│         - USB transfer time-out: [20 sec]
│         - Device reset time-out: [20 sec]
│         - Device power-up delay: [Auto]
│
├── IntelRCSetup
│   │
│   │ RC Revision: 04.04.00
│   │
│   ├── Processor Configuration >
│   │   │
│   │   ├── Per-Socket Configuration >
│   │   │   │
│   │   │   Socket 0 (Detected CPU)
│   │   │     • Processor Socket: (populated/empty)
│   │   │     • Processor ID: XXXXXXXX
│   │   │     • Processor Frequency: X.XXX GHz
│   │   │     • Processor Max Ratio: XXH
│   │   │     • Processor Min Ratio: XXH
│   │   │     • Microcode Revision: XXXXXXXX
│   │   │     • L1 Cache RAM: XXX KB
│   │   │     • L2 Cache RAM: XXXX KB
│   │   │     • L3 Cache RAM: XXXXX KB
│   │   │   
│   │   │   Socket 1
│   │   │     • Processor 1 Version: Not Present
│   │   │
│   │   - Hyper-Threading [ALL]: [Enable]
│   │   - Check CPU BIST Result: [Disabled]
│   │   - Monitor/Mwait: [Enable]
│   │   - Execute Disable Bit: [Enable]
│   │   - Enable Intel TXT Support: [Disable]
│   │   - VMX: [Enable]
│   │   - Enable SMX: [Disable]
│   │   - Lock Chipset: [Enable]
│   │   - MSR Lock Control: [Enable]
│   │   - PPIN Control: [Unlock/Enable]
│   │   - DEBUG INTERFACE: [Disable]
│   │   - Hardware Prefetcher: [Enable]
│   │   - Adjacent Cache Prefetch: [Enable]
│   │   - DCU Streamer Prefetcher: [Enable]
│   │   - DCU IP Prefetcher: [Enable]
│   │   - DCU Mode: [32KB 8Way Without ECC]
│   │   - Direct Cache Access (DCA): [Auto]
│   │   - DCA Prefetch Delay: [32]
│   │   - X2APIC: [Disable]
│   │   - AES-NI: [Enable]
│   │   - Down Stream PECI: [Enable]
│   │   - IIO LLC Ways [19:0] (Hex): 0
│   │   - QLRU Config [63:32] (Hex): 0
│   │   - QLRU Config [31:0] (Hex): 0
│   │   - SMM Save State: [Disable]
│   │   - Targeted Smi: [Disable]
│   │
│   ├── Advanced Power Management Configuration >
│   │   │
│   │   - Power Technology: [Custom]
│   │   - Config TDP: [Disable]
│   │   - IOTG Setting: [Disable]
│   │   - Uncore CLR Freq OVRD: [Auto]
│   │   │
│   │   ├── CPU P State Control >
│   │   │   - EIST (P-states): [Enable]
│   │   │   - Turbo Mode: [Enable]
│   │   │   - P-state coordination: [HW_ALL]
│   │   │   - SPD: [Disable]
│   │   │   - PL2_SAFETY_NET_ENABLE: [Enable]
│   │   │   - Boot performance mode: [Max Performance]
│   │   │
│   │   ├── CPU HWPM State Control >
│   │   │   - Enable CPU HWPM: [Disable]
│   │   │   - Enable CPU Autonomous Cstate: [Disable]
│   │   │
│   │   ├── CPU C State Control >
│   │   │   - C2C3TT: 0
│   │   │   - Package C State limit: [C0/C1 state]
│   │   │   - CPU C3 report: [Enable]
│   │   │   - CPU C6 report: [Enable]
│   │   │
│   │   ├── CPU T State Control >
│   │   │   - ACPI T-States: [Enable]
│   │   │
│   │   ├── CPU - Advanced PM Tuning >
│   │   │   └── Energy Perf BIAS >
│   │   │
│   │   ├── SOCKET RAPL Config >
│   │   │
│   │   └── DRAM RAPL Configuration >
│   │       - DRAM RAPL Baseline: [DRAM RAPL Mode 1]
│   │       - Override BW_LIMIT_TF: 1
│   │       - DRAM RAPL Extended Range: [Enable]
│   │
│   ├── Common RefCode Configuration >
│   │   - MMIOHBase: [56T]
│   │   - MMIO High Size: [256G]
│   │   - Isoc Mode: [Auto]
│   │   - MeSeg Mode: [Auto]
│   │   - Numa: [Enable]
│   │
│   ├── QPI Configuration >
│   │   │
│   │   ├── QPI General Configuration >
│   │   │   │
│   │   │   QPI Status
│   │   │   │   │
│   │   │   │   QPI Status Information
│   │   │   │     • Number of CPU: (detected)
│   │   │   │     • Number of IIO: (detected)
│   │   │   │     • Current QPI Link Speed: (current speed)
│   │   │   │     • Current QPI Link Frequency: (frequency)
│   │   │   │     • QPI Global MMIO Low Base / Limit: (address range)
│   │   │   │     • QPI Global MMIO High Base / Limit: (address range)
│   │   │   │     • QPI Pci-e Configuration Base / Size: (address/size)
│   │   │   │
│   │   │   - Degrade Precedence: [Topology Precedence]
│   │   │   - Link Frequency Select: [Auto]
│   │   │   - Link L0p Enable: [Enable]
│   │   │   - Link L1 Enable: [Enable]
│   │   │   - Legacy VGA Socket: 0
│   │   │   - MMIO P2P Disable: [no]
│   │   │   - E2E Parity Enable: [Disable]
│   │   │   - COD Enable: [Auto]
│   │   │   - Early Snoop: [Auto]
│   │   │   - Home Dir Snoop with IVT-Style OSB: [Auto]
│   │   │   - QPI Debug Print Level: [All]
│   │   │
│   │   └── QPI Per Socket Configuration >
│   │       │
│   │       ├── CPU 0 >
│   │       │   - Bus Resources Allocation Ratio: 1
│   │       │   - IO Resources Allocation Ratio: 1
│   │       │   - MMIOL Resources Allocation Ratio: 1
│   │       │   - IIO Disable: [no]
│   │       │
│   │       ├── CPU 1 >
│   │       │   - Bus Resources Allocation Ratio: 1
│   │       │   - IO Resources Allocation Ratio: 1
│   │       │   - MMIOL Resources Allocation Ratio: 1
│   │       │   - IIO Disable: [no]
│   │       │
│   │       ├── CPU 2 >
│   │       │   - Bus Resources Allocation Ratio: 1
│   │       │   - IO Resources Allocation Ratio: 1
│   │       │   - MMIOL Resources Allocation Ratio: 1
│   │       │   - IIO Disable: [no]
│   │       │
│   │       └── CPU 3 >
│   │           - Bus Resources Allocation Ratio: 1
│   │           - IO Resources Allocation Ratio: 1
│   │           - MMIOL Resources Allocation Ratio: 1
│   │           - IIO Disable: [no]
│   │
│   ├── Memory Configuration >
│   │   │
│   │   Integrated Memory Controller (IMC)
│   │     - Enforce POR: [Disabled]
│   │     - PPR Type: [PPR Disabled]
│   │     - PPR Error Injection test: [Disabled]
│   │     - Memory Frequency: [Auto]
│   │     - MRC Promote Warnings: [Enabled]
│   │     - Promote Warnings: [Enabled]
│   │     - Halt on mem Training Error: [Enabled]
│   │     - Multi-Threaded MRC: [Auto]
│   │     - Enforce Timeout: [Auto]
│   │     - Enhanced Log Parsing: [Disable]
│   │     - BSSA Module Loader: [Auto]
│   │     - Backside RMT: [Auto]
│   │     - Rank Multiplication: [Auto]
│   │     - LRDIMM Module Delay: [Auto]
│   │     - MemTest: [Disable]
│   │     - MemTestLoops: 1
│   │     - Dram Maintenance Test: [Auto]
│   │     - Dram Maintenance Test Direction: [UP Direction]
│   │     - Dram Maintenance Test Invertion: [Disabled]
│   │     - Dram Maintenance Test Repetitions: 3
│   │     - Dram Maintenance Test Interation o: 1
│   │     - Dram Maintenance Swizzle enabling: [Auto]
│   │     - Dram Maintenance Refresh enabling: [Enabled]
│   │     - Memory Type: [UDIMMs and RDIMMs]
│   │     - CECC WA CH Mask: 10
│   │     - Rank Margin Tool: [Auto]
│   │     - RMT Pattern Length: 32767
│   │     - CMD Pattern Length: 1
│   │     - Per Bit Margin: [Auto]
│   │     - Training Result Offset Config: [Auto]
│   │     - Attempt Fast Boot: [Enable]
│   │     - Attempt Fast Cold Boot: [Auto]
│   │     - MemTest On Fast Boot: [Auto]
│   │     - RMT On Cold Fast Boot: [Auto]
│   │     - BDAT: [Disabled]
│   │     - Data Scrambling: [Auto]
│   │     - Allow SBE during training: [Auto]
│   │     - WR CRC feature Control: [Auto]
│   │     - Platform type input for SPD page s: [Auto]
│   │     - CECC WA Control: [Auto]
│   │     - CAP ERR FLOW feature Control: [Auto]
│   │     - Scrambling Seed Low: 41003
│   │     - Scrambling Seed High: 54165
│   │     - Enable ADR: [Disabled]
│   │     - MC BGF threshold: 0
│   │     - DLL Reset Test: 0
│   │     - MC ODT Mode: [Auto]
│   │     - Opp read during WMM: [Auto]
│   │     - Normal Operation Duration: 1024
│   │     - Number of Sparing Transaction: 4
│   │     - PSMI Support: [Disabled]
│   │     - C/A Parity Enable: [Auto]
│   │     - SMB Clock Frequency: [Auto]
│   │   
│   │   ├── Memory Topology >
│   │   │   │
│   │   │   Detected DIMMs
│   │   │     • Socket0.ChX.DimmX: (DIMM information when installed)
│   │   │
│   │   ├── Memory Thermal >
│   │   │   - Set Throttling Mode: [CLTT]
│   │   │   - OLTT Peak BW %: 50
│   │   │   - Phase Shedding: [Auto]
│   │   │   - Memory Power Savings Mode: [Auto]
│   │   │   │
│   │   │   ├── Memory Power Savings Advanced Options >
│   │   │   │   - CK in SR: [Auto]
│   │   │   │
│   │   │   - MDLL Off: [Auto]
│   │   │   - MEMHOT Throttling Mode: [Input-only]
│   │   │   - Mem Electrical Throttling: [Disabled]
│   │   │
│   │   ├── Memory Timings & Voltage Override >
│   │   │   - DIMM profile: [Disabled]
│   │   │   - Memory Frequency: [Auto]
│   │   │
│   │   ├── Memory Map >
│   │   │   - Socket Interleave Below 4GB: [Disable]
│   │   │   - Channel Interleaving: [Auto]
│   │   │   - Rank Interleaving: [Auto]
│   │   │   - IOT Memory Buffer Reservation: 0
│   │   │   - A7 Mode: [Enable]
│   │   │
│   │   ├── Memory RAS Configuration >
│   │   │   - RAS Mode: [Disable]
│   │   │   - Lockstep x4 DIMMs: [Auto]
│   │   │   - Memory Rank Sparing: [Disabled]
│   │   │   - Correctable Error Threshold: 32767
│   │   │   - Leaky bucket low bit: 40
│   │   │   - Leaky bucket high bit: 41
│   │   │   - DRAM Maintenance: [Auto]
│   │   │   - Patrol Scrub: [Enable]
│   │   │   - Patrol Scrub Interval: 24
│   │   │   - Demand Scrub: [Enable]
│   │   │   - Device Tagging: [Disable]
│   │   │   - Handle Hard Error Detection: [Disable]
│   │   │   - Memory Power Management: [Disable]
│   │   │
│   │   └── DIMM Rank Enable Mask: [Disabled]
│   │
│   ├── IIO Configuration >
│   │   │
│   │   - IIO PCIe Link on phase: [Post chipset init]
│   │   - PCIe Train by BIOS: [yes]
│   │   - PCIe Hot Plug: [Disable]
│   │   - PCIe ACPI Hot Plug: [Disable]
│   │   - EV DFX Features: [Disable]
│   │   │
│   │   ├── IIOO Configuration >
│   │   │   │
│   │   │   │ IIO O
│   │   │   │
│   │   │   - IIO IOAPIC: [Enable]
│   │   │
│   │   ├── IOAT Configuration >
│   │   │   - Enable IOAT: [Disable]
│   │   │   - No Snoop: [Disable]
│   │   │   - Disable TPH: [Enable]
│   │   │   - Relaxed Ordering: [Disable]
│   │   │   - Apply BDX CBDMA ECO: [no]
│   │   │
│   │   ├── IIO General Configuration >
│   │   │   │
│   │   │   PCI Express Global Options
│   │   │     - TX EQ WA: [Enable]
│   │   │     - DMI Vc1 Control: [Disable]
│   │   │     - DMI Vcp Control: [Disable]
│   │   │     - DMI Vcm Control: [Disable]
│   │   │     - VCO No-Snoop Configuration: [Disable]
│   │   │     - Gen3 Phase3 Loop Count: [16]
│   │   │     - Skip Halt On DMI Degradation: [Disable]
│   │   │     - Power down unused ports: [yes]
│   │   │     - SLD WA Revision: [Auto]
│   │   │     - Rx Clock WA: [Disable]
│   │   │     - PCI-E ASPM (Global): [Disable]
│   │   │     - PCIE Stop & Scream Support: [Disable]
│   │   │     - Snoop Response Hold Off: 6
│   │   │   
│   │   │   PCIe Port Bifurcation Options
│   │   │     - IOU2 (IIO PCIe Port 1): [x4x4]
│   │   │     - IOU0 (IIO PCIe Port 2): [x8x8]
│   │   │     - IOU1 (IIO PCIe Port 3): [x16]
│   │   │     - No PCIe port active ECO: [PCU Squelch exit ig...]
│   │   │     - IOU0 Non-Posted Prefetch: [Disable]
│   │   │     - IOU1 Non-Posted Prefetch: [Disable]
│   │   │     - IOU2 Non-Posted Prefetch: [Disable]
│   │   │   
│   │   │   ├── Socket 0 PcieD00F0 - Port 0/DMI >
│   │   │   │   - Link Speed: [Auto]
│   │   │   │   - Override Max Link Width: [Auto]
│   │   │   │   - PCI-E Port DeEmphasis: [-6.0 dB]
│   │   │   │   - PCI-E Port Link Status: (link status)
│   │   │   │   - PCI-E Port Link Max: (max width)
│   │   │   │   - PCI-E Port Link Speed: (current speed)
│   │   │   │   - PCI-E ASPM: [Disable]
│   │   │   │   - Fatal Err Over: [Disable]
│   │   │   │   - Non-Fatal Err Over: [Disable]
│   │   │   │   - Corr Err Over: [Disable]
│   │   │   │   - LOs Support: [Disable]
│   │   │   │
│   │   │   ├── Socket 0 PcieD01F0 - Port 1A >
│   │   │   │   - PCI-E Port: [Auto]
│   │   │   │   - Hot Plug Capable: [Disable]
│   │   │   │   - Extra Bus Reserved: 0
│   │   │   │   - Reserved Memory: 10
│   │   │   │   - Reseved Memory Alignment: 1
│   │   │   │   - Prefetchable Memory: 10
│   │   │   │   - Prefetchable Memory Alignment: 1
│   │   │   │   - Reserved I/O: 0
│   │   │   │   - PCI-E Port Link: [Enable]
│   │   │   │   - Link Speed: [Auto]
│   │   │   │   - Override Max Link Width: [Auto]
│   │   │   │   - PCI-E Port DeEmphasis: [-6.0 dB]
│   │   │   │   - PCI-E Port Link Status: Link Did Not Train
│   │   │   │   - PCI-E Port Link Max: Max Width x4
│   │   │   │   - PCI-E Port Link Speed: Link Did Not Train
│   │   │   │   - PCI-E ASPM: [Disable]
│   │   │   │   - Fatal Err Over: [Disable]
│   │   │   │   - Non-Fatal Err Over: [Disable]
│   │   │   │   - Corr Err Over: [Disable]
│   │   │   │   - LOs Support: [Disable]
│   │   │   │   - PM ACPI Mode: [Disable]
│   │   │   │   - Gen3 Eq Mode: [Auto]
│   │   │   │   - Gen3 Spec Mode: [Auto]
│   │   │   │   - Gen3 Phase2 Mode: [Hardware Adaptive]
│   │   │   │   - Gen3 DN TX Preset: [Auto]
│   │   │   │   - Gen3 DN Rx Preset Hint: [Auto]
│   │   │   │   - Gen3 UP Tx Preset: [Auto]
│   │   │   │   - Hide Port?: [no]
│   │   │   │   - Pcie Ecrc: [Auto]
│   │   │   │
│   │   │   ├── Socket 0 PcieD01F1 - Port 1B >
│   │   │   │   • (Same options as Port 1A)
│   │   │   │
│   │   │   ├── Socket 0 PcieD02F0 - Port 2A >
│   │   │   │   • (Same options as Port 1A)
│   │   │   │
│   │   │   ├── Socket 0 PcieD02F2 - Port 2C >
│   │   │   │   • (Same options as Port 1A)
│   │   │   │   - PCI-E Port Link Status: (link status)
│   │   │   │
│   │   │   └── Socket 0 PcieD03F0 - Port 3A >
│   │   │       • (All Port 1A options)
│   │   │       - PCI-E Port Link Status: (link status)
│   │   │       - PCI-E Port Link Speed: (current speed)
│   │   │       - Non-Transparent Bridge PCIe Port D: [Auto]
│   │   │       - Enable NTB BARS: [Enabled]
│   │   │       - Enable SPLIT BARS: [Enabled]
│   │   │       - Primary BAR 23 Size: 22
│   │   │       - Primary BAR 4 Size: 20
│   │   │       - Primary BAR 5 Size: 20
│   │   │       - Secondary BAR 23 Size: 20
│   │   │
│   │   └── Intel VT for Directed I/O (VT-d) >
│   │       - VTd Azalea VCp Optimizations: [Disable]
│   │       - Intel VT for Directed I/O (VT-d): [Enable]
│   │       - ACS Control: [Enable]
│   │       - Interrupt Remapping: [Enable]
│   │       - Coherency Support (Non-Isoch): [Enable]
│   │       - Coherency Support (Isoch): [Enable]
│   │
│   └── PCH Configuration >
│       │
│       ├── PCH Devices >
│       │   - Board Capability: [DeepSx]
│       │   - DeepSx Power Policies: [Disabled]
│       │   - GP27 Wake From DeepSx: [Disabled]
│       │   - SMBUS Device: [Enabled]
│       │   - PCH Server Error Reporting Mode (S): [Disabled]
│       │   - PCH Display: [Enabled]
│       │   - Serial IRQ Mode: [Continuous]
│       │   - External SSC Enable - CK420: [Disabled]
│       │   - PCH state after G3: [Off]
│       │   - PCH CRID: [Disabled]
│       │
│       ├── PCH sSATA Configuration >
│       │   │
│       │   - sSATA Controller: [Enabled]
│       │   - Configure sSATA as: [AHCI]
│       │   - SATA test mode: [Disabled]
│       │   - SATA Mode options >
│       │   - sSATA Mode options
│       │   - sSATA AHCI LPM: [Enabled]
│       │   - sSATA AHCI ALPM: [Enabled]
│       │   │
│       │   ├── sSATA Port 0
│       │   │   │ Port 0: (Detected Device)
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── sSATA Port 1
│       │   │   │ Port 1: (Detected Device)
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── sSATA Port 2
│       │   │   │ Port 2: (Detected Device)
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── sSATA Port 3
│       │   │   │ Port 3: (Not Installed)
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── sSATA Port 4
│       │   │   │ Software Preserve: [Not Installed]
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── sSATA Port 5
│       │   │   │ Software Preserve: [Not Installed]
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - sSATA Device Type: [Hard Disk Drive]
│       │   │
│       │   - SATA HDD Unlock: [Enabled]
│       │   - SATA Led locate: [Enabled]
│       │
│       ├── PCH SATA Configuration >
│       │   │
│       │   - SATA Controller: [Enabled]
│       │   - Configure SATA as: [AHCI]
│       │   - SATA test mode: [Disabled]
│       │   - SATA Mode options >
│       │   - SATA AHCI LPM: [Enabled]
│       │   - SATA AHCI ALPM: [Enabled]
│       │   │
│       │   ├── SATA Port 0
│       │   │   │ Port 0: (Detected Device)
│       │   │   │ Software Preserve: (Status)
│       │   │   - Port 0: [Enabled]
│       │   │   - Hot Plug: [Disabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Configured as eSATA: Hot Plug supported
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - SATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── SATA Port 1
│       │   │   │ Port 1: (Detected Device)
│       │   │   │ Software Preserve: (Status)
│       │   │   - Port 1: [Enabled]
│       │   │   - Hot Plug: [Disabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Configured as eSATA: Hot Plug supported
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - SATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── SATA Port 3
│       │   │   │ Software Preserve: [Not Installed]
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - SATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── SATA Port 4
│       │   │   │ Software Preserve: [Not Installed]
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - SATA Device Type: [Hard Disk Drive]
│       │   │
│       │   ├── SATA Port 5
│       │   │   │ Software Preserve: [Not Installed]
│       │   │   - Hot Plug: [Enabled]
│       │   │   - Configure as eSATA: [Disabled]
│       │   │   - Spin Up Device: [Disabled]
│       │   │   - SATA Device Type: [Hard Disk Drive]
│       │   │
│       │   - SATA Led locate: [Enabled]
│       │
│       ├── USB Configuration >
│       │   - USB Precondition: [Disabled]
│       │   - XHCI Mode: [Auto]
│       │   - Trunk Clock Gating (BTCG): [Enabled]
│       │   - USB Ports Per-Port Disable Control: [Disabled]
│       │   - XHCI Idle L1: [Enabled]
│       │   - USB XHCI s755 WA: [Enabled]
│       │
│       ├── Security Configuration >
│       │   - GPIO Lockdown: [Disabled]
│       │   - RTC Lock: [Enabled]
│       │   - BIOS Lock: [Disabled]
│       │   - Host Flash Lock-Down: [Disabled]
│       │   - Gbe Flash Lock-Down: [Disabled]
│       │
│       - Onboard LAN1 Control: [Enabled]
│       - Onboard LAN2 Control: [Enabled]
│
├── Security
│   │
│   Password Description
│     • If ONLY the Administrator's password is set, then this only limits
│       access to Setup and is only asked for when entering Setup.
│     • If ONLY the User's password is set, then this is a power on password
│       and must be entered to boot or enter Setup. In Setup the User will
│       have Administrator rights.
│   
│   Password Length Range
│     • Minimum length: 3
│     • Maximum length: 20
│   
│   - Administrator Password: (Set/Change)
│   - User Password: (Set/Change)
│
├── Boot
│   │
│   Boot Configuration
│     - Boot Option #1: [Device Name]
│     - Boot Option #2: [Device Name]
│
└── Save & Exit
    │
    Save Options
      - Save Changes and Exit
      - Discard Changes and Exit
      - Save Changes and Reset
      - Discard Changes and Reset
      - Save Changes
      - Discard Changes
    
    Default Options
      - Restore Defaults
      - Save as User Defaults
      - Restore User Defaults
    
    Boot Override
      • UEFI: Built-in EFI Shell
      • UEFI OS (Detected OS Device)
      • sSATA P0: (Detected Device)
      • sSATA P1: (Detected Device)
      • sSATA P2: (Detected Device)
      • sSATA P3: (Detected Device)
      • SATA0 P0: (Detected Device)
      • SATA0 P1: (Detected Device)
```

---

## Legenda de Formatação

| Símbolo | Significado |
|---------|-------------|
| `├──` ou `└──` | **Submenu clicável** (tem `>` na BIOS) |
| `-` | Item configurável / campo de entrada |
| `•` | Valor informativo / leitura de sensor / item de lista |
| Texto simples | Seção descritiva / título de grupo |

---

## Teclas de Atalho (Hotkeys)

| Tecla | Função |
|-------|--------|
| ↔ | Select Screen |
| ↑↓ | Select Item |
| Enter | Select |
| +/- | Change Option |
| F1 | General Help |
| F2 | Previous Values |
| F9 | Optimized Defaults |
| F10 | Save & Exit |
| ESC | Exit |

---

**Data:** 11/11/2025  
**BIOS Version:** M94X8 3.00 x64 (Build: 10/12/2024)
