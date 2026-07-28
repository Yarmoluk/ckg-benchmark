## META
domain: hardware-security
version: 0.1.0
nodes: 12
edges: 14
created: 2026-07-27
author: Daniel Yarmoluk / Graphify.md
description: Hardware attack paths — secure boot bypass, fault injection, firmware manipulation

## GRAPH
```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
FI1,Fault Injection Attack,,AttackPrimitive
FI2,Voltage Glitching,FI1,AttackPrimitive
FI3,Clock Glitching,FI1,AttackPrimitive
BR14,Secure Boot Bypass,FI1,BootSecurity
BR15,Signature Check Defeat,FI1|BR14,BootSecurity
GA4,Patched Firmware Loading,BR14|BR15,FirmwareAttack
GA5,Persistent Implant,GA4,FirmwareAttack
LAB4,ChipWhisperer,FI2|FI3,Lab
LAB5,JTAG Debugger,FI1,Lab
HHC7,Hardware Security Controls,,Defense
HHC8,Secure Boot Enforcement,HHC7|BR14,Defense
HHC9,Physical Tamper Detection,HHC7|FI1,Defense
```

## TAXONOMY
AttackPrimitive, BootSecurity, FirmwareAttack, Lab, Defense

## KEY PATHS
- Attack path: FI1 --[defeats]--> BR14 --[enables]--> GA4 (fault-inject the signature check, load patched image)
- Lab tool: LAB4 (ChipWhisperer) drives FI2/FI3
- Defense: HHC7 --[enforces]--> HHC8 --[blocks]--> BR14

## SOURCES
- NIST SP 800-193 (Platform Firmware Resiliency Guidelines)
- UEFI Secure Boot specification
- ChipWhisperer documentation (newae.com)
