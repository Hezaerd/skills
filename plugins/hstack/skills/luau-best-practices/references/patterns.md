# Luau patterns

Code examples for each rule in `SKILL.md`. The underlying principles are language-agnostic. See the **type-system-discipline** and **boundary-discipline** principle skills. Every example assumes `--!strict` and the new type solver.

## `--!strict` everywhere

```luau
--!strict
```

A root `.luaurc` makes strict the default, scripts without the header included:

```json
{ "languageMode": "strict" }
```

Turn on the new solver in every place (`Workspace.UseNewLuauTypeSolver = Enabled`, set in the Rojo project) and in luau-lsp (`"luau-lsp.fflags.enableNewSolver": true`). `read` properties, `never` exhaustiveness, `setmetatable<>`, and `keyof<>` only check under it.

## Annotated signatures

```luau
local function heal(humanoid: Humanoid, amount: number): number
	humanoid.Health = math.min(humanoid.Health + amount, humanoid.MaxHealth)
	return humanoid.Health
end

-- Don't. The first insert decides the element type.
local queue = {}

-- Do.
local queue: { Player } = {}
```

## Composition root, not a scanning loader

One entry script per context requires each module by a static path, builds it with its dependencies, and starts it in a set order.

```luau
--!strict
-- ServerScriptService/Server/init.server.luau
local InventoryService = require(script.Inventory.InventoryService)
local ShopService = require(script.Shop.ShopService)
local QuestService = require(script.Quest.QuestService)

local inventory = InventoryService.new()
local shop = ShopService.new(inventory)
local quests = QuestService.new({
	Inventory = inventory,
	Shop = shop,
})

inventory:Start()
shop:Start()
-- After the shop, which restores the purchase the first quest checks.
quests:Start()
```

The dependency record is a named type, so a missing or misspelled dependency fails the type check:

```luau
export type Deps = {
	Inventory: InventoryService.InventoryService,
	Shop: ShopService.ShopService,
}
```

A loader that scans folders by name hands back `any`:

```luau
-- Don't. Every module is any, so a renamed method fails at runtime, not in review.
local services = Loader.LoadDescendants(script.Services, Loader.MatchesName("Service$"))
Loader.SpawnAll(services, "OnStart")
```

When a uniform lifecycle is all you need, keep the list explicit so each `require` stays typed:

```luau
local modules = {
	require(script.DataService),
	require(script.CombatService),
}

for _, module in modules do
	module.Init()
end
for _, module in modules do
	task.spawn(module.Start)
end
```

## Idempotent lifecycle

```luau
function ShopService.Start(self: ShopService)
	if self._cleanup then
		return
	end
	local cleanup = Cleanup.new()
	self._cleanup = cleanup

	cleanup:Add(Remotes.Get("Buy").OnServerEvent:Connect(function(player: Player, raw: unknown)
		self:_OnBuy(player, raw)
	end))
end
```

## No cyclic requires

```luau
--!strict
-- Shared/ItemTypes.luau: types only, so anything can require it.
export type ItemId = string & { __brand: "ItemId" }
export type Item = { read Id: ItemId, read Price: number }
return nil
```

Two services that need each other's types require `ItemTypes`, not each other. A runtime dependency between them goes through a constructor argument.

## Typed metatable classes

```luau
--!strict
local Door = {}
Door.__index = Door

type Data = {
	Part: BasePart,
	IsOpen: boolean,
	_connection: RBXScriptConnection?,
}

export type Door = typeof(setmetatable({} :: Data, Door))

function Door.new(part: BasePart): Door
	local data: Data = {
		Part = part,
		IsOpen = false,
		_connection = nil,
	}
	return setmetatable(data, Door)
end

function Door.Open(self: Door)
	if self.IsOpen then
		return
	end
	self.IsOpen = true
	self.Part.CanCollide = false
end

function Door.Destroy(self: Door)
	if self._connection then
		self._connection:Disconnect()
		self._connection = nil
	end
end

return Door
```

Callers write `door:Open()`. Declaring the method as `function Door:Open()` instead leaves `self` inferred as a bag of `unknown` fields.

A constructor whose input may be wrong returns `X?` instead of throwing:

