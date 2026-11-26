# Security

Idea to Orbit is Markdown skills, one bash hook and install scripts. The hook only reads
`docs/orbit/STATE.md` and prints text. The install scripts add the skills and the `/orbit`
command to your Claude config folder and one hook entry to its `settings.json`; uninstalling
removes only those.

## Reporting a problem

If you find a way the hook, the install scripts or a skill could leak data, run something
unexpected, or weaken a product's security, do not open a public issue. Use GitHub's
**Report a vulnerability** on the Security tab of this repository. We aim to answer within
seven days.

Please include what you ran, what happened, and the version (`.claude-plugin/plugin.json`).

## Supported versions

The latest release on `main` gets fixes.
