# Firefox Bitwarden sidebar

## Intent

Open the Bitwarden Firefox extension sidebar by voice.

## Implementation scope

Add a Firefox-scoped personal Talon command, `sidebar bitwarden` (with
`panel bitwarden` as an alternative), which sends Bitwarden's `Shift+Alt+Y`
shortcut.

## Validation

Run the Talon configuration gate and check Talon's latest file-change reload
errors after saving the rule.

## Rollback

Remove `my-config/firefox_bitwarden.talon`.
