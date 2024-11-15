#   Copyright IBM Corporation 2021
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
from parseio import parseIO
ManifestFile = "manifest.yml"
LogTag = "<DETECT SCRIPT>"

# Performs the detection of pom file and extracts service name
def detect(inputPath):
    print(LogTag + ' Input file of transformer: ' + inputPath)
    with open(inputPath) as f:
        data = f.read()
        detectInput = json.loads(data)
        print(LogTag + ' Input data: ' + str(detectInput))
        services = {}
        for rootDir, _, fileList in os.walk(detectInput["InputDirectory"]):
                for fileName in fileList:
                    if fileName != ManifestFile:
                        continue
                    fullFilePath = os.path.join(rootDir, fileName)
                    print(LogTag + ' Manifest File Found Here: ' + str(fullFilePath))
                    with open(fullFilePath, 'r') as f:
                        doc = yaml.safe_load(f)

                    serviceName = doc["applications"][0]["name"]
                    print(LogTag + ' Service Name from Manifest File : ' + str(serviceName))
                    services[serviceName] = [{
                        "paths": {"ServiceDirectories": [rootDir]} }]

                    #pomTree = ET.parse(fullFilePath)
                    #pomRoot = pomTree.getroot()
                    #for a in pomRoot:
                    #    if 'artifactId' in a.tag:
                    #        services[a.text] = [{
                    #        "paths": {"ServiceDirectories": [rootDir]} }]
                    #        break
    return services

# Entry-point of detect script
def main():
    ioEnvNames = ['M2K_DETECT_INPUT_PATH', 'M2K_DETECT_OUTPUT_PATH']
    inputPath, outputPath = parseIO(ioEnvNames, LogTag)
    services = detect(inputPath)
    outDir = os.path.dirname(outputPath)
    if os.path.exists(outDir) == False:
        os.makedirs(outDir, exist_ok=True)
    with open(outputPath, "w+") as f:
        json.dump(services, f)

if __name__ == '__main__':
    main()