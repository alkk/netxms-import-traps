# NetXMS template generator from traps defined in MIB file

Quick and dirty script which loads traps from MIB file and generate template for NetXMS.
Custom event is created for each trap.

## Requirements

[pysmi](https://github.com/etingof/pysmi), all referenced MIB files (e.g. SNMPv2-SMI, SNMPv2-TC)

## Usage

In the example bellow I assume that you have MIB file `myproduct.mib` in current directory and all related MIBs in the `/usr/share/snmp/mibs`.

```shell
# create new virtual environment
vf new -p python3.11 netxms-import-traps

# parse mib file myproduct.mib and save to intermediate JSON file ("PRODUCT.json", as defined in the MIB file, "… DEFINITIONS ::= BEGIN" line)
mibdump.py --mib-borrower= --mib-searcher= --mib-source='file:///usr/share/snmp/mibs' --mib-source='.' --generate-mib-texts  --destination-format json myproduct

# generate template from JSON file
./generate_template.py PRODUCT.json

# output is in PRODUCT.xml
```
