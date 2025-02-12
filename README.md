# py-mtr

`py-mtr` is a Python tool inspired by the `mtr` (My Traceroute) utility. It performs network trace operations to a specified destination using different protocols such as ICMP, UDP, TCP, and ESP.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Script Descriptions](#script-descriptions)
4. [Examples](#examples)
5. [License](#license)

## Installation

Before using `py-mtr`, make sure you have the required Python packages installed. You can use the `install_packages.py` script to automatically install the necessary packages:

    
    python install_packages.py
    

This script installs the following packages:
- `scapy`
- `tabulate`

## Usage

The main script `py-mtr.py` can be executed as follows:

    
    python py-mtr.py [destination] [options]
    

### Options
- `destination`: Target destination (IP address or hostname).
- `-p, --protocol`: Protocol to use for probes (ICMP, UDP, TCP, ESP). Default is `ICMP`.
- `--udp`: Use UDP protocol for probes.
- `--tcp`: Use TCP protocol for probes.
- `--icmp`: Use ICMP protocol for probes.
- `--esp`: Use ESP protocol for probes.
- `-d, --dns`: Perform DNS lookup.
- `-o, --output`: Output file for results.
- `--port`: Port to use for UDP/TCP probes.
- `--source`: Source IP address. Default is the system's default IP address.
- `-c, --probes`: Number of probes per hop. Default is 3.
- `--max_hops`: Maximum number of hops. Default is 10.

## Script Descriptions

### py-mtr.py

The `py-mtr.py` script performs the following operations:
1. Parses command-line arguments to specify the target destination, protocol, and other options.
2. Sets up logging for error messages.
3. Displays a message indicating the start of execution.
4. Validates the protocol and performs the network trace using the specified protocol.
5. Formats and prints the results, either to the console or to an output file if specified.

### install_packages.py

The `install_packages.py` script checks for and installs the required Python packages. It ensures that `scapy` and `tabulate` are installed before running the `py-mtr.py` script.

## Examples

Example usage of `py-mtr.py` to trace to a destination using ICMP protocol:

    
    python py-mtr.py example.com
    

Example usage of `py-mtr.py` to trace to a destination using UDP protocol and specify the port:

    
    python py-mtr.py example.com --udp --port 33434
    

## License

This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for details.
