# Jubilant, the joyful library for integration-testing Juju charms

Jubilant is a Python library that wraps the [Juju](https://juju.is/) CLI for use in charm integration tests. It provides methods that map 1:1 to Juju CLI commands, but with a type-annotated, Pythonic interface.

**NOTE:** Jubilant is in very early stages of development. This is pre-alpha code. Our intention is to release a 1.0.0 version early to mid 2025.


## Design goals

- Familiar to users of the Juju CLI. We try to ensure methods, argument names, and response field names match the Juju CLI and its responses, with minor exceptions (such as "application" being shortened to "app" in `Status` fields).
- Simple API. Any cleverness in helpers and fixtures.
- TODO: versioning (Juju 3 and 4, maybe jubilant.compat for Juju 5 changes)
- TODO: no async/await


## To implement

- Go over TODOs in code and fix
- Add other commands (see below)
- Flesh out status types in _types.py
- Put up a docs site (presumably canonical-jubilant.readthedocs-hosted.com)

Other commands we think tests will use and should be implemented:

```
# add-secret                 Add a new secret. ### MAYBE???
# add-unit                   Adds one or more units to a deployed application.
# config                     Gets, sets, or resets configuration for a deployed
# exec                       Run the commands on the remote targets specified.
# integrate                  Integrate two applications.
# offer                      Offer application endpoints for use in other models.
# refresh                    Refresh an application's charm.
# remove-application         Remove applications from the model.
# remove-unit                Remove application units from the model.
# run                        Run an action on a specified unit.
# show-operation             Show results of an operation.
# ssh                        Initiates an SSH session on a Juju machine or container.
# trust                      Sets the trust status of a deployed application to true.
```
