# Onshape shortcuts

## Intent

Add voice commands for the documented Onshape keyboard shortcuts while editing
documents, without making those commands available on the Onshape home page or
other non-document routes.

## Implementation scope

- Add an app-specific Talon file under `my-config/apps/onshape/`.
- Match `browser.host: cad.onshape.com` and a browser path beginning with
  `/documents/`.
- Cover the general, Part Studio, Assembly, 3D View, Sketch, Feature Studio,
  and Drawing shortcuts from Onshape's keyboard-shortcuts documentation.

## Validation

- Run the Talon configuration gate.
- Confirm the context matches a `/documents/...` URL and not the Onshape home
  page.
- Test representative general, view, sketch, and drawing commands in Onshape.

## Rollback

Remove `my-config/apps/onshape/onshape.talon` and this plan file.
