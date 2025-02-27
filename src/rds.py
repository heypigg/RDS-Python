from src.client_factory import EC2Client
from src.ec2 import EC2

RDS_DB_SUBNET_NAME = 'my-rds-subnet-group'

class RDS:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.rds """

    def create_postgresql_instance(self):
        print("Creating Amazon RDS PostgreSQL DB Instance...")

        security_group_id = self.create_db_securty_group_and_add_rules()

        # create subnet group
        self.create_db_subnet_group()
        print("Create DB Subnet group...")

        self._client.create_db_instance(
            DBName='MyPostgreSQLDB',
            DBInstanceIdentifier='mypostgresdb',
            DBInstanceClass='db.t2.micro',
            Engine='postgres',
            EngineVersion='9.6.6',
            Port=5432,
            MasterUsername='postgres',
            MasterUserPassword='mypostgrespassword',
            AllocatedStorage=20,
            MultiAZ=False,
            StorageType='gp2',
            PubliclyAccessible=True,
            VpcSecurityGroupIds =[security_group_id],
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'Molnar-PostgreSQL-Instance'
                }
            ]
        )

    def describe_instances(self):
        print("Describing all RDS instances...")
        return self._client.describe_db_instances()

    def modify_master_user_password(self, db_identifier, new_password):
        print("Modifying master user password...")
        return self._client.modify_db_instance(
            DBInstanceIdentifier=db_identifier,
            MasterUserPassword=new_password
        )

    def take_backup_of_db_instance(self, db_identifier, db_snapshot_identifier, tags):
        print("Backing up DB instance...")
        return self._client.create_db_snapshot(
            DBInstanceIdentifier=db_identifier,
            DBSnapshotIdentifier=db_snapshot_identifier,
            Tags=tags
        )

    def restore_db_from_backup(self, db_identifier, db_snapshot_identifier):
        print("Restoring DB from snapshot...")
        return self._client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db_identifier,
            DBSnapshotIdentifier=db_snapshot_identifier
    )

    def delete_db(self, db_identifier):
        print("Deleting RDS Instance with name " + db_identifier)
        return self._client.delete_db_instance(
            DBInstanceIdentifier=db_identifier,
            SkipFinalSnapshot=True
        )

    def create_db_subnet_group(self):
        print("Creating RDS DB Subnet Group " + RDS_DB_SUBNET_NAME)
        self._client.create_db_subnet_group(
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            DBSubnetGroupDescription='My own subnet group for RDS DB',
            SubnetIds=['subnet-03ff1d5c', 'subnet-3f22ce1e', 'subnet-48912005', 'subnet-937b9df5', 'subnet-a0d7e29e', 'subnet-f9a873f7']
        )

    def create_db_securty_group_and_add_rules(self):
        ec2_client = EC2Client().get_client()
        ec2 = EC2(ec2_client)

        # create security group
        security_group = ec2.create_security_group()

        # get id of the sg
        security_group_id = security_group['GroupId']

        print("Create RDS security group with id " + security_group_id)

        # add public access rule to sg
        ec2.add_inbound_rule_to_sg(security_group_id)

        print("Added inbound public access rule to sg with id " + security_group_id)

        return security_group_id
