## Overview

This prototype demonstrates, how the SIREN modeling language can be transformed into specific cyber security monitoring rules. It takes an existing Prototype for creating Zeek based compliance monitoring, and expands it with the SIREN modeling language.
The SIREN modeling language was added in a two-fold way: 

(1) The BPMN-to-Zeek Parser was updated to be able to read the modeling language, which required complete rebuilding of the transformator. 
(2) We added a error detection module, which tests the XML input for the SIREN syntax, and prints the error code.

## Modules
### gather_information.py
extracting the BPMN-Information out of the XML-tree, and saving it into the python environment. This is based on the SIREN modeling language.

### create_zeek_input.py
This module creates a tsv input, based on the previously gathered information. This output can then be used as an input for the Zeek Prototype found here: https://github.com/Blinded

### verify_requirements.py
This module checks the information extracted out of the XML and checks if they are in comformity with the SIREN modeling language.


## Results
The prototype shows how the modeling language can be integrated into existing BPMN based prototypes, and demonstrates a vision for modeling security-related attributes within business processes.
The resulting syntax-transformer can be used as an API to extract the relevant attributes from the BPMN and connect it to an arbitrary Python-based tool.

## Demonstration (Usage of the SIREN modeler with the existing Prototype)

### 1. Example Use Case in Camunda
![image](https://github.com/user-attachments/assets/63216242-bcb1-4adc-81cd-6c5139035bed)
Note: See the requirements modelled as Camunda-Annotations, as defined by the Siren.exe modelling language

### 2. Select Input (xml, or bpmn file (Export from Camunda)
![image](https://github.com/user-attachments/assets/b8d192c4-616d-4344-a655-299774e4b3d6)

### 3. Create Input for the Zeek Prototype (see Zeek-Monitor Github)
The language checks the input, if it matches the modelling language. 
In the Use Case there is only one communication (Pool 1 to Pool 2) using the MQTT Protocol. 
It checks for Siren conformity, then creates the .tsv input for the Zeek-Monitor (Related Work).

https://github.com/mahopy/siren.exe/blob/main/Use%20Case/zeek_input_use_case.tsv


### 4. SIREN conformity checking
![image](https://github.com/user-attachments/assets/0d913a0d-4c66-4549-aff4-90243b8d0861)

