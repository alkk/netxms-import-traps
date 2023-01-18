#!/usr/bin/env python3

import json
import re
import sys
import uuid
import xml.etree.cElementTree as ET

if len(sys.argv) != 2:
    print('Usage: gen.py <input_file.json>')
    exit(1)

input_file = sys.argv[1]
if input_file.endswith('.json'):
    input_file = input_file[:-5]
    output_file = input_file + '.xml'
else:
    print('Input file must be a JSON file')
    exit(1)

with open(sys.argv[1]) as f:
    data = json.load(f)
trap_definitions = [obj for obj in data.values() if 'class' in obj and obj['class'] == 'notificationtype']

INITIAL_EVENT_ID = 90000

template_root = ET.Element('configuration')
ET.SubElement(template_root, 'formatVersion').text = '4'
events = ET.SubElement(template_root, 'events')

event_idx = 1
for trap_definition in trap_definitions:
    event = ET.SubElement(events, 'event', id=str(event_idx))
    ET.SubElement(event, 'guid').text = str(uuid.uuid4())
    name = re.sub(r'(?<=[a-z])[A-Z]', r'_\g<0>', trap_definition['name'])
    ET.SubElement(event, 'name').text = name.upper()
    ET.SubElement(event, 'code').text = str(INITIAL_EVENT_ID + event_idx)
    ET.SubElement(event, 'severity').text = '0'
    ET.SubElement(event, 'flags').text = '1'
    description = trap_definition['description']
    ET.SubElement(event, 'message').text = description
    ET.SubElement(event, 'tags').text = ''
    if 'objects' in trap_definition:
        description += "\nParameters:\n"
        idx = 2
        for obj in trap_definition['objects']:
            description += f"\n%{idx} - {data[obj['object']]['description']}"
            idx += 1
    ET.SubElement(event, 'description').text = description

    event_idx += 1

traps = ET.SubElement(template_root, 'traps')
trap_idx = 1
for trap_definition in trap_definitions:
    trap = ET.SubElement(traps, 'trap', id=str(trap_idx))
    ET.SubElement(trap, 'guid').text = str(uuid.uuid4())

    event_name = re.sub(r'(?<=[a-z])[A-Z]', r'_\g<0>', trap_definition['name'])
    ET.SubElement(trap, 'event').text = event_name.upper()

    ET.SubElement(trap, 'oid').text = trap_definition['oid']
    ET.SubElement(trap, 'description').text = trap_definition['description']
    if 'objects' in trap_definition:
        parameters = ET.SubElement(trap, 'parameters')
        parameter_idx = 1
        for obj in trap_definition['objects']:
            parameter = ET.SubElement(parameters, 'parameter', id=str(parameter_idx))
            ET.SubElement(parameter, 'flags').text = '0'
            ET.SubElement(parameter, 'description').text = data[obj['object']]['name']
            ET.SubElement(parameter, 'oid').text = data[obj['object']]['oid']
            parameter_idx += 1
    trap_idx += 1

ET.ElementTree(template_root).write(output_file)
