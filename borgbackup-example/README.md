
What is borgbackup and why are we caring about it?

DIY point in time snapshots to a local filesystem

block deduplicated storage

say you have some local filesystem storage that you care about:
- maybe your cool webapp uses sqlite
- maybe your config files are meticulously crafted

so what are you doing about backups?
- AWS elastic block storage backups?

what about:
- point in time?
- recovery procedure?
- backup schedule?
- data provenance?
- edge compute & multi-cloud?

other people have automated solutions to these problems!

- see: [borgbackup](https://borgbackup.readthedocs.io/en/stable/#what-is-borgbackup)

