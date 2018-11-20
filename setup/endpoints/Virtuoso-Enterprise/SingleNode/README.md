
# Setup Virtuoso Enterprise Edition (PAGO ami)

* Go to the Amazon EC2 console: https://console.aws.amazon.com/ec2/
	1. Choose AMI from AWS marketplace: Virtuoso Universal Server 7.2.42 (Enterprise-- Cloud PAGO Edition)
	2. Choose instance type: r3.2xlarge (64GB RAM machine with 8 vCPU)
	3. Configure instance (leave as is, or choose 3 instances for cluster setups)
	4. Add Storage: Add EBS volume 1000 GB (sdb), root volume 80GB , choose volume type provisioned IOPS (we chose 1000)
	5. Add tags: optional
	6. Configure security group - open ports required for Virtuoso (8890, 80 and 22 are required, source = anywhere)
	7. Review and launch: you need to select an amazon key-pair to be able to ssh to your nodes! (see AWS documentation for more information)


* Connect to your instance: ssh -X -i <your_key>.pem  <user>@<public_dsn_name.com>

* run prepareVirtuoso.sh
	- this script will mount the EBS Volume
	- move all virtuoso files to the 1TB volume and creating symlinks on the root partition
	- it creates a data directory in Virtuoso home directory 

* download the triples dataset in the data folder


