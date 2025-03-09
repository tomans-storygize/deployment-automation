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

__all__ = ['CollectionInstanceArgs', 'CollectionInstance']

@pulumi.input_type
class CollectionInstanceArgs:
    def __init__(__self__, *,
                 collection_instance_id: pulumi.Input[str],
                 collection_slug: pulumi.Input[str],
                 data: pulumi.Input[str]):
        """
        The set of arguments for constructing a CollectionInstance resource.
        :param pulumi.Input[str] collection_slug: The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
               resource in the same config you MUST use depends_on to avoid race conditions.
        :param pulumi.Input[str] data: The instance data.
        """
        pulumi.set(__self__, "collection_instance_id", collection_instance_id)
        pulumi.set(__self__, "collection_slug", collection_slug)
        pulumi.set(__self__, "data", data)

    @property
    @pulumi.getter(name="collectionInstanceId")
    def collection_instance_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "collection_instance_id")

    @collection_instance_id.setter
    def collection_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "collection_instance_id", value)

    @property
    @pulumi.getter(name="collectionSlug")
    def collection_slug(self) -> pulumi.Input[str]:
        """
        The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
        resource in the same config you MUST use depends_on to avoid race conditions.
        """
        return pulumi.get(self, "collection_slug")

    @collection_slug.setter
    def collection_slug(self, value: pulumi.Input[str]):
        pulumi.set(self, "collection_slug", value)

    @property
    @pulumi.getter
    def data(self) -> pulumi.Input[str]:
        """
        The instance data.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: pulumi.Input[str]):
        pulumi.set(self, "data", value)


@pulumi.input_type
class _CollectionInstanceState:
    def __init__(__self__, *,
                 collection_instance_id: Optional[pulumi.Input[str]] = None,
                 collection_slug: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 out_data: Optional[pulumi.Input[str]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CollectionInstance resources.
        :param pulumi.Input[str] collection_slug: The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
               resource in the same config you MUST use depends_on to avoid race conditions.
        :param pulumi.Input[str] created_at: Timestamp in RFC3339 format when the instance was added to the collection.
        :param pulumi.Input[str] data: The instance data.
        :param pulumi.Input[str] out_data: The instance data stored after any modifications made server-side. If the instance belongs to a device collection a host
               ID attribute will be added to the data.
        :param pulumi.Input[str] updated_at: Timestamp in RFC3339 format when the instance was last changed.
        """
        if collection_instance_id is not None:
            pulumi.set(__self__, "collection_instance_id", collection_instance_id)
        if collection_slug is not None:
            pulumi.set(__self__, "collection_slug", collection_slug)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if data is not None:
            pulumi.set(__self__, "data", data)
        if out_data is not None:
            pulumi.set(__self__, "out_data", out_data)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="collectionInstanceId")
    def collection_instance_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "collection_instance_id")

    @collection_instance_id.setter
    def collection_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "collection_instance_id", value)

    @property
    @pulumi.getter(name="collectionSlug")
    def collection_slug(self) -> Optional[pulumi.Input[str]]:
        """
        The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
        resource in the same config you MUST use depends_on to avoid race conditions.
        """
        return pulumi.get(self, "collection_slug")

    @collection_slug.setter
    def collection_slug(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "collection_slug", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp in RFC3339 format when the instance was added to the collection.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def data(self) -> Optional[pulumi.Input[str]]:
        """
        The instance data.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter(name="outData")
    def out_data(self) -> Optional[pulumi.Input[str]]:
        """
        The instance data stored after any modifications made server-side. If the instance belongs to a device collection a host
        ID attribute will be added to the data.
        """
        return pulumi.get(self, "out_data")

    @out_data.setter
    def out_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "out_data", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp in RFC3339 format when the instance was last changed.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)


class CollectionInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collection_instance_id: Optional[pulumi.Input[str]] = None,
                 collection_slug: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a CollectionInstance resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collection_slug: The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
               resource in the same config you MUST use depends_on to avoid race conditions.
        :param pulumi.Input[str] data: The instance data.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CollectionInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a CollectionInstance resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param CollectionInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CollectionInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collection_instance_id: Optional[pulumi.Input[str]] = None,
                 collection_slug: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CollectionInstanceArgs.__new__(CollectionInstanceArgs)

            if collection_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'collection_instance_id'")
            __props__.__dict__["collection_instance_id"] = collection_instance_id
            if collection_slug is None and not opts.urn:
                raise TypeError("Missing required property 'collection_slug'")
            __props__.__dict__["collection_slug"] = collection_slug
            if data is None and not opts.urn:
                raise TypeError("Missing required property 'data'")
            __props__.__dict__["data"] = data
            __props__.__dict__["created_at"] = None
            __props__.__dict__["out_data"] = None
            __props__.__dict__["updated_at"] = None
        super(CollectionInstance, __self__).__init__(
            'smallstep:index/collectionInstance:CollectionInstance',
            resource_name,
            __props__,
            opts,
            package_ref=_utilities.get_package())

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            collection_instance_id: Optional[pulumi.Input[str]] = None,
            collection_slug: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            data: Optional[pulumi.Input[str]] = None,
            out_data: Optional[pulumi.Input[str]] = None,
            updated_at: Optional[pulumi.Input[str]] = None) -> 'CollectionInstance':
        """
        Get an existing CollectionInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collection_slug: The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
               resource in the same config you MUST use depends_on to avoid race conditions.
        :param pulumi.Input[str] created_at: Timestamp in RFC3339 format when the instance was added to the collection.
        :param pulumi.Input[str] data: The instance data.
        :param pulumi.Input[str] out_data: The instance data stored after any modifications made server-side. If the instance belongs to a device collection a host
               ID attribute will be added to the data.
        :param pulumi.Input[str] updated_at: Timestamp in RFC3339 format when the instance was last changed.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CollectionInstanceState.__new__(_CollectionInstanceState)

        __props__.__dict__["collection_instance_id"] = collection_instance_id
        __props__.__dict__["collection_slug"] = collection_slug
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["data"] = data
        __props__.__dict__["out_data"] = out_data
        __props__.__dict__["updated_at"] = updated_at
        return CollectionInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="collectionInstanceId")
    def collection_instance_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "collection_instance_id")

    @property
    @pulumi.getter(name="collectionSlug")
    def collection_slug(self) -> pulumi.Output[str]:
        """
        The collection will be created implicitly if it does not exist. If creating this collection with a smallstep.Collection
        resource in the same config you MUST use depends_on to avoid race conditions.
        """
        return pulumi.get(self, "collection_slug")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Timestamp in RFC3339 format when the instance was added to the collection.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def data(self) -> pulumi.Output[str]:
        """
        The instance data.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter(name="outData")
    def out_data(self) -> pulumi.Output[str]:
        """
        The instance data stored after any modifications made server-side. If the instance belongs to a device collection a host
        ID attribute will be added to the data.
        """
        return pulumi.get(self, "out_data")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Timestamp in RFC3339 format when the instance was last changed.
        """
        return pulumi.get(self, "updated_at")

