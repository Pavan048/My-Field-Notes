| Feature | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Declare | `[1, 2, 2]` | `(1, 2, 2)` | `{1, 2}` | `{"a": 1}` |
| Constructor | `list()` | `tuple()` | `set()` | `dict()` |
| Ordered | Yes | Yes | No | Yes (insertion order) |
| Mutable | Yes | No | Yes | Yes |
| Duplicates | Yes | Yes | No | Keys: no; values: yes |
| Access | Index: `a[0]` | Index: `b[0]` | No indexing | Key: `d["a"]` |
| Membership lookup | O(n) | O(n) | O(1) average | O(1) average (keys) |
| Iterate | `for x in a:` | `for x in b:` | `for x in c:` | `for k, v in d.items():` |
| Update | `a.append(3)` | Not allowed (immutable) | `c.add(3)` | `d["b"] = 2` |
| Use | Ordered, editable items | Fixed collection | Unique items, fast membership | Key-value lookup |
| Example | `a = [1, 2]; a.append(3)` | `b = (10, 20)` | `c = set([1, 1, 2])` | `d = {"id": 1}; d["id"]` |

*Empty `{}` is a dictionary; use `set()` for an empty set. Set elements and dictionary keys must be hashable.*
