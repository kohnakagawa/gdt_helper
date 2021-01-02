# Gdt helper

Ghidra has "Parse C Source" feature to add new struct to "Data Type Manager." Using this feature, we can add new struct to "Data Type Manager" by writing C header file.

However, this is not easily performed as you expected. Without setting "Parse Configuration" propely, Ghidra cannot parse a relatively simple C header file. Although several "Parse Configurations" are provided by default, this does not work properly without changing include paths.

Gdt helper solves this problem. It makes "Parse Cofigurations" for your envorinment.

# How to use

See [example](./example).

# Supported

- Ubuntu 20.04
- macOS

# Special thanks

Inspired by https://github.com/0x6d696368/ghidra-data/blob/master/typeinfo/README.md.
