import sys
import re

def loadTlds(file):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            tlds = file.read().splitlines()
        return set(tld.strip().lower() for tld in tlds if tld.strip())
    except Exception as e:
        print(f"Error reading TLD file: {e}")
        exit(1)

# URL regex adapted from https://github.com/gchq/CyberChef/blob/master/src/core/lib/Extract.mjs as this works pretty well
def extrUrls(line):
    protocol = r"[A-Z]+://"
    hostname = r"[-\w]+(?:\.\w[-\w]*)+"
    port = r":\d+"
    path = r"/[^.!,?\"<>\[\]{}\s\x7F-\xFF]*" + \
           r"(?:[.!,?]+[^.!,?\"<>\[\]{}\s\x7F-\xFF]+)*"
    url = re.compile(protocol + hostname + "(?:" + port + ")?" + "(?:" + path + ")?", re.IGNORECASE)
    return url.findall(line)

# Find all potential domains, then verify the TLD
def extrDomains(line, validTlds):
    domain = re.compile(r'\b((?:(?:[a-zA-Z0-9_](?:[a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,13})|localhost)\b')
    domains = domain.findall(line)
    validDomains = []
    for domain in domains:
        tld = domain.split('.')[-1]
        if tld in validTlds:
            validDomains.append(domain)
    return validDomains

def main(argv):

    # No args provided print syntax, then exit
    if len(argv)!=3:
        print("UDExtract.py [INPUT_FILE] [OUTPUT_FILE]")
        print("---------------------------------------")
        print("[INPUT_FILE] -> The file you want to parse")
        print("[OUTPUT_FILE] -> The file you want to store the results in")
        print("\nA list of valid TLDs can be found here -> https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
        exit(1)

    inFile = argv[1]
    outFile = argv[2]
    validTlds = loadTlds('TLDs.txt')   
    urls = set();
    domains = set();

    # Read inFile, check each line for matches
    try:
        print(f"Attempting to parse <- {inFile}")
        with open(inFile, 'r', encoding='utf-8', errors='ignore') as file:
            print("Checking for matches")
            for line in file:
                lineUrls = extrUrls(line)
                lineDomains = extrDomains(line, validTlds)
                urls.update(lineUrls)
                domains.update(lineDomains)
    except Exception as e:
        print(f"Error parsing file '{inFile}': {e}")
    
    # Write to outFile
    try:
        print(f"Writing output -> {outFile}")
        with open(outFile, 'w', encoding='utf-8') as file:
            file.write("---- URLs ----\n")
            for url in urls:
                file.write(url + '\n')
            
            file.write("\n---- Domains ----\n")
            for domain in domains:
                file.write(domain + '\n')
    except Exception as e:
        print(f"Error writing to file '{outFile}': {e}")
        exit(1)
    
    print("Done!")

if __name__ == "__main__":
    main(sys.argv)