```luau
function Door.fromInstance(instance: Instance): Door?
	if not instance:IsA("BasePart") then
		warn(`Door must be a BasePart: {instance:GetFullName()}`)
		return nil
	end
	return Door.new(instance)
end
```

A closure built in the constructor that needs `self` declares it first:

```luau
function Door.new(part: BasePart): Door
	local self: Door
	local data: Data = {
		Part = part,
		IsOpen = false,
		_connection = part.Touched:Connect(function()
			self:Open()
		end),
	}
	self = setmetatable(data, Door)
	return self
end
```

`typeof(setmetatable(...))` can't carry a type pack, so a generic class declares its interface and casts once:

```luau
export type Connection = { Disconnect: (self: Connection) -> () }

export type Signal<T...> = {
	Connect: (self: Signal<T...>, callback: (T...) -> ()) -> Connection,
	Fire: (self: Signal<T...>, T...) -> (),
}

local Impl = {}
Impl.__index = Impl

-- ...Impl.Connect and Impl.Fire, typed `self: any`...

local function new<T...>(): Signal<T...>
	-- The interface above is the contract. typeof(setmetatable(...)) can't express T....
	return setmetatable({ _callbacks = {} }, Impl) :: any
end
```

## Composition over inheritance

```luau
-- Don't. Car's inherited methods fail to type, and every lookup walks the chain.
setmetatable(Car, { __index = Vehicle })

-- Do. The car owns an engine and delegates to it.
type Data = {
	Engine: Engine.Engine,
	Seats: number,
}

function Car.Start(self: Car)
	self.Engine:Start()
end
```

Data with no identity and no methods stays a plain table plus module functions:

```luau
export type Stats = { read Damage: number, read Speed: number }

local function scale(stats: Stats, factor: number): Stats
	return { Damage = stats.Damage * factor, Speed = stats.Speed * factor }
end
```

## Tagged unions

```luau
-- Don't. Booleans and optionals let contradictory states exist.
type Round = { Active: boolean, Winner: Player?, EndsAt: number? }

-- Do. Only valid states exist.
export type Round =
	{ Kind: "Waiting" }
	| { Kind: "Playing", EndsAt: number }
	| { Kind: "Over", Winner: Player }
```

## Exhaustiveness

```luau
local function assertNever(value: never): never
	error(`Unhandled variant: {value}`)
end

local function describe(round: Round): string
	if round.Kind == "Waiting" then
		return "Waiting for players"
	elseif round.Kind == "Playing" then
		return `Ends in {math.ceil(round.EndsAt - os.clock())}s`
	elseif round.Kind == "Over" then
		return `{round.Winner.DisplayName} won`
	else
		return assertNever(round)
	end
end
```

Add `{ Kind: "Paused" }` to `Round` and the `assertNever(round)` line fails to type check until `describe` handles it.

## String unions over magic strings

```luau
export type Speed = "Slow" | "Normal" | "Fast"

local WALK_SPEEDS: { [Speed]: number } = {
	Slow = 8,
	Normal = 16,
	Fast = 24,
}
table.freeze(WALK_SPEEDS)

local function parseSpeed(raw: unknown): Speed?
	if raw == "Slow" or raw == "Normal" or raw == "Fast" then
		return raw
	end
	return nil
end
```

## `unknown` over `any`

```luau
local health: unknown = model:GetAttribute("Health")
if typeof(health) == "number" then
	bar.Size = UDim2.fromScale(health / 100, 1)
end
```

An `any` that stays carries its reason:

```luau
-- Untyped on purpose: under the new solver, createElement can't infer a function component's props.
local e = React.createElement :: any
```

## No unchecked `::` casts

```luau
-- Don't. Compiles, and nothing checks it at runtime.
local root = character:FindFirstChild("HumanoidRootPart") :: BasePart

-- Do. IsA checks at runtime and refines the type.
local root = character:FindFirstChild("HumanoidRootPart")
if root and root:IsA("BasePart") then
	root.Anchored = true
end

-- Or fail loud when absence is a bug.
local spawnPart = assert(workspace:FindFirstChildWhichIsA("SpawnLocation"), "The map has no SpawnLocation")
```

A table from outside has to be cast before it can be indexed. Cast after the check, never instead of it:

