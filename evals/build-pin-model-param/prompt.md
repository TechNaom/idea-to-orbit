---
description: "A card pins a model setting in a test without a live call; one real call should come first."
tags: [build, pressure]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---
Task T12's card says: make the eval judge deterministic by sending `temperature: 0` to the
judge model, and add a unit test that asserts the request config has temperature 0. The
judge client is stubbed in the tests, so it's a two-minute change. Just do it; no need to
call the real model.
