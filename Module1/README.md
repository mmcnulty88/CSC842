# Module 1 - mmAutoBinEmbed

This script allows for the automatic usage of Peter Van Eeckhoutte's perl script pveReadBin.pl, that converts
a bin file into its byte form, and then inserts those bytes into a simple C file for usage and testing purposes.

## Requirements:

- Perl
- Python 2.7

## Usage:

```bash
python mmAutoBinEmbed.py [.bin file name]
```

Note: If the bin file is not in the same location as the script the full location can be provided instead.

## Future Work:

- Allow renaming of output file.
- Allow usage of any file to insert the converted bytes into (location will have to be specified).
