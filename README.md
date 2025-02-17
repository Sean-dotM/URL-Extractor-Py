# URL-Extractor-Py
A simple URL and domain extractor written using python and regular expressions (gibberish for the uninitiated). I may come back to this in the future to expand on functionality and usability, but this is currently not a priority for me.

## Usage
Using the script is pretty straight forward; the script only takes two arguments - an input file, and the name of the desired output file. Please refer to the syntax below:
```
UDExtract.py [INPUT_FILE] [OUTPUT_FILE]
---------------------------------------
[INPUT_FILE] -> The file you want to parse
[OUTPUT_FILE] -> The file you want to store the results in
```
`TLDs.txt` as the name implies, is a plaintext list (with a single entry per line) of TLDs that the script will try to extract.
The file included with this repository is a modified version of IANA's TLD list which you can find [here](https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
The changes made are as follows:
- Removed first line which denotes version info, etc..
- Removed IDNs (Punycode TLDs) as these are not supported by the regex anyways

If you wish you to extract domains matching only a certain TLD, please modify this file.

## Regex
URL regex:
> [!NOTE]
> This regex is a Python adaptation of the CyberChef `Exract URLs` recipe, you can refer to the source [here](https://github.com/gchq/CyberChef/blob/master/src/core/lib/Extract.mjs)
```
protocol = r"[A-Z]+://"
hostname = r"[-\w]+(?:\.\w[-\w]*)+"
port = r":\d+"
path = r"/[^.!,?\"<>\[\]{}\s\x7F-\xFF]*" + \
       r"(?:[.!,?]+[^.!,?\"<>\[\]{}\s\x7F-\xFF]+)*"
url = re.compile(protocol + hostname + "(?:" + port + ")?" + "(?:" + path + ")?", re.IGNORECASE)
```
Domain regex: `\b((?:(?:[a-zA-Z0-9_](?:[a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})|localhost)\b`

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
