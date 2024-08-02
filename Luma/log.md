
### ```A1``` >> a completely ready-made tokenizer has been written.
---
### ```A2``` >> the core of the language is almost formed.
---
### ```A3``` >> a fully working parser is ready.
---
### ```A4``` >> added support for importing Python self-written modules (but only functions can be imported).

Here is an example of a function translated from python to Luma
```python
import sys
sys.path.extend('../')
import math

from src.core import luma_functions
from src.core import luma_values
from src.core import luma_types

fs = luma_functions.LumaFunctionsSaver()

@luma_functions.LumaFun(fs, 'sin', True, types=[[luma_types.LumaTypes.get('Float'), luma_types.LumaTypes.get('Int')]])
def _(arg: luma_values.ValueConstruct):
    return luma_values.FloatValue.Create(
        math.sin(arg.value.value)
    )
```
and this is how this file is imported.
```cs
using "libs/math" (py);

let a = math.sin(180);
```
```(py)``` at the end means that when downloading this file, the standard python module loader will be used

---

### ```A5``` added the ability to create mutable and non-mutable variables using the keyword ```mut```.
```cs
let a = 10;             // Not mutable
let mut name = "John";  // Mutable
```

---

### ```A6``` it is also possible to leave single-line and multi-line comments on the code.
```cs
let dummy = 3.1415 * 2 * "NOOOOO"; // This is error code and this one line comment!


using 'libs/stdlib' (py);

/*
    This is multi-line comment!
    And this code is secces!
*/
stdlib.print("Hello World!");
```

---

### ```A7``` it is also possible create lambda functions.
```cs
using 'libs/stdlib' (py);

let mul = lambda(a, b) {
    |> a * b
};

stdlib.print(mul(2, 3)); // this code printed 6!
```

### ```A8``` added simple for loops.
```cs
using 'libs/stdlib' (py);

for (let i; i <= 10; i = i + 1;) {
    stdlib.println(i, );
};
// this code print 0  1  2  3  4  5  6  7  8  9  10
```
