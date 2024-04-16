import boto3

client = boto3.client("elasticache")

paginator = client.get_paginator("describe_cache_clusters")


for page in paginator.paginate():
    for cluster in page["CacheClusters"]:
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
        region = client.meta.region_name
        cluster_arn = f"arn:aws:elasticache:{region}:{account_id}:cluster:{cluster['CacheClusterId']}"
        tags = client.list_tags_for_resource(ResourceName=cluster_arn)

        print(f"Cluster ARN: {cluster_arn}")
        print(f"Tags: {tags['TagList']}")
