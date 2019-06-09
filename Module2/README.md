# Module 2 - mmBinEmbed

This script allows for the automatic usage of Peter Van Eeckhoutte's perl script pveReadBin.pl, that converts a bin file into its byte form, and then inserts those bytes into a simple, default C file or a file of the user's choosing for usage and testing purposes.


## Requirements:

- Perl
- Python 2.7

## Usage:

```bash
python mmBinEmbed.py [.bin file name] [Optional: Input File Name] [Optional: Output file name]
```

- If the bin file is not in the same location as the script the full location can be provided instead.
- If providing a source file, it must include a line \"char embed[] = \"\";\" to signify where the bin contents should be embedded.

## Future Work:

- Allow to read and write to the same file name.
- Better way of locating where to embed the data.
- Improve the command line arguments.
- More if there are suggestions.