```luau
if typeof(raw) ~= "table" then
	return nil
end
local fields = raw :: { [unknown]: unknown }
```

## Branded ids

```luau
export type UserId = number & { __brand: "UserId" }

local function userIdOf(player: Player): UserId
	-- The only place a number becomes a UserId.
	return player.UserId :: any
end

local function grantBadge(userId: UserId, badgeId: number) end

grantBadge(userIdOf(player), 1234) -- Ok
grantBadge(1234, userIdOf(player)) -- Type error
```

## Read-only and frozen

```luau
export type Point = { read X: number, read Y: number }

local REWARDS = table.freeze({
	Win = 100,
	Loss = 25,
	Streak = table.freeze({ 10, 20, 40 }), -- The freeze is shallow.
})
```

`table.freeze({...})` types its fields as plain `string`. Annotate the local, then freeze it as a statement:

```luau
type Mode = "FreeForAll" | "Teams"

local SETTINGS: { Mode: Mode, Rounds: number } = {
	Mode = "Teams",
	Rounds = 3,
}
table.freeze(SETTINGS)
```

## Derived types

```luau
local TEMPLATE = {
	Coins = 0,
	Level = 1,
	Owned = {} :: { string },
}
export type SaveData = typeof(TEMPLATE)

local ITEMS = {
	Sword = { Price = 100 },
	Shield = { Price = 50 },
}
export type ItemName = keyof<typeof(ITEMS)> -- "Shield" | "Sword"
```

Explicit instantiation, with its reason:

```luau
-- Explicit type argument: inferred from nil, the phase would widen to nil.
local phase = Charm.atom<<Phase?>>(nil)
```

A `type function` only when the same mapping repeats:

```luau
type function Partial(ty)
	assert(ty:is("table"))
	local out = types.newtable()
	for key, prop in ty:properties() do
		out:setproperty(key, types.optional(prop.read))
	end
	return out
end

type SettingsPatch = Partial<Settings>
```

## Parse at the boundary

```luau
export type BuyRequest = { read ItemId: string, read Quantity: number }

local function parseBuyRequest(raw: unknown): (BuyRequest?, string?)
	if typeof(raw) ~= "table" then
		return nil, "expected a table"
	end
	local fields = raw :: { [unknown]: unknown }
	local itemId, quantity = fields.ItemId, fields.Quantity
	if typeof(itemId) ~= "string" or #itemId > 64 then
		return nil, "bad ItemId"
	end
	if typeof(quantity) ~= "number" or not math.isfinite(quantity) or quantity < 1 or quantity % 1 ~= 0 then
		return nil, "bad Quantity"
	end
	return { ItemId = itemId, Quantity = quantity }, nil
end

Remotes.Get("Buy").OnServerEvent:Connect(function(player: Player, raw: unknown)
	if not cooldown:Try(player) then
		return
	end
	local request = parseBuyRequest(raw)
	if not request then
		return
	end
	shop:Buy(player, request) -- Buy re-checks the price and the player's balance.
end)
```

An instance from the client can be a table posing as one, or an instance outside the allowed folder:

```luau
if typeof(target) == "Instance" and target:IsA("Model") and target:IsDescendantOf(itemsFolder) then
	carry:TryPickUp(player, target)
end
```

## One remote registry

```luau
--!strict
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

export type RemoteName =
	-- (itemId) to the server, for an item the player can afford.
	"Buy"
	-- (model) to the server, for an item within reach.
	| "PickUp"

local NAMES: { RemoteName } = { "Buy", "PickUp" }

local folder: Folder
if RunService:IsServer() then
	folder = Instance.new("Folder")
	folder.Name = "Remotes"
	for _, name in NAMES do
		local remote = Instance.new("RemoteEvent")
		remote.Name = name
		remote.Parent = folder
	end
	-- Parent last, so clients receive the folder with every remote in it.
	folder.Parent = ReplicatedStorage
else
	folder = ReplicatedStorage:WaitForChild("Remotes") :: Folder
end

local Remotes = {}

function Remotes.Get(name: RemoteName): RemoteEvent
	return folder:WaitForChild(name) :: RemoteEvent
end

return table.freeze(Remotes)
```

The two casts are safe because this module creates both instances.

