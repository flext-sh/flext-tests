# Native payload contract

`m.Tests.Payload` owns a native value tree. Its `kind` distinguishes atoms,
lists, tuples, sets, frozensets, and mappings. Collection children are accessed
through `items`, mapping children through `entries`, and native leaves through
`atom`. Fields belonging to another arm must be empty.

The four fields are frozen, child sequences are tuples, and mapping entries are
owned read-only copies. Mutating an input mapping cannot change the validated
tree. Native model leaves deliberately retain their original identity and
mutability; freezing the tree does not freeze the application object it observes.
`None` is a valid atom, not a valid payload document. Unsupported leaves and
unknown fields fail validation.

Native bytes, temporal values, timezone objects, paths, classes, and model
instances are not JSON. Inspect `atom` directly to retain their meaning and
instance identity. A Pydantic dump is not a native-value round trip: it can
serialize nested model instances. JSON/file projection belongs to the explicit
output boundary, not to native matching or payload ownership.

The model recursively references itself; its reusable aliases remain finite.
The read-only payload protocol exposes meaningful fields rather than an empty
marker accepting arbitrary values.

Collection kind preserves source information. Matcher normalization remains a
separate behavior: tuple/list comparison and deterministic set ordering must
not change merely because the owned tree retains this information.

## Boundary changes

Native ingress rejects unsupported objects instead of silently converting them
to strings. Type and attribute matchers still inspect the original subject;
these checks do not require a serializable payload.

Mapping keys retain the established string normalization. Distinct source keys
that produce the same string now raise an error before a mapping is returned,
instead of overwriting an entry.

Bytes remain bytes inside the native tree and binary files. At the explicit
text/metadata projection, UTF-8 decoding is strict: invalid bytes raise instead
of being discarded. JSON serialization of an application model belongs to the
selected file output boundary, never to native ownership or comparison.

The shared `u.Cli.files_detect_format_from_content` owner recognizes a native
Pydantic model without serializing it. It applies the existing mapping-format
policy and explicit format override. Only the selected JSON/YAML file writer
invokes the model's JSON-mode dump; format detection must not perform a second,
premature export.
