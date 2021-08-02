"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

from secrets import PUBLIC_KEY


# Local variables
name_format = "uniglot-dev-{}"
az = "ap-northeast-2a"
size = "t2.micro"

# Create a VPC and a public subnet
vpc = aws.ec2.Vpc(
    name_format.format("vpc"),
    cidr_block="172.31.0.0/16",
    enable_dns_hostnames=True,
)

public_subnet = aws.ec2.Subnet(
    name_format.format("vpc-public-subnet"),
    cidr_block="172.31.32.0/20",
    vpc_id=vpc.id,
    availability_zone=az,
)

ig = aws.ec2.InternetGateway(
    name_format.format("ig"),
    vpc_id=vpc.id,
)

routetable = aws.ec2.RouteTable(
    name_format.format("routetable"),
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=ig.id,
        ),
    ],
    vpc_id=vpc.id,
)

routetable_assoc = aws.ec2.MainRouteTableAssociation(
    name_format.format("routetable-assoc"),
    route_table_id=routetable.id,
    vpc_id=vpc.id,
)

# Create a security group that restricts incoming traffic to HTTP
security_group = aws.ec2.SecurityGroup(
    name_format.format("security-group"),
    vpc_id=vpc.id,
    description="Enables HTTP access",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=0,
            to_port=65535,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)

# EC2 settings
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["125523088429"],
    filters=[
        aws.GetAmiFilterArgs(
            name="name",
            values=["CentOS 7.9.2009 x86_64"],
        )
    ],
)

keypair = aws.ec2.KeyPair(
    "uniglot-dev",
    public_key=PUBLIC_KEY,
)

ec2 = aws.ec2.Instance(
    "uniglot-dev",
    instance_type=size,
    vpc_security_group_ids=[security_group.id],
    availability_zone=az,
    subnet_id=public_subnet.id,
    ami=ami.id,
    key_name=keypair.key_name,
)

# Elastic IP settings
eip = aws.ec2.Eip(
    name_format.format("eip"),
    instance=ec2.id,
    vpc=True,
)
eip_assoc = aws.ec2.EipAssociation(
    name_format.format("eip-assoc"),
    instance_id=ec2.id,
    allocation_id=eip.id,
)

pulumi.export("elastic_ip", eip.public_ip)