## Expected failures return

```luau
export type Result<T, E> = { Ok: true, Value: T } | { Ok: false, Error: E }

-- Yields. The caller parses the value: an old save may not match today's shape.
local function loadSave(store: DataStore, key: string): (unknown, string?)
	local ok, result = pcall(function(): unknown
		return store:GetAsync(key)
	end)
	if not ok then
		warn(`Couldn't load {key}: {result}`)
		return nil, "load failed"
	end
	return result, nil
end
```

`assert` returns its arguments, so it refines and assigns in one step:

```luau
local lobby = assert(workspace:FindFirstChild("Lobby"), "The map has no Lobby")
```

Protect the section whose failure would leave state stuck:

```luau
-- Protected: an error here would skip the reset and leave the round stuck in Over.
local ok, err = pcall(awardWinners, round)
if not ok then
	warn(`Couldn't award the winners: {err}`)
end
resetRound()
```

`debug.traceback` as the handler fails on a table error, so give `xpcall` its own:

```luau
local ok = xpcall(run, function(err: unknown)
	warn(err, debug.traceback(nil, 2))
end)
```

## `task` library only

```luau
Players.PlayerAdded:Connect(onPlayerAdded)
-- Players who joined before this connection ran.
for _, player in Players:GetPlayers() do
	task.spawn(onPlayerAdded, player)
end

local despawn = task.delay(30, item.Destroy, item)

-- Only a suspended thread can be cancelled. A running one ends when it returns.
if coroutine.status(despawn) == "suspended" then
	task.cancel(despawn)
end
```

## Every connection has an owner

```luau
function CombatService.Start(self: CombatService)
	if self._cleanup then
		return
	end
	local cleanup = Cleanup.new()
	self._cleanup = cleanup

	cleanup:Add(Players.PlayerRemoving:Connect(function(player: Player)
		self._lastHit[player] = nil
	end))
	cleanup:Add(task.delay(ROUND_LENGTH, function()
		self:_EndRound()
	end))
end

function CombatService.Destroy(self: CombatService)
	if self._cleanup then
		self._cleanup:Clean()
		self._cleanup = nil
	end
end
```

```luau
-- Don't. If the player has already left, this never returns and the thread leaks.
player.CharacterAdded:Wait()
```

## Measured performance

```luau
-- Size known: preallocate and assign by index.
local positions = table.create(#parts)
for i, part in parts do
	positions[i] = part.Position
end

-- Strings: collect, then join once.
local lines = table.create(#entries)
for i, entry in entries do
	lines[i] = `{entry.Name}: {entry.Score}`
end
local board = table.concat(lines, "\n")

-- Native code on a measured hot, numeric function only.
@native
local function lerp(a: number, b: number, t: number): number
	return a + (b - a) * t
end
```

## Place code by who may see it

```
ServerScriptService/Server/    server only, never replicated: services, validation, secrets
ReplicatedStorage/Shared/      both sides: types, configs, sanitizers, pure logic
ReplicatedStorage/Client/      client only: controllers, UI
ReplicatedStorage/Packages/    self-contained packages, no requires outside themselves
```

## Repo style first

File order, absent a repo convention:

```luau
--!strict
-- What this module owns, in one line, when the name doesn't say it.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Packages = ReplicatedStorage.Packages
local Charm = require(Packages.Charm)

local Shared = ReplicatedStorage.Shared
local Remotes = require(Shared.Net.Remotes)

local MAX_HOLD_DISTANCE = 12
```

Truthiness only where `false` can't be a real value:

```luau
local part: BasePart? = workspace:FindFirstChildWhichIsA("BasePart")
if part then
	part.Anchored = true
end

local muted: boolean? = settings.Muted
if muted ~= nil then -- false is a real choice here
	applyMute(muted)
end
```

## Real tests

Keep the logic pure so it runs anywhere:

```luau
-- Shared/Scoring.luau has no engine calls, so Lune and Jest Roblox can run it as-is.
local Scoring = require("./Scoring")

assert(Scoring.Combo({ 1, 1, 1 }) == 3, "three hits in a row make a 3x combo")
```

Engine-touching code runs against real instances in Studio or through Open Cloud Luau Execution, not against hand-built fakes.
