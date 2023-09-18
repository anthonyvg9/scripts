from docbooks.lib.s3.cluster_snapshot import list_snapshots_s3
snapshots_and_deltas = list_snapshots_s3(prefix=f'bfa9c3c4-0355-41b8-887c-a927a3686201/2023-08-28T00:59')
snapshots = list(filter(lambda path: 'snapshot.json' in path, snapshots_and_deltas))
#snapshots_and_deltas
snapshots

from docbooks.lib.s3.cluster_snapshot import ClusterSnapshot
snap = ClusterSnapshot.from_s3_full_path(snapshots[0])
for node_item in snap.raw['nodeList']['items']:
    node_name = node_item['metadata']['name']
    print("Node Name:", node_name)