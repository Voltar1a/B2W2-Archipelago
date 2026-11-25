# Setup guide

## Requirements
- Archipelago `0.6.7` or newer (with `pokemon_b2w2.apworld` installed).
- BizHawk (Windows or Linux).
  - If using BizHawk 2.10 or lower, disable AutoSaveRam (`Config > Customize... > Advanced`) so save data persists properly.
- A clean USA/Europe `.nds` ROM of Pokémon Black Version 2 or Pokémon White Version 2.

## Patch and launch
1. Open your patch file.
2. Select your matching base `.nds` ROM when prompted if not done before. Archipelago will generate your patched `.nds` ROM and launch BizHawk + the BizHawk Client.

## Connect to Multiworld
1. In BizHawk, open Tools > Lua Console and load `data/lua/connector_bizhawk_generic.lua` from your Archipelago installation folder.
2. In the BizHawk Client, enter `<address>:<port>`, click Connect, and enter your slot name (and password if set).
