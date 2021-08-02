# Provisioning EC2 on VPC using Pulumi (Python)

## Resources provisioned by this code

- VPC
  - Public subnet
  - Internet gateway
  - Route table
  - Security group
- EC2 instance (CentOS 7.9.2009 x86_64)
  - Key pair
  - Elastic IP

## Usage

Create `secrets.py` and add your public key. The example format is presented on the file `secrets.py.example`. Then you can create a Pulumi stack and deploy it.

```bash
pulumi new aws-python  # Create a new Pulumi stack
pulumi up  # Deploy the stack
```
