# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities

__all__ = [
    'GetCollectionInstanceResult',
    'AwaitableGetCollectionInstanceResult',
    'get_collection_instance',
    'get_collection_instance_output',
]

@pulumi.output_type
class GetCollectionInstanceResult:
    """
    A collection of values returned by getCollectionInstance.
    """
    def __init__(__self__, collection_slug=None, created_at=None, data=None, id=None, out_data=None, updated_at=None):
        if collection_slug and not isinstance(collection_slug, str):
            raise TypeError("Expected argument 'collection_slug' to be a str")
        pulumi.set(__self__, "collection_slug", collection_slug)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if data and not isinstance(data, str):
            raise TypeError("Expected argument 'data' to be a str")
        pulumi.set(__self__, "data", data)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if out_data and not isinstance(out_data, str):
            raise TypeError("Expected argument 'out_data' to be a str")
        pulumi.set(__self__, "out_data", out_data)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="collectionSlug")
    def collection_slug(self) -> str:
        return pulumi.get(self, "collection_slug")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def data(self) -> str:
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outData")
    def out_data(self) -> str:
        return pulumi.get(self, "out_data")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        return pulumi.get(self, "updated_at")


class AwaitableGetCollectionInstanceResult(GetCollectionInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCollectionInstanceResult(
            collection_slug=self.collection_slug,
            created_at=self.created_at,
            data=self.data,
            id=self.id,
            out_data=self.out_data,
            updated_at=self.updated_at)


def get_collection_instance(collection_slug: Optional[str] = None,
                            id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCollectionInstanceResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['collectionSlug'] = collection_slug
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('smallstep:index/getCollectionInstance:getCollectionInstance', __args__, opts=opts, typ=GetCollectionInstanceResult, package_ref=_utilities.get_package()).value

    return AwaitableGetCollectionInstanceResult(
        collection_slug=pulumi.get(__ret__, 'collection_slug'),
        created_at=pulumi.get(__ret__, 'created_at'),
        data=pulumi.get(__ret__, 'data'),
        id=pulumi.get(__ret__, 'id'),
        out_data=pulumi.get(__ret__, 'out_data'),
        updated_at=pulumi.get(__ret__, 'updated_at'))
def get_collection_instance_output(collection_slug: Optional[pulumi.Input[str]] = None,
                                   id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCollectionInstanceResult]:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['collectionSlug'] = collection_slug
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('smallstep:index/getCollectionInstance:getCollectionInstance', __args__, opts=opts, typ=GetCollectionInstanceResult, package_ref=_utilities.get_package())
    return __ret__.apply(lambda __response__: GetCollectionInstanceResult(
        collection_slug=pulumi.get(__response__, 'collection_slug'),
        created_at=pulumi.get(__response__, 'created_at'),
        data=pulumi.get(__response__, 'data'),
        id=pulumi.get(__response__, 'id'),
        out_data=pulumi.get(__response__, 'out_data'),
        updated_at=pulumi.get(__response__, 'updated_at')))
