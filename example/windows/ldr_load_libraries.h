#include <Windows.h>

typedef struct _UNICODE_STRING {//UNICODE_STRING structure
    USHORT Length;
    USHORT MaximumLength;
    PWSTR Buffer;
} UNICODE_STRING;
typedef UNICODE_STRING * PUNICODE_STRING;

NTSYSAPI NTSTATUS NTAPI LdrLoadDll(
  PWCHAR               PathToFile OPTIONAL,
  ULONG                Flags OPTIONAL,
  PUNICODE_STRING      ModuleFileName,
  PHANDLE              ModuleHandle);
