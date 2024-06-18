# Save Header

## Concept

The first line of a save file acts as an Header/Id for the save. This line is structured into several sections.

## Structure

The ID is divided as follows:

| Length | Field       | Description                                                                                  |
|--------|-------------|----------------------------------------------------------------------------------------------|
| 4      | `marker`    | A constant marker indicating it's a save file.                                               |
| 1      | `unknown`   | Can be either `0` or `1`. The purpose of this field is unknown.                               |
| 1      | `type`      | Specifies the compression type and binary format.                                             |
| 8      | `randomID`  | Random hexadecimal digits for unique identification.                                          |
| 8      | `metaLength`| Length of the metadata block in bytes, or the number of bytes to skip until game state data is read. |

### `type` Field Values

The `type` field indicates the compression type and data format:

| Value | Compression        | Format    |
|-------|--------------------|-----------|
| 5     | Split Compressed   | Binary    |
| 4     | Split Compressed   | Plaintext |
| 3     | Unified Compressed | Binary    |
| 2     | Unified Compressed | Plaintext |
| 1     | Uncompressed       | Binary    |
| 0     | Uncompressed       | Plaintext |

## Example

Consider the save ID: `SAV010341a5d1700000127`

Breaking it down:

- `SAV0` - Marker
- `1` - Unknown
- `0` - Type
- `341a5d17` - Random ID
- `00000127` - Metadata length
