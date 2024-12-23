import os
import json

cluster_spec = json.loads(os.environ["AFO_ENV_CLUSTER_SPEC"])
role = cluster_spec["role"]
assert role == "worker", "{} vs worker".format(role)
node_rank = cluster_spec["index"]
nnodes = len(cluster_spec[role])
try:
   import torch_npu
   nproc_per_node = os.popen("npu-smi info | grep 910B | wc -l").read().strip()
except ImportError:
   nproc_per_node = os.popen("nvidia-smi --list-gpus | wc -l").read().strip()
master = cluster_spec[role][0]
master_addr, master_ports = master.split(":")
master_ports = master_ports.split(",")
print(
   "python3 -m torch.distributed.launch "
   "--nproc_per_node={} "
   "--nnodes={} "
   "--node_rank={} "
   "--master_addr={} "
   "--master_port={}".format(
       nproc_per_node, nnodes, node_rank, master_addr, master_ports[0]
   )
)