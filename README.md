## Overview

This prototype demonstrates, how the SIREN modeling language can be transformed into specific cyber security monitoring rules. It takes an existing Prototype for creating Zeek based compliance monitoring, and expands it with the SIREN modeling language.
The SIREN modeling language was added in a two-fold way: 

(1) The BPMN-to-Zeek Parser was updated to be able to read the modeling language, which required complete rebuilding of the transformator. 
(2) We added a error detection module, which tests the XML input for the SIREN syntax, and prints the error code.

## Modules
### gather_information.py
extracting the BPMN-Information out of the XML-tree, and saving it into the python environment. This is based on the SIREN modeling language.

### create_zeek_input.py
This module creates a tsv input, based on the previously gathered information. This output can then be used as an input for the Zeek Prototype found here: https://github.com/TODO

### verify_requirements.py
This module checks the information extracted out of the XML and checks if they are in comformity with the SIREN modeling language.


## Results
The prototype shows how the modeling language can be integrated into existing BPMN based prototypes, and demonstrates a vision for modeling security-related attributes within business processes.
The resulting syntax-transformer can be used as an API to extract the relevant attributes from the BPMN and connect it to an arbitrary Python-based tool.

## Demonstration (Usage of the SIREN modeler with the existing Prototype)

