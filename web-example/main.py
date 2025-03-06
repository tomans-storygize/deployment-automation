import json
from pathlib import Path
import mimetypes

import pulumi
from pulumi_aws import s3


class S3Website:

    def __init__(self, prefix: str):
        DEPLOY_PREFIX = prefix

        self.S3_BUCKET_NAME = f"{DEPLOY_PREFIX}-s3-bucket"
        self.S3_SITE_NAME = f"{DEPLOY_PREFIX}-s3-website"
        self.S3_BLOCK_RULE_NAME = f"{DEPLOY_PREFIX}-public-access-block"
        self.BUCKET_POLICY_NAME = f"{DEPLOY_PREFIX}-bucket-policy"
        

    def deploy(self) -> None:
        web_bucket = s3.BucketV2(self.S3_BUCKET_NAME)

        web_site = s3.BucketWebsiteConfigurationV2(
           self.S3_SITE_NAME, bucket=web_bucket.bucket, index_document={"suffix": "index.html"}
        )

        public_access_block = s3.BucketPublicAccessBlock(
            # https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
            self.S3_BLOCK_RULE_NAME, bucket=web_bucket.id, block_public_acls=False
        )

        content_dir = "www"
        for file in Path(content_dir).glob("**/*"):
            if file.is_file():
                filepath = file.absolute()
                mime_type, _ = mimetypes.guess_type(filepath)
                obj = s3.BucketObject(
                    str(file), bucket=web_bucket.id, source=pulumi.FileAsset(filepath), content_type=mime_type
                )

        bucket_name = web_bucket.id
        bucket_policy = s3.BucketPolicy(
            self.BUCKET_POLICY_NAME,
            bucket=bucket_name,
            policy=self.public_read_policy_for_bucket(bucket_name),
            opts=pulumi.ResourceOptions(depends_on=[public_access_block]),
        )

        # Export the name of the bucket
        pulumi.export("bucket_name", web_bucket.id)
        pulumi.export("website_url", web_site.website_endpoint)


    def public_read_policy_for_bucket(self, bucket_name) -> pulumi.Output[str]:
        return pulumi.Output.json_dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    # bucket policy: anyone with this URL can read
                    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [
                            pulumi.Output.format("arn:aws:s3:::{0}/*", bucket_name),
                        ],
                    }
                ],
            }
        )


if __name__ == "__main__":
    S3Website("tomans-toy-website").deploy()
