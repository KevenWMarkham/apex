# apex-cxml

APEX **CXML** (Customer Experience Markup Language) canonical entities for the RC Practice.

Entities: Customer · Loyalty · Interaction · Order.

**Heavy PII surface.** Every PII attribute uses the `_token` suffix convention and is classified `Classification.PII`. The `tokenizer_hooks` module enumerates tokenised columns so the `tokenizer-mcp` Silver-transform step knows what to tokenise.
