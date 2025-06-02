## Overview

This prototype demonstrates, how the SIREN modeling language can be transformed into specific cyber security monitoring rules. It takes an existing Prototype for creating Zeek based compliance monitoring, and expands it with the SIREN modeling language.
The SIREN modeling language was added in a two-fold way: 

(1) The BPMN-to-Zeek Parser was updated to be able to read the modeling language, which required complete rebuilding of the transformator. 
(2) We added a error detection module, which tests the XML input for the SIREN syntax, and prints the error code.

## Modules
TODO


## Results
The prototype shows how the modeling language can be integrated into existing BPMN based prototypes, and demonstrates a vision for modeling security-related attributes within business processes.
The resulting syntax-transformer can be used as an API to extract the relevant attributes from the BPMN and connect it to an arbitrary Python-based tool.
