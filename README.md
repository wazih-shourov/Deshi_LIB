# deshilib 🇧🇩

**deshilib** হলো একটি বাংলা প্রোগ্রামিং ভাষা যা Python এ compile হয়।  
Write code in Bangla keywords — deshilib converts it to Python and runs it.

## Installation

```bash
pip install deshilib
````

## Usage

### As a Python module

```python
import deshilib

# সরাসরি Bangla code চালাও
deshilib.run_code("""
rakho x = 10
jodi x > 5 thole
    bol "baro"
nahole
    bol "choto"
""")

# ফাইল থেকে চালাও
deshilib.run_file("program.bd")

# Python code এ convert করো (run না করে)
py = deshilib.to_python("bol 5 + 3")
print(py)  # print(5 + 3)
```

### As a CLI tool

```bash
deshilib program.bd
```

## Bangla Keywords

| Bangla Keyword          | Python Equivalent | কাজ         |
| ----------------------- | ----------------- | ----------- |
| `rakho`                 | `=`               | ভ্যারিয়েবল |
| `bol`                   | `print()`         | প্রিন্ট     |
| `jodi ... thole`        | `if ...:`         | শর্ত        |
| `nahole jodi ... thole` | `elif ...:`       | নইলে যদি    |
| `nahole`                | `else:`           | নইলে        |
| `jotokhon ... thole`    | `while ...:`      | লুপ         |
| `dhori`                 | `def`             | ফাংশন       |
| `ferot de`              | `return`          | রিটার্ন     |

## Example Program

```
# grade.bd
rakho marks = 85

jodi marks >= 90 thole
    bol "A+"
nahole jodi marks >= 80 thole
    bol "A"
nahole jodi marks >= 70 thole
    bol "B"
nahole
    bol "C"
```

```bash
deshilib grade.bd
# Output: A
```

## License

MIT
