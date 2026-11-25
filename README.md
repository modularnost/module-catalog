# Modularnost module catalog

A curated catalog of modules for the [Modularnost](https://github.com/modularnost/panel)
Docker Swarm panel. [`catalog.json`](catalog.json) uses schema version 1 and
lists one approved version per installable module.

| Module | What it does | Permissions | Installation |
| --- | --- | --- | --- |
| [Builder](https://github.com/modularnost/builder_module) | Builds and deploys applications from Git repositories | `service:read`, `service:create` | [Catalog setup](https://github.com/modularnost/panel/blob/main/docs/catalog.md#install-builder-from-the-catalog) |
| [Metrics](https://github.com/modularnost/metrics_module) | Stores historical CPU, memory, network, and disk I/O for Swarm services | `stats:read` | [Installation guide](https://github.com/modularnost/metrics_module#install) |

Catalog-based installation requires panel integration. To install Metrics now,
follow its guide and use the image digest from `catalog.json` in the command.

The Metrics entry pins a public multi-platform image built from the contract 3
source. The image reports version `0.4.0` in its manifest. The catalog pins its
digest because this build was published through the rolling `edge` channel.

## Catalog format

The [JSON Schema](catalog.schema.json) defines the required fields and allowed
values. Keep a module's ID stable and match its Swarm module name.
`requires.contract` is the module protocol version. An optional
`requires.min_panel_version` records a minimum panel version.

- `swarm_service` supplies a version and a digest-pinned public image. The
  internal port defaults to `8080`. When a data volume is declared, the panel
  installer should attach a named volume at `mount_path` on the selected node
  and keep the service pinned there so redeployments preserve the data.
- `manual` supplies a public installation guide for a module with additional
  setup or dependencies.
- `swarm_stack` supplies a version and a digest-pinned public module image
  that contains a deployment bundle. The same format can be used by any module.

### Deployment bundle

An image for `swarm_stack` contains `/usr/share/modularnost/deploy/manifest.json`:

```json
{
  "schema_version": 1,
  "stack_files": ["stack.yml", "stack.dependencies.yml"],
  "registry_credentials": true
}
```

`stack_files` lists one or more Compose files in merge order. Paths are relative
to the deployment directory. Additional assets live in that same directory.
Use regular files and paths whose segments begin with a letter or digit and
contain only letters, digits, periods, underscores, and hyphens. Keep the
bundle to 64 files, 256 KiB per file, and a 1 MiB tar archive.

Set `registry_credentials` when the stack requires the panel to manage
encrypted registry credentials. The default is `false`. The panel can read
and check the bundle during preflight without starting the module. Publish
stack entries when the panel supports deploying them.

## Submit a module

Open a PR updating `catalog.json`. Link to the public source and provide a
publicly pullable image digest for `swarm_service` and `swarm_stack`. Check that the
version, contract, and permissions match the image's `/manifest`. Include any
required storage or manual setup. Optional screenshots belong in
`screenshots/<id>/` and each needs descriptive alt text.

Run the same validation as CI:

```sh
python -m pip install jsonschema==4.26.0
python validate.py
```
