# Example

This directory contains some examples of creating data types and function definitions using gdt helper.
You might also need to edit output header files to parse properly, but in that case this script tries to warn you.

[linux](./linux) contains an example to create data types and function definitions of OpenSSL.

```
$ python gdt_helper.py make-parse-options gcc # paste it to "Parse Options"
$ python gdt_helper.py make-file-to-parse gcc ./example/linux/open_ssl.h # specify open_ssl.h.out to "Source files to parse"
```

[osx](./osx) contains an example to create data types and function definitions for macOS system headers.

```
$ python gdt_helper.py make-parse-options clang # paste it to "Parse Options"
# NOTE: system header file path may differ on your environment
$ python gdt_helper.py make-file-to-parse clang ./example/osx/mac_system.h --additional-includes /Library/Developer/CommandLineTools/SDKs/MacOSX10.16.sdk/usr/include
```

[windows](./windows) contains an example to create data types and function definitions for Windows system headers.

```
$ python gdt_helper.py make-parse-options x86_64-w64-mingw32-gcc
$ python gdt_helper.py make-file-to-parse x86_64-w64-mingw32-gcc ./example/ldr_load_libraries.h
```
