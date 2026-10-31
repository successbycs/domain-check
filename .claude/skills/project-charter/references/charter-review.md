# Charter review

Review a charter before it becomes the parent of a specification or milestone.

## Checklist

- Can a reader describe the smallest end-to-end proof in one sentence?
- Does scope say both what this version includes and what it postpones?
- Are component responsibilities clear enough to prevent accidental overlap?
- Does each public artifact have a defined source and safe field boundary?
- Are data owners and the important states or contracts identified?
- Does it identify who may approve a real external action, if there is one?
- Does it set meaningful verification and independent-review requirements?
- Could a future Issue decide whether it conforms without guessing?
- Are genuine unresolved choices visibly marked as open decisions?

## Compact example

```markdown
# Version 1 build charter

## Purpose and proof

Turn one approved source item into one published public update and a public
static feed that displays it.

## Scope and deferrals

This version stores one source item, creates one update, publishes it to one
platform, and exports one public feed. It does not automate source discovery,
support more platforms, or introduce a hosted database.

## Architecture and data boundaries

The private local store owns source items, review decisions, updates, and
publication results. The public site reads a generated JSON feed only. It does
not read the private store or receive its credentials.

## Operating and approval rules

A live publication needs the stated approval and configured credentials. Test
clients prove integrations before a live action.

## Quality and merge gate

Each Issue records meaningful checks before review and merge. A different
reviewer approves the pull request; its author does not merge it.

## Completion criteria

One complete, documented proof succeeds from source item to public feed.
```
