# tmps.py

tmps.py is a Python script that allows you to list, create, update, or delete files in the `/tmp/tmps/<env>` directory. It is designed to work with specific environments (dev, val, inf, fr) and supports various actions through command-line arguments.

## Features

- List files in a specified environment
- Create new files with specified mode and name
- Update existing files with new mode and name
- Delete files by primary key (name)

## Installation

To use tmps.py, you need to have Python installed on your system. You can download it from [python.org](https://www.python.org/).

## Usage

### Basic Syntax

```bash
tmps.py -e <env> -a <action> [-j <json>] [-k <pk>]
```

### Arguments

- `-e` or `--env`: Specifies the environment (dev, val, inf, fr). This is a mandatory argument.
- `-a` or `--action`: Specifies the action to perform (get, post, put, delete). This is a mandatory argument.
- `-j` or `--json`: Specifies the JSON content for creating or updating files. This is an optional argument.
- `-k` or `--pk`: Specifies the primary key (name of the file) for getting, updating, or deleting files. This is an optional argument.

### JSON File Format

The JSON file format for creating or updating files is as follows:

```json
{
  "env": "<env>",
  "mode": "0<nnn>",
  "name": "<name>"
}
```

- `<env>`: The environment (must correspond to the environment set with the `-e` option).
- `<nnn>`: The mode of the file, must respect regex `[2,6,7][1-7]{2}` (examples: 0644, 0755, 0632...).
- `<name>`: The name of the file (must respect regex `\w+`).

### Examples

1. **Create a new file:**

```bash
tmps.py -e dev -a post -j '{"env":"dev","mode": "0644","name": "Maurice"}'
```

This command creates a file named `Maurice` with mode `0644` for the `dev` environment. The file will be created at `/tmp/tmps/dev/Maurice`.

2. **List all files in an environment:**

```bash
tmps.py -e dev -a get
```

This command lists all files in the `/tmp/tmps/dev` directory.

3. **Update an existing file:**

```bash
tmps.py -e dev -a put -j '{"env":"dev","mode": "0755","name": "Maurice"}' -k Maurice
```

This command updates the file `Maurice` with mode `0755` for the `dev` environment.

4. **List a specific file:**

```bash
tmps.py -e dev -a get -k Maurice
```

This command lists the file `/tmp/tmps/dev/Maurice`.

5. **Delete a file:**

```bash
tmps.py -e dev -a delete -k Jean
```

This command deletes the file `Jean` from the `dev` environment.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Pascal

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Issues

If you encounter any issues or have questions, please open an issue on the GitHub repository.
