---
name: luau-best-practices
description: "Luau best practices for Roblox. Use when reading or editing any .luau file, or .lua files in a Rojo project. Run it with /hstack:luau-best-practices in Claude Code or $hstack:luau-best-practices in Codex."
paths: ["**/*.luau"]
disable-model-invocation: true
metadata:
  short-description: Apply Luau best practices
---

# Luau best practices

Apply the **type-system-discipline** principle skill first. The repo's own rules win. Read its agent instruction file, `.luaurc`, `selene.toml`, and `.stylua.toml`, and match the nearest module's idiom before these defaults.

| Rule | Summary |
|------|---------|
| `--!strict` everywhere | Every file starts with `--!strict`, or `.luaurc` sets `"languageMode": "strict"`. Run the new type solver (`UseNewLuauTypeSolver = Enabled`, luau-lsp `enableNewSolver`). `--!nonstrict` only while migrating a legacy file, `--!nocheck` only for vendored or generated code. Fix the error, don't lower the mode. |
| Annotated signatures | Every function annotates its parameters and its return type. Annotate empty tables where they're declared (`local ids: { number } = {}`), so the first insert doesn't pick the type. |
| Composition root, not a scanning loader | One entry script per context (`init.server.luau`, `init.client.luau`) requires each module by a static path, builds it with its dependencies, and starts it in a set order. A comment names the reason wherever order matters. A typed `Deps` record carries the dependencies. A loader that scans folders by name returns `any` and erases every type. If you need a uniform `Init` then `Start` lifecycle, iterate an explicit list of requires. |
| Idempotent lifecycle | `Start` returns early when already started. The cleanup object it creates doubles as the started flag. `Init` work is synchronous. Anything that yields runs in `Start` under `task.spawn`. |
| No cyclic requires | Move shared types into a types-only module that ends `return nil`, or pass the dependency through the constructor. Never break a cycle with `require(x) :: any`. Require paths stay static (instance paths or require-by-string, whichever the repo uses). |
| Typed metatable classes | `X.__index = X`, a private `type Data`, then `export type X = typeof(setmetatable({} :: Data, X))`. `X.new` writes every field, nil ones included. Declare methods with `.` and an explicit `self: X`, and call them with `:`. Unannotated `function X:Y()` infers a useless `self`, and no fix is planned. A generic class (`Signal<T...>`) declares its interface type and casts once in `new`, with a comment saying why. |
| Composition over inheritance | No `__index` chains. Inherited methods fail to type ("Expected this to be exactly 'Base', but got 'Derived'") and defeat method caching. Pass collaborators in. Data with no identity and no methods stays a plain table plus module functions. |
| Tagged unions | Model variants with a singleton string discriminant (`Kind: "Playing"`). Refine with `==`. No booleans plus optional fields. Only strings and booleans can be singleton types. |
| Exhaustiveness | End every `if`/`elseif` chain over a union with `else return assertNever(x)`, where `assertNever(x: never): never` errors. A new variant then fails the type check. This needs the new solver. The old one reports a false positive on a complete chain. |
| String unions over magic strings | Enum-like values are singleton unions (`type RemoteName = "PickUp" \| "Drop"`). A frozen lookup keyed by the union doubles as the runtime validator. |
| `unknown` over `any` | External data is `unknown`: remote arguments, attributes, decoded JSON, values from `pcall`. Refine it before use. `any` appears only with a comment naming the solver or library limitation it works around. |
| No unchecked `::` casts | `::` is a compile-time claim with no runtime check. `inst :: BasePart` compiles even when it's wrong. Narrowing hierarchy: singleton `==` > `typeof`/`type` > `IsA` > `assert(...)` > `::`. Cast only after a check (`raw :: { [unknown]: unknown }` after `typeof(raw) == "table"`). |
| Branded ids | Brand primitives that must not mix: `type UserId = number & { __brand: "UserId" }`. The one cast lives in the parser or constructor. It's a convention, not a language feature. |
| Read-only and frozen | Hand out interfaces with `read` properties. `table.freeze` constants and configs, and freeze nested tables too, since the freeze is shallow. `table.freeze({...})` widens literals to `string`, so annotate the local first and freeze it as a statement. |
| Derived types | Reach for `typeof(template)`, `keyof<typeof(T)>`, `index<>`, and the module's existing `export type`s before declaring a new type. Use explicit instantiation (`f<<T>>()`) with a comment when inference widens. Write a `type function` only when the same mapping repeats. |
| Parse at the boundary | The server never trusts the client. A remote handler takes `unknown` arguments, rate-limits per player, parses into a named read-only type, then calls a typed method. Parsing checks `typeof` and `IsA`, `math.isfinite` (NaN and inf), string lengths, and `IsDescendantOf` for instances. The server re-checks game rules such as distance, price, and ownership. See the **boundary-discipline** principle skill. |
| One remote registry | One module names every remote, documents its payload, and exposes a typed getter. The server creates the folder and parents it last, and the client waits for it. Use an IDL compiler (Zap, Blink) when the repo has one. |
| Expected failures return | `assert` guards invariants and misuse, and returns its arguments (`local x = assert(maybe, "why")`). `error(msg, 2)` blames the caller. Expected failures return `(value?, reason?)` or a `Result` tagged union. Wrap every yielding `*Async` call in `pcall`. Protect a section whose failure would leave state stuck. `xpcall` with table errors needs a custom handler, because `debug.traceback` as the handler returns "error in error handling". |
| `task` library only | `task.spawn`, `task.defer`, `task.delay`, `task.wait`, `task.cancel`. Never `wait`, `spawn`, or `delay`. Say whether a function yields in its comment ("Yields.", "Must not yield."). Cancel only a suspended thread. Handle players already in the server after connecting `PlayerAdded`. |
| Every connection has an owner | A cleanup object (the repo's own, Trove, or Janitor) collects connections, threads, instances, and callbacks, and `Destroy` cleans them in reverse. Clear player-keyed tables on `PlayerRemoving`. Use `:Once()` for one-shot listeners. A `:Wait()` on a departed player's signal never returns, so its thread leaks. |
| Measured performance | Preallocate with `table.create(n)` and assign by index when the size is known. Build strings with `table.concat` or a `buffer`, never `..=` in a loop. Use generalized iteration (`for k, v in t`). Never `getfenv`, `setfenv`, or `loadstring`, which turn off the compiler's optimizations. Put `@native` only on measured hot numeric functions. Measure first, per the **benchmark-checklist** skill. |
| Place code by who may see it | Server-only code and secrets live under `ServerScriptService` and never replicate. Shared code lives in `ReplicatedStorage`, client code in the client container. A package stays self-contained, with no requires reaching outside it. |
| Repo style first | Match the repo's casing and layout. Absent one, follow the Roblox Lua style guide: PascalCase modules, classes, and types, camelCase locals and functions, `SCREAMING_SNAKE` constants, `_private` members. `game:GetService` at the top of the file. Early returns over nesting. `if a then b else c` over `a and b or c`. String interpolation over `..`. `if x then` only when `false` isn't a valid value of `x`. StyLua, selene (`std = "roblox"`), and `luau-lsp analyze` with a Rojo sourcemap run in CI. |
| Real tests | Keep domain logic free of engine calls and test it for real, in Lune or Jest Roblox. Run engine-touching code against real instances in Studio or Open Cloud Luau Execution. TestEZ is archived. Never mock through `setfenv`. |

Examples: `references/patterns.md`.
