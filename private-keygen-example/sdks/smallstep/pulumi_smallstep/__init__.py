# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .account import *
from .attestation_authority import *
from .authority import *
from .collection import *
from .collection_instance import *
from .device_collection import *
from .device_collection_account import *
from .get_account import *
from .get_attestation_authority import *
from .get_authority import *
from .get_collection import *
from .get_collection_instance import *
from .get_device_collection_account import *
from .get_provisioner import *
from .get_provisioner_webhook import *
from .provider import *
from .provisioner import *
from .provisioner_webhook import *
from .workload import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_smallstep.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_smallstep.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "smallstep",
  "mod": "index/account",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/account:Account": "Account"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/attestationAuthority",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/attestationAuthority:AttestationAuthority": "AttestationAuthority"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/authority",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/authority:Authority": "Authority"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/collection",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/collection:Collection": "Collection"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/collectionInstance",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/collectionInstance:CollectionInstance": "CollectionInstance"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/deviceCollection",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/deviceCollection:DeviceCollection": "DeviceCollection"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/deviceCollectionAccount",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/deviceCollectionAccount:DeviceCollectionAccount": "DeviceCollectionAccount"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/provisioner",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/provisioner:Provisioner": "Provisioner"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/provisionerWebhook",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/provisionerWebhook:ProvisionerWebhook": "ProvisionerWebhook"
  }
 },
 {
  "pkg": "smallstep",
  "mod": "index/workload",
  "fqn": "pulumi_smallstep",
  "classes": {
   "smallstep:index/workload:Workload": "Workload"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "smallstep",
  "token": "pulumi:providers:smallstep",
  "fqn": "pulumi_smallstep",
  "class": "Provider"
 }
]
"""
)
